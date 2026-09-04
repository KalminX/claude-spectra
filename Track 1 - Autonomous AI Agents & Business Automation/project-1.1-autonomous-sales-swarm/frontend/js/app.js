/**
 * AUTONOMOUS 5-AGENT SALES SWARM — FRONTEND CONTROLLER
 * Handles simulation control, real-time telemetry, lead inspection, and Agent 4 Closer sandbox.
 */

const App = (() => {
    // --- State ---
    const state = {
        currentTab: 'pipeline',
        leads: [],
        metrics: {},
        simState: {},
        selectedLeadId: null,
        isBusy: false
    };

    const PRESET_MESSAGES = {
        price_objection: "Sounds interesting, but how much does this service cost per month? We are a small crew on a tight budget.",
        complexity_objection: "How complicated is the setup? We don't have an IT team to manage this.",
        already_have_objection: "We already have an answering service that takes messages for us at night.",
        positive_interest: "Saw your email about our missed calls last weekend. Can I call the demo number right now from my cell?",
        unsubscribe: "Please remove me from your mailing list immediately."
    };

    // --- DOM Elements Cache ---
    let el = {};

    function initElements() {
        el = {
            stepBtn: document.getElementById('stepBtn'),
            runBatchBtn: document.getElementById('runBatchBtn'),
            resetBtn: document.getElementById('resetBtn'),
            simNiche: document.getElementById('simNiche'),
            simCity: document.getElementById('simCity'),
            simCount: document.getElementById('simCount'),
            simScenario: document.getElementById('simScenario'),
            currentStepBadge: document.getElementById('currentStepBadge'),
            batchProgressText: document.getElementById('batchProgressText'),
            leadsCountTab: document.getElementById('leadsCountTab'),
            leadsTableBody: document.getElementById('leadsTableBody'),
            eventLogContainer: document.getElementById('eventLogContainer'),
            
            // Sandbox elements
            sandboxLeadSelect: document.getElementById('sandboxLeadSelect'),
            sandboxPresetSelect: document.getElementById('sandboxPresetSelect'),
            sandboxMessageInput: document.getElementById('sandboxMessageInput'),
            sandboxSubmitBtn: document.getElementById('sandboxSubmitBtn'),
            closerEmptyState: document.getElementById('closerEmptyState'),
            closerResultCard: document.getElementById('closerResultCard'),
            closerStatusBadge: document.getElementById('closerStatusBadge'),
            closerIntentVal: document.getElementById('closerIntentVal'),
            closerConfidenceVal: document.getElementById('closerConfidenceVal'),
            closerReasoningVal: document.getElementById('closerReasoningVal'),
            closerActionVal: document.getElementById('closerActionVal'),
            closerResponseMsgVal: document.getElementById('closerResponseMsgVal'),

            // Meta-reviewer elements
            metaReviewBtn: document.getElementById('metaReviewBtn'),
            metaReviewEmptyState: document.getElementById('metaReviewEmptyState'),
            metaReviewContent: document.getElementById('metaReviewContent'),
            metaAnalysisSummary: document.getElementById('metaAnalysisSummary'),
            metaWeakPatterns: document.getElementById('metaWeakPatterns'),
            metaConversionGain: document.getElementById('metaConversionGain'),
            metaSubjectLines: document.getElementById('metaSubjectLines'),
            metaHookAngles: document.getElementById('metaHookAngles'),

            // Modal elements
            leadModal: document.getElementById('leadModal'),
            modalCompanyName: document.getElementById('modalCompanyName'),
            modalSubTitle: document.getElementById('modalSubTitle'),
            modalBody: document.getElementById('modalBody')
        };
    }

    // --- Tab Navigation ---
    function switchTab(tabId) {
        state.currentTab = tabId;
        const tabs = ['pipeline', 'closerSandbox', 'metaEvolution', 'eventLogs'];
        tabs.forEach(t => {
            const section = document.getElementById(`tab-${t}`);
            const btn = document.getElementById(`tab-${t}-btn`);
            if (t === tabId) {
                if (section) section.style.display = 'block';
                if (btn) btn.classList.add('active');
            } else {
                if (section) section.style.display = 'none';
                if (btn) btn.classList.remove('active');
            }
        });

        if (tabId === 'closerSandbox') {
            populateSandboxLeads();
        }
    }

    // --- API Service Calls ---
    async function fetchState() {
        try {
            const res = await fetch('/api/simulation/state');
            if (!res.ok) return;
            const data = await res.json();
            state.simState = data;
            updateMetricsUI(data.metrics);
            updateCurrentStepUI(data.current_step_name, data.current_step_index, data.total_steps);
            renderLogs(data.recent_logs);
            if (data.latest_refinement) {
                renderMetaRefinement(data.latest_refinement);
            }
        } catch (err) {
            console.warn("State polling error:", err);
        }
    }

    async function fetchLeads() {
        try {
            const res = await fetch('/api/simulation/leads');
            if (!res.ok) return;
            const leads = await res.json();
            state.leads = leads;
            renderLeadsTable(leads);
            if (el.leadsCountTab) el.leadsCountTab.innerText = leads.length;
        } catch (err) {
            console.warn("Leads fetch error:", err);
        }
    }

    async function stepSimulation() {
        if (state.isBusy) return;
        setBusy(true, el.stepBtn, "Stepping...");
        try {
            const niche = el.simNiche ? el.simNiche.value : "Plumbing";
            const cityParts = el.simCity ? el.simCity.value.split(',') : ["Dallas", "TX"];
            const count = el.simCount ? parseInt(el.simCount.value) : 2;
            const scenario = el.simScenario ? el.simScenario.value : "balanced";

            const res = await fetch('/api/simulation/step', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    niche,
                    city: cityParts[0],
                    state: cityParts[1],
                    count,
                    scenario
                })
            });
            if (!res.ok) throw new Error(await res.text());
            await fetchState();
            await fetchLeads();
        } catch (err) {
            alert("Simulation step failed: " + err.message);
        } finally {
            setBusy(false, el.stepBtn, "Step Agent");
        }
    }

    async function runFullBatch() {
        if (state.isBusy) return;
        setBusy(true, el.runBatchBtn, "Running Batch...");
        try {
            const niche = el.simNiche ? el.simNiche.value : "Plumbing";
            const cityParts = el.simCity ? el.simCity.value.split(',') : ["Dallas", "TX"];
            const count = el.simCount ? parseInt(el.simCount.value) : 3;
            const scenario = el.simScenario ? el.simScenario.value : "balanced";

            const res = await fetch('/api/simulation/run-batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    niche,
                    city: cityParts[0],
                    state: cityParts[1],
                    count,
                    scenario
                })
            });
            if (!res.ok) throw new Error(await res.text());
            await fetchState();
            await fetchLeads();
        } catch (err) {
            alert("Batch execution failed: " + err.message);
        } finally {
            setBusy(false, el.runBatchBtn, "Run Batch");
        }
    }

    async function resetSimulation() {
        if (!confirm("Are you sure you want to clear all simulated leads and reset the database?")) return;
        try {
            await fetch('/api/simulation/reset', { method: 'POST' });
            await fetchState();
            await fetchLeads();
            resetCloserSandboxUI();
        } catch (err) {
            alert("Reset failed: " + err.message);
        }
    }

    // --- UI Update Handlers ---
    function updateMetricsUI(m) {
        if (!m) return;
        setMetricText('metric-scouted', m.total_leads_scouted);
        setMetricText('stat-scouted', m.total_leads_scouted);

        const delRate = m.total_leads_scouted > 0 ? Math.round((m.verified_leads / m.total_leads_scouted) * 100) : 100;
        setMetricText('metric-deliverability', `${delRate}%`);
        setMetricText('stat-verified', m.verified_leads);

        setMetricText('metric-outreach', m.outreach_sent);
        setMetricText('stat-hooks', m.outreach_sent);

        setMetricText('metric-replies', m.replies_received);
        setMetricText('metric-positives', m.positive_replies);
        setMetricText('metric-unsub', m.unsubscribes);
        setMetricText('metric-demos', m.demos_booked);
        setMetricText('stat-objections', m.objections_handled);
        setMetricText('stat-demos', m.demos_booked);
    }

    function setMetricText(id, val) {
        const elem = document.getElementById(id);
        if (elem) elem.innerText = val;
    }

    function updateCurrentStepUI(stepName, stepIndex, total) {
        if (el.currentStepBadge) el.currentStepBadge.innerText = stepName || 'idle';
        if (el.batchProgressText) el.batchProgressText.innerText = `(Step ${stepIndex}/${total})`;

        const agentKeys = ['scout', 'verifier', 'personalizer', 'closer', 'meta_review'];
        agentKeys.forEach((agent, idx) => {
            const badge = document.getElementById(`badge-${agent}`);
            const card = document.getElementById(`card-${agent}`);
            if (!badge || !card) return;

            if (idx < stepIndex) {
                badge.innerText = 'DONE';
                badge.className = 'badge badge-done';
                card.classList.remove('is-active');
            } else if (idx === stepIndex) {
                badge.innerText = 'ACTIVE';
                badge.className = 'badge badge-active';
                card.classList.add('is-active');
            } else {
                badge.innerText = 'WAITING';
                badge.className = 'badge badge-waiting';
                card.classList.remove('is-active');
            }
        });
    }

    function renderLeadsTable(leads) {
        if (!el.leadsTableBody) return;
        if (!leads || leads.length === 0) {
            el.leadsTableBody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align: center; padding: 1.5rem; color: var(--text-dim);">
                        No leads in active session. Advance an agent step or run a batch to populate.
                    </td>
                </tr>
            `;
            return;
        }

        el.leadsTableBody.innerHTML = leads.map(l => {
            const statusTag = l.status === 'SUPPRESSED' ? '<span class="badge" style="background: rgba(244,63,94,0.15); color: #f43f5e; border: 1px solid #f43f5e;">SUPPRESSED</span>' :
                              l.status.includes('VERIFIED_PASSED') || l.status === 'HOOK_GENERATED' ? '<span class="badge badge-done">' + l.status + '</span>' :
                              l.status.includes('DISCARDED') ? '<span class="badge badge-active">' + l.status + '</span>' :
                              '<span class="badge badge-waiting">' + l.status + '</span>';

            const score = l.email_deliverability_score ? Math.round(l.email_deliverability_score * 100) : 95;
            const scoreColor = score >= 80 ? 'var(--emerald)' : 'var(--amber)';
            const lostRevHtml = l.lost_revenue ? `<span style="color: var(--rose); font-weight: bold;">$${Math.round(l.lost_revenue).toLocaleString()}/mo</span>` : '<span style="color: var(--text-dim);">-</span>';

            return `
                <tr>
                    <td>
                        <div style="font-weight: 700; color: #fff;">${escapeHtml(l.company_name)}</div>
                        <div style="font-size: 0.68rem; color: var(--text-dim);">${escapeHtml(l.niche)} • ${escapeHtml(l.owner_name)}</div>
                    </td>
                    <td>
                        <div style="color: var(--text-muted); font-family: var(--font-mono);">${escapeHtml(l.email)}</div>
                        <div style="font-size: 0.68rem; color: var(--text-dim); font-family: var(--font-mono);">${escapeHtml(l.phone)}</div>
                    </td>
                    <td style="color: var(--text-muted);">${escapeHtml(l.city)}, ${escapeHtml(l.state)}</td>
                    <td>
                        <span style="color: ${scoreColor}; font-weight: 600; font-family: var(--font-mono);">
                            ${score}% (${escapeHtml(l.phone_type || 'mobile')})
                        </span>
                    </td>
                    <td style="font-family: var(--font-mono);">${lostRevHtml}</td>
                    <td>${statusTag}</td>
                    <td style="text-align: right;">
                        <button onclick="App.viewLeadDetail('${l.id}')" class="btn btn-secondary" style="padding: 0.25rem 0.55rem; font-size: 0.72rem;">
                            Inspect
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    }

    function renderLogs(logs) {
        if (!el.eventLogContainer || !logs || logs.length === 0) return;
        el.eventLogContainer.innerHTML = logs.map(l => {
            const color = l.level === 'success' ? 'var(--emerald)' : l.level === 'warning' ? 'var(--amber)' : 'var(--text-muted)';
            return `
                <div style="line-height: 1.45; border-bottom: 1px solid rgba(255,255,255,0.03); padding-bottom: 0.25rem;">
                    <span style="color: var(--text-dim);">[${l.timestamp}]</span>
                    <span style="color: var(--cyan); font-weight: 600;">[${escapeHtml(l.source)}]</span>
                    <span style="color: ${color};">${escapeHtml(l.message)}</span>
                </div>
            `;
        }).join('');
        el.eventLogContainer.scrollTop = el.eventLogContainer.scrollHeight;
    }

    // --- Closer Sandbox ---
    function populateSandboxLeads() {
        if (!el.sandboxLeadSelect) return;
        el.sandboxLeadSelect.innerHTML = '<option value="">-- Select a simulated lead --</option>' +
            state.leads.map(l => `<option value="${l.id}">${escapeHtml(l.company_name)} (${escapeHtml(l.niche)})</option>`).join('');
        applyPresetText();
    }

    function applyPresetText() {
        if (!el.sandboxPresetSelect || !el.sandboxMessageInput) return;
        const preset = el.sandboxPresetSelect.value;
        if (PRESET_MESSAGES[preset]) {
            el.sandboxMessageInput.value = PRESET_MESSAGES[preset];
        }
    }

    async function submitSandboxReply() {
        if (!el.sandboxLeadSelect || !el.sandboxLeadSelect.value) {
            alert("Please select a simulated contractor from the dropdown.");
            return;
        }

        const leadId = el.sandboxLeadSelect.value;
        const scenario = el.sandboxPresetSelect ? el.sandboxPresetSelect.value : "price_objection";
        const customText = el.sandboxMessageInput ? el.sandboxMessageInput.value : "";

        setBusy(true, el.sandboxSubmitBtn, "Classifying...");

        try {
            const res = await fetch('/api/simulation/closer-reply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    lead_id: leadId,
                    scenario,
                    custom_text: customText
                })
            });
            if (!res.ok) throw new Error(await res.text());
            const data = await res.json();
            renderCloserDecision(data.closer_response);
            await fetchState();
            await fetchLeads();
        } catch (err) {
            alert("Closer processing failed: " + err.message);
        } finally {
            setBusy(false, el.sandboxSubmitBtn, "Submit Reply");
        }
    }

    function renderCloserDecision(c) {
        if (!c) return;
        if (el.closerEmptyState) el.closerEmptyState.style.display = 'none';
        if (el.closerResultCard) el.closerResultCard.style.display = 'block';

        if (el.closerStatusBadge) {
            el.closerStatusBadge.innerText = 'COMPLETED';
            el.closerStatusBadge.className = 'badge badge-done';
        }

        if (el.closerIntentVal) el.closerIntentVal.innerText = c.detected_intent;
        if (el.closerConfidenceVal) el.closerConfidenceVal.innerText = `${Math.round(c.confidence * 100)}%`;
        if (el.closerReasoningVal) el.closerReasoningVal.innerText = c.reasoning;
        if (el.closerActionVal) el.closerActionVal.innerText = c.action_taken;
        if (el.closerResponseMsgVal) el.closerResponseMsgVal.innerText = c.response_message;
    }

    function resetCloserSandboxUI() {
        if (el.closerEmptyState) el.closerEmptyState.style.display = 'block';
        if (el.closerResultCard) el.closerResultCard.style.display = 'none';
        if (el.closerStatusBadge) {
            el.closerStatusBadge.innerText = 'IDLE';
            el.closerStatusBadge.className = 'badge badge-waiting';
        }
    }

    // --- Meta-Reviewer ---
    async function triggerMetaReview() {
        setBusy(true, el.metaReviewBtn, "Optimizing...");
        try {
            const res = await fetch('/api/simulation/meta-review', { method: 'POST' });
            if (!res.ok) throw new Error(await res.text());
            const refinement = await res.json();
            renderMetaRefinement(refinement);
            await fetchState();
        } catch (err) {
            alert("Optimization failed: " + err.message);
        } finally {
            setBusy(false, el.metaReviewBtn, "Run Optimization");
        }
    }

    function renderMetaRefinement(r) {
        if (!r) return;
        if (el.metaReviewEmptyState) el.metaReviewEmptyState.style.display = 'none';
        if (el.metaReviewContent) el.metaReviewContent.style.display = 'block';

        if (el.metaAnalysisSummary) el.metaAnalysisSummary.innerText = r.analysis_summary;
        if (el.metaConversionGain) el.metaConversionGain.innerText = r.expected_conversion_gain;

        if (el.metaWeakPatterns) {
            el.metaWeakPatterns.innerHTML = (r.weak_patterns_detected || []).map(p => `<li>${escapeHtml(p)}</li>`).join('');
        }
        if (el.metaSubjectLines) {
            el.metaSubjectLines.innerHTML = (r.improved_subject_lines || []).map(s => 
                `<div class="card" style="padding: 0.5rem 0.75rem; color: var(--amber); font-family: var(--font-mono); font-size: 0.75rem;">${escapeHtml(s)}</div>`
            ).join('');
        }
        if (el.metaHookAngles) {
            el.metaHookAngles.innerHTML = (r.adjusted_hook_angles || []).map(a => 
                `<div class="card" style="padding: 0.5rem 0.75rem; color: var(--cyan); font-size: 0.75rem;">${escapeHtml(a)}</div>`
            ).join('');
        }
    }

    // --- Lead Detail Inspection Modal ---
    async function viewLeadDetail(leadId) {
        try {
            const res = await fetch(`/api/simulation/leads/${leadId}`);
            if (!res.ok) throw new Error("Lead not found");
            const l = await res.json();

            if (el.modalCompanyName) el.modalCompanyName.innerText = l.company_name;
            if (el.modalSubTitle) el.modalSubTitle.innerText = `${l.id} • ${l.niche} • ${l.city}, ${l.state}`;

            let bodyHtml = `
                <div class="card modal-lead-overview">
                    <div><strong style="color: var(--text-dim);">Owner:</strong> ${escapeHtml(l.owner_name)}</div>
                    <div><strong style="color: var(--text-dim);">Synthetic Email:</strong> <span style="font-family: var(--font-mono);">${escapeHtml(l.email)}</span></div>
                    <div><strong style="color: var(--text-dim);">Phone:</strong> <span style="font-family: var(--font-mono);">${escapeHtml(l.phone)}</span></div>
                    <div><strong style="color: var(--text-dim);">24/7 Service Claim:</strong> ${l.has_24_7_service_claim ? '<span style="color: var(--emerald);">Yes</span>' : 'Standard'}</div>
                </div>
            `;

            if (l.verification) {
                bodyHtml += `
                    <div class="card" style="padding: 0.85rem;">
                        <div style="font-weight: 700; color: #fff; margin-bottom: 0.25rem;">Agent 2: Verification Audit</div>
                        <div style="color: var(--text-muted);">
                            Score: <strong style="color: var(--emerald);">${Math.round(l.verification.deliverability_score * 100)}%</strong> | 
                            Carrier Line: <strong style="color: var(--amber);">${l.verification.phone_type}</strong> | 
                            Status: <strong>${l.verification.status}</strong>
                        </div>
                        <div style="font-size: 0.72rem; color: var(--text-dim); margin-top: 0.25rem;">${escapeHtml(l.verification.reason)}</div>
                    </div>
                `;
            }

            if (l.reviews && l.reviews.length > 0) {
                bodyHtml += `
                    <div>
                        <div style="font-weight: 700; color: #fff; margin-bottom: 0.35rem;">Discovered Customer Reviews:</div>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            ${l.reviews.map(r => `
                                <div class="card" style="padding: 0.75rem; font-size: 0.75rem;">
                                    <div style="color: var(--amber); font-weight: bold;">${'★'.repeat(r.rating)}${'☆'.repeat(5-r.rating)} - ${escapeHtml(r.author)}</div>
                                    <div style="color: var(--text-muted); margin-top: 0.25rem;">${escapeHtml(r.text)}</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            }

            if (l.hook) {
                bodyHtml += `
                    <div class="card" style="padding: 0.85rem; border-color: rgba(16,185,129,0.3); background: rgba(16,185,129,0.04);">
                        <div style="font-weight: 700; color: var(--emerald); margin-bottom: 0.25rem;">Agent 3: Synthesized 3-Sentence ROI Hook</div>
                        <div style="color: var(--text-dim); font-size: 0.72rem;">Subject: <span style="color: var(--amber); font-family: var(--font-mono);">${escapeHtml(l.hook.subject_line)}</span></div>
                        <div style="background: rgba(0,0,0,0.3); padding: 0.6rem; border-radius: 0.4rem; margin: 0.4rem 0; line-height: 1.45; color: var(--text-main);">
                            ${escapeHtml(l.hook.email_body)}
                        </div>
                        <div style="color: var(--rose); font-weight: bold; font-family: var(--font-mono); font-size: 0.75rem;">
                            Estimated Lost Revenue: $${Math.round(l.hook.lost_revenue).toLocaleString()}/month
                        </div>
                    </div>
                `;
            }

            if (l.conversations && l.conversations.length > 0) {
                bodyHtml += `
                    <div>
                        <div style="font-weight: 700; color: #fff; margin-bottom: 0.35rem;">Conversation Thread:</div>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            ${l.conversations.map(c => `
                                <div class="card" style="padding: 0.75rem; font-size: 0.75rem; border-color: ${c.direction === 'OUTBOUND' ? 'rgba(16,185,129,0.2)' : 'rgba(245,158,11,0.2)'};">
                                    <div style="font-size: 0.68rem; font-weight: 700; color: ${c.direction === 'OUTBOUND' ? 'var(--emerald)' : 'var(--amber)'};">
                                        ${c.direction} (${c.channel}) • ${c.timestamp}
                                    </div>
                                    <div style="margin-top: 0.25rem; color: var(--text-main);">${escapeHtml(c.message_content)}</div>
                                    ${c.detected_intent ? `<div style="font-size: 0.68rem; color: var(--cyan); margin-top: 0.25rem; font-family: var(--font-mono);">Intent: ${c.detected_intent} • Action: ${c.action_taken}</div>` : ''}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            }

            if (el.modalBody) el.modalBody.innerHTML = bodyHtml;
            if (el.leadModal) el.leadModal.classList.add('is-open');
        } catch (err) {
            alert("Failed to load lead details: " + err.message);
        }
    }

    function closeModal() {
        if (el.leadModal) el.leadModal.classList.remove('is-open');
    }

    // --- Helpers ---
    function setBusy(busy, buttonEl, label) {
        state.isBusy = busy;
        if (buttonEl) {
            buttonEl.disabled = busy;
            buttonEl.innerText = label;
        }
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // --- Init ---
    function init() {
        initElements();
        fetchState();
        fetchLeads();
        setInterval(fetchState, 4000);
    }

    // Public API
    return {
        init,
        switchTab,
        stepSimulation,
        runFullBatch,
        resetSimulation,
        applyPresetText,
        submitSandboxReply,
        triggerMetaReview,
        viewLeadDetail,
        closeModal
    };
})();

// Bootstrap on DOM ready
document.addEventListener('DOMContentLoaded', App.init);
