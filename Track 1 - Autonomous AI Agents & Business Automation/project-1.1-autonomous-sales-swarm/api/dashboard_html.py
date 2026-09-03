def get_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autonomous 5-Agent Sales Swarm — Simulation & Control Center</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#ecfdf5',
                            500: '#10b981',
                            600: '#059669',
                        },
                        darkBg: '#090d16',
                        cardBg: '#111827',
                        cardBorder: '#1f2937'
                    }
                }
            }
        }
    </script>
    <style>
        body { background-color: #090d16; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .glass-card { background: rgba(17, 24, 39, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .tab-btn.active { border-bottom: 2px solid #10b981; color: #10b981; font-weight: 600; }
        .pulse-dot { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: .4; transform: scale(1.15); } }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0b0f19; }
        ::-webkit-scrollbar-thumb { background: #1f2937; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #374151; }
    </style>
</head>
<body class="text-slate-200 min-h-screen flex flex-col">

    <!-- Top Navigation Header -->
    <header class="border-b border-slate-800/80 bg-slate-950/80 sticky top-0 z-40 backdrop-blur">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-9 h-9 rounded-lg bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 font-bold text-lg">
                    ⚡
                </div>
                <div>
                    <h1 class="text-base font-bold text-white tracking-tight flex items-center gap-2">
                        AUTONOMOUS SALES SWARM
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 pulse-dot"></span> 100% SIMULATION MODE
                        </span>
                    </h1>
                    <p class="text-xs text-slate-400">SkillsVital Voice AI Engine • Zero Real Data • Safe RFC Test Range</p>
                </div>
            </div>

            <!-- Quick Action Buttons -->
            <div class="flex items-center space-x-2">
                <button onclick="stepSimulation()" id="stepBtn" class="px-3 py-1.5 text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg border border-slate-700 transition flex items-center gap-1.5">
                    <span>⏭</span> Step Agent
                </button>
                <button onclick="runFullBatch()" id="runBatchBtn" class="px-3.5 py-1.5 text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg shadow-sm shadow-emerald-900/50 transition flex items-center gap-1.5">
                    <span>▶</span> Run Full Batch
                </button>
                <button onclick="resetSimulation()" class="px-2.5 py-1.5 text-xs font-medium text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg border border-transparent hover:border-red-500/20 transition" title="Reset Database & Simulation">
                    <span>🔄</span> Reset
                </button>
            </div>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

        <!-- Simulation Control Bar -->
        <section class="glass-card rounded-xl p-4 border border-slate-800">
            <div class="flex flex-wrap items-center justify-between gap-4">
                <div class="flex flex-wrap items-center gap-3">
                    <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Parameters:</span>
                    
                    <!-- Niche Select -->
                    <select id="simNiche" class="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-2.5 py-1.5 focus:border-emerald-500 focus:outline-none">
                        <option value="Plumbing">Plumbing (Emergency Drain/Leak)</option>
                        <option value="HVAC">HVAC (A/C & Heating Failures)</option>
                        <option value="Electrical">Electrical (Emergency Tripped Power)</option>
                        <option value="Roofing">Roofing (Storm Damage Leak)</option>
                    </select>

                    <!-- City Select -->
                    <select id="simCity" class="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-2.5 py-1.5 focus:border-emerald-500 focus:outline-none">
                        <option value="Dallas,TX">Dallas, TX (214)</option>
                        <option value="Phoenix,AZ">Phoenix, AZ (602)</option>
                        <option value="Denver,CO">Denver, CO (303)</option>
                        <option value="Orlando,FL">Orlando, FL (407)</option>
                        <option value="Austin,TX">Austin, TX (512)</option>
                        <option value="Atlanta,GA">Atlanta, GA (404)</option>
                    </select>

                    <!-- Batch Count -->
                    <select id="simCount" class="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-2.5 py-1.5 focus:border-emerald-500 focus:outline-none">
                        <option value="2">2 Simulated Leads</option>
                        <option value="3" selected>3 Simulated Leads</option>
                        <option value="5">5 Simulated Leads</option>
                        <option value="8">8 Simulated Leads</option>
                    </select>

                    <!-- Scenario Select -->
                    <select id="simScenario" class="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-2.5 py-1.5 focus:border-emerald-500 focus:outline-none">
                        <option value="balanced">Scenario: Balanced Realistic Mix</option>
                        <option value="price_objection">Scenario: Price Pushback ($497/mo)</option>
                        <option value="complexity_objection">Scenario: Setup Hesitation (No IT)</option>
                        <option value="positive_interest">Scenario: High Interest (Demo Link)</option>
                        <option value="unsubscribe">Scenario: Unsubscribe Waves</option>
                    </select>
                </div>

                <div class="flex items-center space-x-2 text-xs">
                    <span class="text-slate-400">Current Step:</span>
                    <span id="currentStepBadge" class="px-2 py-0.5 rounded bg-slate-800 text-emerald-400 font-mono font-semibold border border-slate-700">
                        scout
                    </span>
                    <span id="batchProgressText" class="text-slate-500 font-mono text-[11px]">(Step 0/7)</span>
                </div>
            </div>
        </section>

        <!-- 5-Agent Architecture Swarm Pipeline Cards -->
        <section class="grid grid-cols-1 md:grid-cols-5 gap-3">
            <!-- Agent 1 -->
            <div id="card-scout" class="glass-card rounded-xl p-3.5 border border-slate-800 transition hover:border-slate-700">
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Agent 1</span>
                    <span id="badge-scout" class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">READY</span>
                </div>
                <h3 class="text-xs font-bold text-white mb-1">Lead Scout</h3>
                <p class="text-[11px] text-slate-400 line-clamp-2">Generates synthetic contractors, extracts 1-star missed-call reviews & 24/7 claims.</p>
                <div class="mt-2 pt-2 border-t border-slate-800 text-[11px] text-slate-300 font-mono flex justify-between">
                    <span>Scouted:</span>
                    <span id="stat-scouted" class="text-emerald-400 font-bold">0</span>
                </div>
            </div>

            <!-- Agent 2 -->
            <div id="card-verifier" class="glass-card rounded-xl p-3.5 border border-slate-800 transition hover:border-slate-700">
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Agent 2</span>
                    <span id="badge-verifier" class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">READY</span>
                </div>
                <h3 class="text-xs font-bold text-white mb-1">Verification Sentry</h3>
                <p class="text-[11px] text-slate-400 line-clamp-2">ZeroBounce deliverability scoring & Twilio carrier mobile vs landline audit.</p>
                <div class="mt-2 pt-2 border-t border-slate-800 text-[11px] text-slate-300 font-mono flex justify-between">
                    <span>Verified:</span>
                    <span id="stat-verified" class="text-emerald-400 font-bold">0</span>
                </div>
            </div>

            <!-- Agent 3 -->
            <div id="card-personalizer" class="glass-card rounded-xl p-3.5 border border-slate-800 transition hover:border-slate-700">
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Agent 3</span>
                    <span id="badge-personalizer" class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">READY</span>
                </div>
                <h3 class="text-xs font-bold text-white mb-1">ROI Personalizer</h3>
                <p class="text-[11px] text-slate-400 line-clamp-2">Calculates lost revenue ($3k-$6k/mo) & crafts 3-sentence non-salesy hooks.</p>
                <div class="mt-2 pt-2 border-t border-slate-800 text-[11px] text-slate-300 font-mono flex justify-between">
                    <span>Hooks:</span>
                    <span id="stat-hooks" class="text-emerald-400 font-bold">0</span>
                </div>
            </div>

            <!-- Agent 4 -->
            <div id="card-closer" class="glass-card rounded-xl p-3.5 border border-slate-800 transition hover:border-slate-700">
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Agent 4</span>
                    <span id="badge-closer" class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">READY</span>
                </div>
                <h3 class="text-xs font-bold text-white mb-1">Autonomous Closer</h3>
                <p class="text-[11px] text-slate-400 line-clamp-2">Dispatches outreach, classifies inbound objections, issues live test line.</p>
                <div class="mt-2 pt-2 border-t border-slate-800 text-[11px] text-slate-300 font-mono flex justify-between">
                    <span>Objections:</span>
                    <span id="stat-objections" class="text-emerald-400 font-bold">0</span>
                </div>
            </div>

            <!-- Agent 5 -->
            <div id="card-meta_review" class="glass-card rounded-xl p-3.5 border border-slate-800 transition hover:border-slate-700">
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Agent 5</span>
                    <span id="badge-meta_review" class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">READY</span>
                </div>
                <h3 class="text-xs font-bold text-white mb-1">Meta-Reviewer</h3>
                <p class="text-[11px] text-slate-400 line-clamp-2">Evolutionary loop: clusters objections, auto-refactors prompts for next batch.</p>
                <div class="mt-2 pt-2 border-t border-slate-800 text-[11px] text-slate-300 font-mono flex justify-between">
                    <span>Demos:</span>
                    <span id="stat-demos" class="text-emerald-400 font-bold">0</span>
                </div>
            </div>
        </section>

        <!-- KPI Metrics Ribbon -->
        <section class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
            <div class="glass-card rounded-xl p-3 border border-slate-800/80">
                <div class="text-[11px] text-slate-400 font-medium">Scouted Leads</div>
                <div id="metric-scouted" class="text-lg font-bold text-white mt-1">0</div>
            </div>
            <div class="glass-card rounded-xl p-3 border border-slate-800/80">
                <div class="text-[11px] text-slate-400 font-medium">Deliverability</div>
                <div id="metric-deliverability" class="text-lg font-bold text-emerald-400 mt-1">100%</div>
            </div>
            <div class="glass-card rounded-xl p-3 border border-slate-800/80">
                <div class="text-[11px] text-slate-400 font-medium">Outbound Sent</div>
                <div id="metric-outreach" class="text-lg font-bold text-white mt-1">0</div>
            </div>
            <div class="glass-card rounded-xl p-3 border border-slate-800/80">
                <div class="text-[11px] text-slate-400 font-medium">Replies Ingested</div>
                <div id="metric-replies" class="text-lg font-bold text-yellow-400 mt-1">0</div>
            </div>
            <div class="glass-card rounded-xl p-3 border border-slate-800/80">
                <div class="text-[11px] text-slate-400 font-medium">Positive Interest</div>
                <div id="metric-positives" class="text-lg font-bold text-emerald-400 mt-1">0</div>
            </div>
            <div class="glass-card rounded-xl p-3 border border-slate-800/80">
                <div class="text-[11px] text-slate-400 font-medium">Suppressed (Opt-Out)</div>
                <div id="metric-unsub" class="text-lg font-bold text-slate-400 mt-1">0</div>
            </div>
            <div class="glass-card rounded-xl p-3 border border-slate-800/80 col-span-2 sm:col-span-1">
                <div class="text-[11px] text-slate-400 font-medium">Demos Booked</div>
                <div id="metric-demos" class="text-lg font-bold text-cyan-400 mt-1">0</div>
            </div>
        </section>

        <!-- Tabs Navigation -->
        <section class="border-b border-slate-800 flex items-center space-x-6 text-sm">
            <button onclick="switchTab('pipeline')" id="tab-pipeline-btn" class="tab-btn active pb-3 transition">
                📋 Simulated Leads & Pipeline (<span id="leadsCountTab">0</span>)
            </button>
            <button onclick="switchTab('closerSandbox')" id="tab-closerSandbox-btn" class="tab-btn pb-3 transition text-slate-400 hover:text-slate-200">
                🎯 Agent 4 Closer Sandbox
            </button>
            <button onclick="switchTab('metaEvolution')" id="tab-metaEvolution-btn" class="tab-btn pb-3 transition text-slate-400 hover:text-slate-200">
                🧬 Agent 5 Evolutionary Loop
            </button>
            <button onclick="switchTab('eventLogs')" id="tab-eventLogs-btn" class="tab-btn pb-3 transition text-slate-400 hover:text-slate-200">
                ⚡ Real-Time Activity Log
            </button>
        </section>

        <!-- TAB 1: Leads & Outreach Pipeline -->
        <section id="tab-pipeline" class="space-y-4">
            <div class="glass-card rounded-xl border border-slate-800 overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-slate-800 text-xs">
                        <thead class="bg-slate-900/60 text-slate-400 font-medium text-left">
                            <tr>
                                <th class="py-3 px-4">Contractor / Trade</th>
                                <th class="py-3 px-4">Contact (Synthetic)</th>
                                <th class="py-3 px-4">Location</th>
                                <th class="py-3 px-4">Hygiene & Deliverability</th>
                                <th class="py-3 px-4">Est. Lost Rev</th>
                                <th class="py-3 px-4">Status</th>
                                <th class="py-3 px-4 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="leadsTableBody" class="divide-y divide-slate-800/60 font-mono text-slate-300">
                            <tr>
                                <td colspan="7" class="py-8 text-center text-slate-500 font-sans">
                                    No simulated leads generated yet. Click <strong>Run Full Batch</strong> or <strong>Step Agent</strong> above to begin.
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 2: Agent 4 Closer Sandbox -->
        <section id="tab-closerSandbox" class="hidden space-y-4">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Reply Form -->
                <div class="lg:col-span-5 glass-card rounded-xl p-5 border border-slate-800 space-y-4">
                    <div class="border-b border-slate-800 pb-3">
                        <h2 class="text-sm font-bold text-white flex items-center gap-2">
                            <span>🎯</span> Prospect Inbound Reply Simulator
                        </h2>
                        <p class="text-xs text-slate-400 mt-1">Test how Agent 4 autonomously classifies intent and overcomes objections in real-time.</p>
                    </div>

                    <!-- Target Lead Selector -->
                    <div>
                        <label class="block text-xs font-medium text-slate-300 mb-1">Target Lead to Reply As:</label>
                        <select id="sandboxLeadSelect" class="w-full bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg p-2 focus:border-emerald-500 focus:outline-none">
                            <option value="">-- Select a simulated lead --</option>
                        </select>
                    </div>

                    <!-- Preset Reply Selector -->
                    <div>
                        <label class="block text-xs font-medium text-slate-300 mb-1">Select Preset Archetype:</label>
                        <select id="sandboxPresetSelect" onchange="applyPresetText()" class="w-full bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg p-2 focus:border-emerald-500 focus:outline-none">
                            <option value="price_objection">Price Resistance: "How much does it cost? We're on a tight budget."</option>
                            <option value="complexity_objection">Complexity Objection: "Is setup complicated? We don't have IT."</option>
                            <option value="already_have_objection">Already Have: "We already have an answering service."</option>
                            <option value="positive_interest">Positive Interest: "Missed 3 calls on weekend. Can I test live demo?"</option>
                            <option value="unsubscribe">Unsubscribe: "Remove me from your list immediately."</option>
                            <option value="custom">Custom Message...</option>
                        </select>
                    </div>

                    <!-- Custom Message Input -->
                    <div>
                        <label class="block text-xs font-medium text-slate-300 mb-1">Prospect Message Text:</label>
                        <textarea id="sandboxMessageInput" rows="4" class="w-full bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg p-2.5 focus:border-emerald-500 focus:outline-none" placeholder="Type what the contractor responds..."></textarea>
                    </div>

                    <button onclick="submitSandboxReply()" id="sandboxSubmitBtn" class="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-emerald-900/50 transition">
                        Dispatch Inbound Reply & Trigger Closer
                    </button>
                </div>

                <!-- Closer Output Display -->
                <div class="lg:col-span-7 glass-card rounded-xl p-5 border border-slate-800 space-y-4">
                    <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
                        <div>
                            <h2 class="text-sm font-bold text-white flex items-center gap-2">
                                <span>🤖</span> Agent 4 Decision & Output
                            </h2>
                            <p class="text-xs text-slate-400 mt-1">Autonomous reasoning, intent classifier confidence, and synthesized response.</p>
                        </div>
                        <span id="closerStatusBadge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">IDLE</span>
                    </div>

                    <div id="closerEmptyState" class="py-16 text-center text-slate-500 text-xs font-sans">
                        Select a lead and trigger an incoming reply on the left to inspect Agent 4's closing logic.
                    </div>

                    <div id="closerResultCard" class="hidden space-y-4">
                        <!-- Intent & Confidence -->
                        <div class="grid grid-cols-2 gap-3">
                            <div class="bg-slate-900/80 rounded-lg p-3 border border-slate-800">
                                <div class="text-[11px] text-slate-400 font-medium">Detected Intent</div>
                                <div id="closerIntentVal" class="text-sm font-bold text-emerald-400 font-mono mt-1">-</div>
                            </div>
                            <div class="bg-slate-900/80 rounded-lg p-3 border border-slate-800">
                                <div class="text-[11px] text-slate-400 font-medium">Classification Confidence</div>
                                <div id="closerConfidenceVal" class="text-sm font-bold text-cyan-400 font-mono mt-1">0%</div>
                            </div>
                        </div>

                        <!-- Reasoning -->
                        <div class="bg-slate-900/80 rounded-lg p-3.5 border border-slate-800 space-y-1">
                            <div class="text-[11px] text-slate-400 font-medium">Agent Reasoning:</div>
                            <p id="closerReasoningVal" class="text-xs text-slate-300 leading-relaxed">-</p>
                        </div>

                        <!-- Action Taken -->
                        <div class="bg-slate-900/80 rounded-lg p-3.5 border border-slate-800 flex items-center justify-between">
                            <span class="text-xs text-slate-400 font-medium">Autonomous Action Taken:</span>
                            <span id="closerActionVal" class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-yellow-400 border border-slate-700">-</span>
                        </div>

                        <!-- Response Sent -->
                        <div class="bg-emerald-950/30 rounded-lg p-3.5 border border-emerald-500/30 space-y-1.5">
                            <div class="text-[11px] text-emerald-400 font-semibold flex items-center justify-between">
                                <span>Autonomous Response Dispatched to Prospect:</span>
                                <span class="text-[10px] text-slate-400 font-mono">Channel: EMAIL</span>
                            </div>
                            <p id="closerResponseMsgVal" class="text-xs text-slate-200 leading-relaxed font-sans bg-slate-900/90 p-3 rounded border border-slate-800 whitespace-pre-wrap">-</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: Agent 5 Evolutionary Loop -->
        <section id="tab-metaEvolution" class="hidden space-y-4">
            <div class="glass-card rounded-xl p-5 border border-slate-800 space-y-5">
                <div class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
                    <div>
                        <h2 class="text-sm font-bold text-white flex items-center gap-2">
                            <span>🧬</span> Agent 5: Evolutionary Meta-Reviewer
                        </h2>
                        <p class="text-xs text-slate-400 mt-1">Continuous conversion rate optimization (CRO) loop refactoring prompt parameters and hooks.</p>
                    </div>
                    <button onclick="triggerMetaReview()" id="metaReviewBtn" class="px-3 py-1.5 text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition shadow">
                        ⚡ Run Evolutionary Optimization Now
                    </button>
                </div>

                <div id="metaReviewEmptyState" class="py-12 text-center text-slate-500 text-xs">
                    No evolutionary optimization run recorded for the current batch yet. Click the button above to execute Agent 5.
                </div>

                <div id="metaReviewContent" class="hidden space-y-5">
                    <!-- Analysis Summary -->
                    <div class="bg-slate-900/80 rounded-xl p-4 border border-slate-800">
                        <div class="text-xs font-semibold text-slate-300 mb-1">Batch Performance Analysis:</div>
                        <p id="metaAnalysisSummary" class="text-xs text-slate-400 leading-relaxed">-</p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <!-- Weak Patterns -->
                        <div class="bg-red-950/20 rounded-xl p-4 border border-red-500/20 space-y-2">
                            <div class="text-xs font-bold text-red-400 flex items-center gap-1.5">
                                <span>⚠️</span> Isolated Weak Patterns & Friction Points
                            </div>
                            <ul id="metaWeakPatterns" class="text-xs text-slate-300 space-y-1.5 list-disc list-inside"></ul>
                        </div>

                        <!-- Expected Gain -->
                        <div class="bg-emerald-950/20 rounded-xl p-4 border border-emerald-500/20 space-y-2">
                            <div class="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                                <span>📈</span> Projected Conversion Gain
                            </div>
                            <div id="metaConversionGain" class="text-sm font-bold text-emerald-300 font-mono mt-1">-</div>
                            <p class="text-[11px] text-slate-400">Calculated velocity improvement for the next scheduled campaign batch.</p>
                        </div>
                    </div>

                    <!-- Auto-Refactored Subject Lines -->
                    <div class="bg-slate-900/80 rounded-xl p-4 border border-slate-800 space-y-2">
                        <div class="text-xs font-bold text-yellow-400 flex items-center gap-1.5">
                            <span>✍️</span> Auto-Refactored Subject Lines (for next batch)
                        </div>
                        <div id="metaSubjectLines" class="grid grid-cols-1 md:grid-cols-3 gap-2"></div>
                    </div>

                    <!-- Adjusted Hook Angles -->
                    <div class="bg-slate-900/80 rounded-xl p-4 border border-slate-800 space-y-2">
                        <div class="text-xs font-bold text-cyan-400 flex items-center gap-1.5">
                            <span>🎯</span> Adjusted Copy Angles & Hooks
                        </div>
                        <div id="metaHookAngles" class="space-y-1.5 text-xs text-slate-300"></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 4: Real-Time Event Log Stream -->
        <section id="tab-eventLogs" class="hidden space-y-4">
            <div class="glass-card rounded-xl p-4 border border-slate-800 space-y-3">
                <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                    <h2 class="text-xs font-bold text-white flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 pulse-dot"></span>
                        Swarm Execution Event Feed
                    </h2>
                    <div class="flex items-center space-x-2">
                        <button onclick="refreshLogs()" class="text-xs text-slate-400 hover:text-white px-2 py-1 rounded bg-slate-800">Refresh</button>
                    </div>
                </div>

                <div id="eventLogContainer" class="font-mono text-[11px] space-y-1.5 max-h-[450px] overflow-y-auto pr-2">
                    <div class="text-slate-500 text-center py-8">Awaiting simulation events...</div>
                </div>
            </div>
        </section>

    </main>

    <!-- Lead Detail Modal / Drawer -->
    <div id="leadModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="glass-card rounded-2xl max-w-2xl w-full max-h-[90vh] flex flex-col border border-slate-700 shadow-2xl overflow-hidden">
            <!-- Modal Header -->
            <div class="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/80">
                <div>
                    <h3 id="modalCompanyName" class="text-sm font-bold text-white">-</h3>
                    <p id="modalSubTitle" class="text-xs text-slate-400 font-mono mt-0.5">-</p>
                </div>
                <button onclick="closeModal()" class="text-slate-400 hover:text-white text-lg px-2">✕</button>
            </div>

            <!-- Modal Body -->
            <div id="modalBody" class="p-5 overflow-y-auto space-y-4 text-xs">
                <!-- Content injected via JS -->
            </div>

            <!-- Modal Footer -->
            <div class="p-3 border-t border-slate-800 bg-slate-900/60 flex justify-end">
                <button onclick="closeModal()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs">Close</button>
            </div>
        </div>
    </div>

    <!-- JavaScript Controller -->
    <script>
        const state = {
            currentTab: 'pipeline',
            leads: [],
            metrics: {},
            simState: {},
            selectedLeadId: null
        };

        const PRESET_MESSAGES = {
            price_objection: "Sounds interesting, but how much does this service cost per month? We are a small crew on a tight budget.",
            complexity_objection: "How complicated is the setup? We don't have an IT team to manage this.",
            already_have_objection: "We already have an answering service that takes messages for us at night.",
            positive_interest: "Saw your email about our missed calls last weekend. Can I call the demo number right now from my cell?",
            unsubscribe: "Please remove me from your mailing list immediately."
        };

        function switchTab(tabId) {
            state.currentTab = tabId;
            ['pipeline', 'closerSandbox', 'metaEvolution', 'eventLogs'].forEach(t => {
                const el = document.getElementById(`tab-${t}`);
                const btn = document.getElementById(`tab-${t}-btn`);
                if (t === tabId) {
                    el.classList.remove('hidden');
                    btn.classList.add('active', 'text-emerald-400');
                    btn.classList.remove('text-slate-400');
                } else {
                    el.classList.add('hidden');
                    btn.classList.remove('active', 'text-emerald-400');
                    btn.classList.add('text-slate-400');
                }
            });
            if (tabId === 'closerSandbox') populateSandboxLeads();
        }

        async function fetchState() {
            try {
                const res = await fetch('/api/simulation/state');
                const data = await res.json();
                state.simState = data;
                updateMetricsUI(data.metrics);
                updateCurrentStepUI(data.current_step_name, data.current_step_index, data.total_steps);
                renderLogs(data.recent_logs);
                if (data.latest_refinement) renderMetaRefinement(data.latest_refinement);
            } catch (err) {
                console.error("Failed to fetch state:", err);
            }
        }

        async function fetchLeads() {
            try {
                const res = await fetch('/api/simulation/leads');
                const leads = await res.json();
                state.leads = leads;
                renderLeadsTable(leads);
                document.getElementById('leadsCountTab').innerText = leads.length;
            } catch (err) {
                console.error("Failed to fetch leads:", err);
            }
        }

        function updateMetricsUI(m) {
            if (!m) return;
            document.getElementById('metric-scouted').innerText = m.total_leads_scouted;
            document.getElementById('stat-scouted').innerText = m.total_leads_scouted;

            const delRate = m.total_leads_scouted > 0 ? Math.round((m.verified_leads / m.total_leads_scouted) * 100) : 100;
            document.getElementById('metric-deliverability').innerText = `${delRate}%`;
            document.getElementById('stat-verified').innerText = m.verified_leads;

            document.getElementById('metric-outreach').innerText = m.outreach_sent;
            document.getElementById('stat-hooks').innerText = m.outreach_sent;

            document.getElementById('metric-replies').innerText = m.replies_received;
            document.getElementById('metric-positives').innerText = m.positive_replies;
            document.getElementById('metric-unsub').innerText = m.unsubscribes;
            document.getElementById('metric-demos').innerText = m.demos_booked;
            document.getElementById('stat-objections').innerText = m.objections_handled;
            document.getElementById('stat-demos').innerText = m.demos_booked;
        }

        function updateCurrentStepUI(stepName, stepIndex, total) {
            document.getElementById('currentStepBadge').innerText = stepName || 'idle';
            document.getElementById('batchProgressText').innerText = `(Step ${stepIndex}/${total})`;

            // Update 5 Agent Cards badges
            const agentCards = ['scout', 'verifier', 'personalizer', 'closer', 'meta_review'];
            agentCards.forEach((agent, idx) => {
                const badge = document.getElementById(`badge-${agent}`);
                const card = document.getElementById(`card-${agent}`);
                if (idx < stepIndex) {
                    badge.innerText = 'DONE';
                    badge.className = 'text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-500/30';
                    card.classList.remove('border-emerald-500', 'bg-emerald-950/10');
                } else if (idx === stepIndex) {
                    badge.innerText = 'ACTIVE';
                    badge.className = 'text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 pulse-dot';
                    card.classList.add('border-emerald-500/60', 'bg-emerald-950/10');
                } else {
                    badge.innerText = 'WAITING';
                    badge.className = 'text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-500';
                    card.classList.remove('border-emerald-500/60', 'bg-emerald-950/10');
                }
            });
        }

        function renderLeadsTable(leads) {
            const tbody = document.getElementById('leadsTableBody');
            if (!leads || leads.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" class="py-8 text-center text-slate-500 font-sans">No simulated leads in database. Click <strong>Run Full Batch</strong> to generate synthetic test leads.</td></tr>`;
                return;
            }

            tbody.innerHTML = leads.map(l => {
                const statusColor = l.status === 'SUPPRESSED' ? 'text-red-400 bg-red-950/40 border-red-500/30' :
                                    l.status.includes('VERIFIED_PASSED') || l.status === 'HOOK_GENERATED' ? 'text-emerald-400 bg-emerald-950/40 border-emerald-500/30' :
                                    l.status.includes('DISCARDED') ? 'text-amber-400 bg-amber-950/40 border-amber-500/30' : 'text-slate-400 bg-slate-800 border-slate-700';

                const score = l.email_deliverability_score ? Math.round(l.email_deliverability_score * 100) : 95;
                const scoreBadge = score >= 80 ? `<span class="text-emerald-400">${score}% (${l.phone_type || 'mobile'})</span>` : `<span class="text-amber-400">${score}% (discarded)</span>`;
                const lostRev = l.lost_revenue ? `<span class="text-rose-400 font-bold">$${Math.round(l.lost_revenue).toLocaleString()}/mo</span>` : `<span class="text-slate-500">-</span>`;

                return `
                    <tr class="hover:bg-slate-800/40 transition">
                        <td class="py-3 px-4 font-medium text-white">
                            <div>${l.company_name}</div>
                            <div class="text-[10px] text-slate-500">${l.niche} • ${l.owner_name}</div>
                        </td>
                        <td class="py-3 px-4 text-slate-400">
                            <div>${l.email}</div>
                            <div class="text-[10px] text-slate-500">${l.phone}</div>
                        </td>
                        <td class="py-3 px-4 text-slate-400">${l.city}, ${l.state}</td>
                        <td class="py-3 px-4">${scoreBadge}</td>
                        <td class="py-3 px-4 font-mono">${lostRev}</td>
                        <td class="py-3 px-4">
                            <span class="px-2 py-0.5 rounded text-[10px] font-semibold border ${statusColor}">
                                ${l.status}
                            </span>
                        </td>
                        <td class="py-3 px-4 text-right">
                            <button onclick="viewLeadDetail('${l.id}')" class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-[10px]">
                                Inspect
                            </button>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function renderLogs(logs) {
            const container = document.getElementById('eventLogContainer');
            if (!logs || logs.length === 0) return;
            container.innerHTML = logs.map(l => {
                const color = l.level === 'success' ? 'text-emerald-400' : l.level === 'warning' ? 'text-amber-400' : 'text-slate-300';
                return `<div class="leading-relaxed border-b border-slate-900/60 pb-1">
                    <span class="text-slate-500">[${l.timestamp}]</span>
                    <span class="text-cyan-400 font-semibold">[${l.source}]</span>
                    <span class="${color}">${l.message}</span>
                </div>`;
            }).join('');
            container.scrollTop = container.scrollHeight;
        }

        async function stepSimulation() {
            const btn = document.getElementById('stepBtn');
            btn.disabled = true;
            btn.innerText = 'Stepping...';
            try {
                const niche = document.getElementById('simNiche').value;
                const [city, stateCode] = document.getElementById('simCity').value.split(',');
                const count = parseInt(document.getElementById('simCount').value);
                const scenario = document.getElementById('simScenario').value;

                await fetch('/api/simulation/step', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ niche, city, state: stateCode, count, scenario })
                });

                await fetchState();
                await fetchLeads();
            } catch (err) {
                alert("Step failed: " + err.message);
            } finally {
                btn.disabled = false;
                btn.innerText = '⏭ Step Agent';
            }
        }

        async function runFullBatch() {
            const btn = document.getElementById('runBatchBtn');
            btn.disabled = true;
            btn.innerText = 'Executing 5 Agents...';
            try {
                const niche = document.getElementById('simNiche').value;
                const [city, stateCode] = document.getElementById('simCity').value.split(',');
                const count = parseInt(document.getElementById('simCount').value);
                const scenario = document.getElementById('simScenario').value;

                await fetch('/api/simulation/run-batch', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ niche, city, state: stateCode, count, scenario })
                });

                await fetchState();
                await fetchLeads();
            } catch (err) {
                alert("Batch execution failed: " + err.message);
            } finally {
                btn.disabled = false;
                btn.innerText = '▶ Run Full Batch';
            }
        }

        async function resetSimulation() {
            if (!confirm("Reset database and simulation pipeline?")) return;
            await fetch('/api/simulation/reset', { method: 'POST' });
            await fetchState();
            await fetchLeads();
        }

        function populateSandboxLeads() {
            const select = document.getElementById('sandboxLeadSelect');
            select.innerHTML = '<option value="">-- Select a simulated lead --</option>' +
                state.leads.map(l => `<option value="${l.id}">${l.company_name} (${l.niche})</option>`).join('');
            applyPresetText();
        }

        function applyPresetText() {
            const preset = document.getElementById('sandboxPresetSelect').value;
            const input = document.getElementById('sandboxMessageInput');
            if (PRESET_MESSAGES[preset]) {
                input.value = PRESET_MESSAGES[preset];
            }
        }

        async function submitSandboxReply() {
            const leadId = document.getElementById('sandboxLeadSelect').value;
            if (!leadId) {
                alert("Please select a simulated lead from the dropdown.");
                return;
            }
            const scenario = document.getElementById('sandboxPresetSelect').value;
            const customText = document.getElementById('sandboxMessageInput').value;

            const btn = document.getElementById('sandboxSubmitBtn');
            btn.disabled = true;
            btn.innerText = 'Agent 4 Classifying...';

            try {
                const res = await fetch('/api/simulation/closer-reply', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ lead_id: leadId, scenario, custom_text: customText })
                });
                const data = await res.json();
                renderCloserDecision(data.closer_response);
                await fetchState();
                await fetchLeads();
            } catch (err) {
                alert("Closer reply failed: " + err.message);
            } finally {
                btn.disabled = false;
                btn.innerText = 'Dispatch Inbound Reply & Trigger Closer';
            }
        }

        function renderCloserDecision(c) {
            document.getElementById('closerEmptyState').classList.add('hidden');
            document.getElementById('closerResultCard').classList.remove('hidden');
            document.getElementById('closerStatusBadge').innerText = 'COMPLETED';
            document.getElementById('closerStatusBadge').className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-500/30';

            document.getElementById('closerIntentVal').innerText = c.detected_intent;
            document.getElementById('closerConfidenceVal').innerText = `${Math.round(c.confidence * 100)}%`;
            document.getElementById('closerReasoningVal').innerText = c.reasoning;
            document.getElementById('closerActionVal').innerText = c.action_taken;
            document.getElementById('closerResponseMsgVal').innerText = c.response_message;
        }

        async function triggerMetaReview() {
            const btn = document.getElementById('metaReviewBtn');
            btn.disabled = true;
            btn.innerText = 'Optimizing Prompts...';
            try {
                const res = await fetch('/api/simulation/meta-review', { method: 'POST' });
                const refinement = await res.json();
                renderMetaRefinement(refinement);
                await fetchState();
            } catch (err) {
                alert("Meta review failed: " + err.message);
            } finally {
                btn.disabled = false;
                btn.innerText = '⚡ Run Evolutionary Optimization Now';
            }
        }

        function renderMetaRefinement(r) {
            if (!r) return;
            document.getElementById('metaReviewEmptyState').classList.add('hidden');
            document.getElementById('metaReviewContent').classList.remove('hidden');

            document.getElementById('metaAnalysisSummary').innerText = r.analysis_summary;
            document.getElementById('metaConversionGain').innerText = r.expected_conversion_gain;

            document.getElementById('metaWeakPatterns').innerHTML = (r.weak_patterns_detected || []).map(p => `<li>${p}</li>`).join('');
            document.getElementById('metaSubjectLines').innerHTML = (r.improved_subject_lines || []).map(s => 
                `<div class="p-2 rounded bg-slate-950 border border-slate-800 text-yellow-300 font-mono text-[11px]">${s}</div>`
            ).join('');
            document.getElementById('metaHookAngles').innerHTML = (r.adjusted_hook_angles || []).map(a => 
                `<div class="p-2 rounded bg-slate-950 border border-slate-800 text-cyan-300 text-[11px]">→ ${a}</div>`
            ).join('');
        }

        async function viewLeadDetail(leadId) {
            try {
                const res = await fetch(`/api/simulation/leads/${leadId}`);
                const l = await res.json();
                
                document.getElementById('modalCompanyName').innerText = l.company_name;
                document.getElementById('modalSubTitle').innerText = `${l.id} • ${l.niche} • ${l.city}, ${l.state}`;

                let bodyHtml = `
                    <div class="grid grid-cols-2 gap-3 bg-slate-900/90 p-3 rounded-lg border border-slate-800">
                        <div><span class="text-slate-500">Contact:</span> ${l.owner_name} (${l.email})</div>
                        <div><span class="text-slate-500">Phone:</span> ${l.phone}</div>
                        <div><span class="text-slate-500">24/7 Claim:</span> ${l.has_24_7_service_claim ? 'Yes' : 'Standard'}</div>
                        <div><span class="text-slate-500">Status:</span> ${l.status}</div>
                    </div>
                `;

                // Verification
                if (l.verification) {
                    bodyHtml += `
                        <div class="bg-slate-900/90 p-3 rounded-lg border border-slate-800 space-y-1">
                            <div class="font-bold text-slate-200">Verification & Hygiene Audit:</div>
                            <div class="text-slate-400">Deliverability Score: <strong class="text-emerald-400">${Math.round(l.verification.deliverability_score*100)}%</strong> | Carrier Line: <strong class="text-yellow-400">${l.verification.phone_type}</strong></div>
                            <div class="text-slate-500 text-[11px]">Audit Reason: ${l.verification.reason}</div>
                        </div>
                    `;
                }

                // Reviews
                if (l.reviews && l.reviews.length > 0) {
                    bodyHtml += `
                        <div class="space-y-1.5">
                            <div class="font-bold text-slate-200">Discovered Customer Reviews:</div>
                            ${l.reviews.map(r => `
                                <div class="bg-slate-950 p-2.5 rounded border border-slate-800 text-[11px]">
                                    <div class="text-amber-400 font-bold">${'★'.repeat(r.rating)}${'☆'.repeat(5-r.rating)} - ${r.author}</div>
                                    <div class="text-slate-300 mt-1">${r.text}</div>
                                </div>
                            `).join('')}
                        </div>
                    `;
                }

                // Hook
                if (l.hook) {
                    bodyHtml += `
                        <div class="bg-emerald-950/20 p-3.5 rounded-lg border border-emerald-500/30 space-y-2">
                            <div class="font-bold text-emerald-400">Agent 3 Synthesized 3-Sentence ROI Hook:</div>
                            <div class="text-slate-400 text-[11px]">Subject: <span class="text-yellow-300 font-mono">${l.hook.subject_line}</span></div>
                            <div class="p-2.5 rounded bg-slate-900 text-slate-200 leading-relaxed font-sans">${l.hook.email_body}</div>
                            <div class="text-xs text-rose-400 font-mono font-bold">Estimated Lost Revenue: $${Math.round(l.hook.lost_revenue).toLocaleString()}/month</div>
                        </div>
                    `;
                }

                // Conversations
                if (l.conversations && l.conversations.length > 0) {
                    bodyHtml += `
                        <div class="space-y-2">
                            <div class="font-bold text-slate-200">Conversation & Closer Thread:</div>
                            ${l.conversations.map(c => `
                                <div class="p-2.5 rounded text-[11px] border ${c.direction === 'OUTBOUND' ? 'bg-slate-900 border-slate-800 text-slate-200 ml-4' : 'bg-amber-950/20 border-amber-500/20 text-amber-200 mr-4'}">
                                    <div class="text-[10px] font-bold uppercase ${c.direction === 'OUTBOUND' ? 'text-emerald-400' : 'text-amber-400'}">${c.direction} (${c.channel}) - ${c.timestamp}</div>
                                    <div class="mt-1">${c.message_content}</div>
                                    ${c.detected_intent ? `<div class="text-[10px] text-cyan-400 mt-1 font-mono">Intent: ${c.detected_intent} | Action: ${c.action_taken}</div>` : ''}
                                </div>
                            `).join('')}
                        </div>
                    `;
                }

                document.getElementById('modalBody').innerHTML = bodyHtml;
                document.getElementById('leadModal').classList.remove('hidden');
            } catch (err) {
                alert("Failed to load lead details: " + err.message);
            }
        }

        function closeModal() {
            document.getElementById('leadModal').classList.add('hidden');
        }

        async function refreshLogs() {
            try {
                const res = await fetch('/api/simulation/logs');
                const logs = await res.json();
                renderLogs(logs);
            } catch (err) {}
        }

        // Initialize on load
        window.addEventListener('DOMContentLoaded', () => {
            fetchState();
            fetchLeads();
            // Polling interval for live updates
            setInterval(fetchState, 4000);
        });
    </script>
</body>
</html>
"""
