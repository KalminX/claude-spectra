import logging
from typing import List, Optional
from core.schemas import RawLead, PersonalizedHook, TradeNiche
from core.database import SwarmDatabase
from core.llm import UniversalLLM
from config import settings

logger = logging.getLogger("Agent3_Personalizer")

class HookPersonalizerAgent:
    """
    AGENT 3: Context & Personalization Engine
    Parses reviews, website context, and missed-call signals.
    Computes custom ROI metrics (estimated monthly lost revenue) and crafts
    a high-converting, personalized 3-sentence cold email and SMS hook.
    """

    def __init__(self, db: SwarmDatabase, llm: Optional[UniversalLLM] = None):
        self.db = db
        self.llm = llm or UniversalLLM()

    def generate_hook(self, lead: RawLead) -> PersonalizedHook:
        logger.info(f"[Agent 3: Hook Engine] Synthesizing custom ROI hook for: {lead.company_name}...")

        # 1. Extract reviews that cite missed calls or emergency frustration
        missed_call_reviews = [r for r in lead.reviews if r.mentions_missed_call or r.rating <= 2]
        primary_complaint = (
            missed_call_reviews[0].text 
            if missed_call_reviews 
            else f"Customers calling for emergency {lead.niche.value} after hours receiving voicemail."
        )

        # 2. Compute niche-specific ticket economics
        ticket_map = {
            TradeNiche.PLUMBING: 550.0,
            TradeNiche.HVAC: 850.0,
            TradeNiche.ELECTRICAL: 450.0,
            TradeNiche.ROOFING: 1800.0,
        }
        avg_ticket = ticket_map.get(lead.niche, 500.0)
        est_missed = 14 if lead.has_24_7_service_claim else 8
        lost_revenue = est_missed * avg_ticket * 0.40  # assuming 40% close rate on captured calls

        # 3. Formulate Prompt for LLM (Claude 3.5 Sonnet / Gemini 2.0 Flash)
        system_prompt = (
            "You are an elite B2B cold outreach copywriter specializing in home-service contractors "
            "(Plumbing, HVAC, Roofing). Write ultra-personalized, non-salesy, direct 3-sentence cold emails. "
            "Never use fluff or jargon like 'I hope this finds you well' or 'synergy'. Get straight to the point."
        )

        prompt = f"""
        Company Name: {lead.company_name}
        Owner Name: {lead.owner_name}
        Trade / Niche: {lead.niche.value}
        Location: {lead.city}, {lead.state}
        24/7 Claim on Website: {lead.has_24_7_service_claim}
        Specific Customer Review Found: "{primary_complaint}"
        Estimated Monthly Lost Revenue from Missed Calls: ${lost_revenue:,.0f}
        Demo Phone Line: {settings.DEMO_PHONE_NUMBER}

        Requirements:
        1. Subject Line: Punchy, curiosity-inducing, lower-case style (e.g. "quick question re: after-hours calls in {lead.city}").
        2. Email Body: EXACTLY 3 sentences:
           - Sentence 1: Reference their specific customer review or after-hours availability.
           - Sentence 2: Mention the estimated ${lost_revenue:,.0f}/mo in lost emergency jobs that slip to competitors.
           - Sentence 3: Low-friction CTA inviting them to dial our live test number ({settings.DEMO_PHONE_NUMBER}) to hear how an AI receptionist answers their phones.
        3. SMS Body: Under 160 characters, direct and personalized.
        """

        # Deterministic sandbox fixture for $0 offline execution
        sandbox_fallback = {
            "lead_id": lead.id,
            "company_name": lead.company_name,
            "estimated_monthly_missed_calls": est_missed,
            "estimated_ticket_value": avg_ticket,
            "estimated_monthly_lost_revenue": lost_revenue,
            "specific_pain_point": primary_complaint[:120] + "...",
            "subject_line": f"missed call on Sunday ({lead.company_name})",
            "email_body_3_sentences": (
                f"Hi {lead.owner_name}, saw a recent note from a customer in {lead.city} who called after hours with an emergency and ended up going to a competitor because nobody picked up. "
                f"For a {lead.niche.value} contractor your size, missing just 3 after-hours calls a week costs roughly ${lost_revenue:,.0f} every month in lost high-margin jobs. "
                f"We built an AI receptionist specifically for {lead.niche.value} crews that answers 24/7 in 2 rings—worth dialing our live demo at {settings.DEMO_PHONE_NUMBER} to hear how it sounds?"
            ),
            "sms_body": f"Hey {lead.owner_name}, quick question about after-hours call overflow for {lead.company_name}. Recovering ~$3k/mo in missed emergency calls for local crews. Worth a chat?"
        }

        hook = self.llm.generate_structured(
            prompt=prompt,
            schema=PersonalizedHook,
            system_instruction=system_prompt,
            sandbox_fallback_data=sandbox_fallback
        )

        # Ensure IDs match
        hook.lead_id = lead.id
        hook.company_name = lead.company_name

        self.db.save_hook(hook)
        logger.info(f"[Agent 3: Hook Engine] Hook generated for {lead.company_name}. Estimated lost revenue: ${hook.estimated_monthly_lost_revenue:,.0f}/mo")
        return hook

    def generate_hooks_for_leads(self, leads: List[RawLead]) -> List[PersonalizedHook]:
        return [self.generate_hook(lead) for lead in leads]
