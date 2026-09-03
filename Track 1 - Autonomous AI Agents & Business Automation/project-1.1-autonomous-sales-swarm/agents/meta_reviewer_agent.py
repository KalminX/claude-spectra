import logging
from typing import Optional, List
from core.schemas import PromptRefinement, CampaignMetrics
from core.database import SwarmDatabase
from core.llm import UniversalLLM

logger = logging.getLogger("Agent5_MetaReviewer")

class MetaReviewerAgent:
    """
    AGENT 5: Meta-Reviewer & Evolutionary Feedback Loop
    Analyzes conversion metrics (open rates, reply patterns, objection clusters, drop-offs).
    Dynamically refactors prompt parameters, subject lines, and hook angles to continuously
    increase reply and booking velocity over time.
    """

    def __init__(self, db: SwarmDatabase, llm: Optional[UniversalLLM] = None):
        self.db = db
        self.llm = llm or UniversalLLM()

    def evaluate_and_optimize(self, batch_id: str = "batch_001") -> PromptRefinement:
        logger.info(f"[Agent 5: Meta-Reviewer] Analyzing performance metrics for batch: {batch_id}...")
        
        metrics = self.db.get_metrics()
        
        system_prompt = (
            "You are an elite AI conversion rate optimization (CRO) specialist and prompt engineer. "
            "You analyze sales outbound conversion data, identify friction points, and refactor prompts "
            "and subject lines to maximize prospect replies and booked meetings."
        )

        prompt = f"""
        Current Campaign Performance Metrics:
        - Total Leads Scouted: {metrics.total_leads_scouted}
        - Verified Deliverable: {metrics.verified_leads}
        - Outbound Touches Dispatched: {metrics.outreach_sent}
        - Replies Received: {metrics.replies_received}
        - Positive Interest Replies: {metrics.positive_replies}
        - Objections Handled: {metrics.objections_handled}
        - Unsubscribes: {metrics.unsubscribes}
        - Demos Booked / Triggered: {metrics.demos_booked}

        Task:
        1. Identify 2-3 weak patterns or friction points in the outreach.
        2. Generate 3 improved, ultra-high-converting cold email subject lines (short, casual, lower-case).
        3. Recommend 2 adjusted hook angles to decrease price resistance.
        4. State the expected conversion gain.
        """

        sandbox_data = {
            "batch_id": batch_id,
            "analysis_summary": (
                f"Evaluated {metrics.outreach_sent} outbound messages with {metrics.replies_received} replies. "
                f"Conversion to demo inquiry is {((metrics.positive_replies / max(metrics.replies_received, 1)) * 100):.1f}%. "
                f"Primary friction point is initial price curiosity and after-hours emergency validation."
            ),
            "weak_patterns_detected": [
                "Subject lines referencing company name too formally trigger promotional tab filtering.",
                "Quotes citing large revenue loss ($6k+) can trigger skepticism without immediate proof.",
                "Prospects want proof of natural voice quality before speaking to any salesperson."
            ],
            "improved_subject_lines": [
                "missed call on sunday?",
                "quick question re: after-hours calls",
                "saw that review about weekend voicemail"
            ],
            "adjusted_hook_angles": [
                "Lead with specific weekend emergency call recovery rather than annual estimates.",
                "Shift CTA to dial the live demo number directly on speakerphone in 30 seconds."
            ],
            "expected_conversion_gain": "+28% reply velocity and +15% direct demo phone dials."
        }

        refinement = self.llm.generate_structured(
            prompt=prompt,
            schema=PromptRefinement,
            system_instruction=system_prompt,
            sandbox_fallback_data=sandbox_data
        )

        refinement.batch_id = batch_id
        logger.info(f"[Agent 5: Meta-Reviewer] Optimization complete: {refinement.expected_conversion_gain}")
        return refinement
