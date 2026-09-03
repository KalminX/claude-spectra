import random
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from core.schemas import (
    RawLead, 
    TradeNiche, 
    ReviewItem, 
    InboundReply, 
    ReplyIntentType
)
from core.database import SwarmDatabase
from config import settings

# Fictional company components for synthetic lead generation
SYNTHETIC_ADJECTIVES = ["Apex", "Titan", "ProFlow", "Premier", "Rapid", "BlueFlame", "Summit", "Reliable", "Guardian", "BreezeAir", "Thunderbolt", "Metro", "LoneStar", "Pacific", "AllStar"]
SYNTHETIC_NOUNS = {
    TradeNiche.PLUMBING: ["Plumbing & Rooter", "Emergency Drain Services", "Piping Solutions", "Plumbing Pros", "Rooter Masters"],
    TradeNiche.HVAC: ["Heating & Air Solutions", "HVAC Specialists", "Climate Control", "Air Comfort Systems", "Thermal Tech"],
    TradeNiche.ROOFING: ["Roofing & Restoration", "Peak Roofing Systems", "Shield Roofing", "Apex Roofing Specialists", "Precision Roofers"],
    TradeNiche.ELECTRICAL: ["Electric & Solar", "PowerGrid Solutions", "VoltMaster Electrical", "Current Dynamics", "Circuit Masters"]
}
SYNTHETIC_FIRST_NAMES = ["Marcus", "Tyler", "Jack", "Greg", "Sarah", "Elena", "Dan", "Robert", "Amanda", "David", "Kevin", "Rachel", "Carlos", "Jason", "Brian"]
SYNTHETIC_LAST_NAMES = ["Vance", "Ross", "Callahan", "Novak", "Jenkins", "Gomez", "Stevens", "Miller", "Wright", "Chen", "Reynolds", "Cooper", "Sanchez", "Baker", "Foster"]

SYNTHETIC_CITIES = [
    ("Dallas", "TX"),
    ("Austin", "TX"),
    ("Phoenix", "AZ"),
    ("Denver", "CO"),
    ("Orlando", "FL"),
    ("Atlanta", "GA"),
    ("Charlotte", "NC"),
    ("Nashville", "TN")
]

SYNTHETIC_REVIEWS_TEMPLATES = [
    {
        "rating": 1,
        "mentions_missed_call": True,
        "text": "Called on a Sunday evening with an emergency burst pipe flooding our kitchen. The phone just rang and rang until it hit a generic voicemail. Ended up having to call another company that answered immediately."
    },
    {
        "rating": 1,
        "mentions_missed_call": True,
        "text": "It was 105 degrees on Saturday when our A/C unit stopped cooling. Called three times between 1pm and 4pm. No one answered and the voicemail box was full. Lost a loyal customer today."
    },
    {
        "rating": 1,
        "mentions_missed_call": True,
        "text": "Our breaker tripped during the thunderstorm. Tried reaching their 24/7 emergency dispatch line at 9pm and nobody picked up. Waited 2 hours for a callback that never arrived."
    },
    {
        "rating": 2,
        "mentions_missed_call": True,
        "text": "Technicians do good work once they actually arrive, but getting anyone to answer their main office phone on weekends is nearly impossible."
    },
    {
        "rating": 5,
        "mentions_missed_call": False,
        "text": "Owner came out personally to inspect the installation. Very fair pricing and transparent explanation of the repair costs."
    },
    {
        "rating": 4,
        "mentions_missed_call": False,
        "text": "Prompt and clean service during regular weekday hours. Would recommend to neighbors."
    }
]

class SyntheticLeadGenerator:
    """
    Generates 100% synthetic, realistic trade contractor lead fixtures.
    - Zero real PII
    - Safe RFC test domains (@simulated.test, @example-contractor.test)
    - NANPA reserved test phone numbers (555-0100 through 555-0199)
    """

    @staticmethod
    def generate_lead(
        niche: Optional[TradeNiche] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        force_invalid_email: bool = False,
        force_invalid_phone: bool = False,
        has_24_7_claim: Optional[bool] = None
    ) -> RawLead:
        chosen_niche = niche or random.choice(list(TradeNiche))
        if city and state:
            c, s = city, state
        else:
            c, s = random.choice(SYNTHETIC_CITIES)

        first_name = random.choice(SYNTHETIC_FIRST_NAMES)
        last_name = random.choice(SYNTHETIC_LAST_NAMES)
        owner_name = f"{first_name} {last_name}"

        adj = random.choice(SYNTHETIC_ADJECTIVES)
        noun = random.choice(SYNTHETIC_NOUNS[chosen_niche])
        company_name = f"{adj} {noun} [Simulated]"
        slug = f"{adj.lower()}-{chosen_niche.value.lower()}-{c.lower()}"

        unique_code = f"{random.randint(10, 99)}"
        lead_id = f"sim_{chosen_niche.value.lower()[:3]}_{s.lower()}_{unique_code}"

        if force_invalid_email:
            email = f"invalid-bounce@{slug}.simulated.test"
        else:
            email = f"{first_name.lower()}@{slug}.simulated.test"

        # Area codes for synthetic cities
        area_code_map = {
            "TX": "214" if c == "Dallas" else "512",
            "AZ": "602",
            "CO": "303",
            "FL": "407",
            "GA": "404",
            "NC": "704",
            "TN": "615"
        }
        area_code = area_code_map.get(s, "555")

        # NANPA reserved test range: 555-0100 through 555-0199
        test_line_num = random.randint(10, 99)
        if force_invalid_phone:
            phone = "+1-555-0000" # invalid carrier test pattern (< 10 digits)
        else:
            phone = f"+1-{area_code}-555-01{test_line_num:02d}"

        website = f"https://{slug}.simulated.test"
        claim_24_7 = has_24_7_claim if has_24_7_claim is not None else random.choice([True, True, False])

        # Pick 2-3 reviews, ensuring at least one missed call review if 24/7 claimed
        missed_reviews = [r for r in SYNTHETIC_REVIEWS_TEMPLATES if r["mentions_missed_call"]]
        positive_reviews = [r for r in SYNTHETIC_REVIEWS_TEMPLATES if not r["mentions_missed_call"]]

        reviews_list = [
            ReviewItem(
                author=f"{random.choice(SYNTHETIC_FIRST_NAMES)} {random.choice(SYNTHETIC_LAST_NAMES)[0]}.",
                rating=missed_reviews[0]["rating"],
                text=random.choice(missed_reviews)["text"],
                date="2026-08-15",
                mentions_missed_call=True
            ),
            ReviewItem(
                author=f"{random.choice(SYNTHETIC_FIRST_NAMES)} {random.choice(SYNTHETIC_LAST_NAMES)[0]}.",
                rating=5,
                text=random.choice(positive_reviews)["text"],
                date="2026-07-28",
                mentions_missed_call=False
            )
        ]

        return RawLead(
            id=lead_id,
            company_name=company_name,
            owner_name=owner_name,
            niche=chosen_niche,
            city=c,
            state=s,
            phone=phone,
            email=email,
            website=website,
            has_24_7_service_claim=claim_24_7,
            reviews=reviews_list
        )

    @staticmethod
    def generate_batch(
        count: int = 3,
        niche: Optional[TradeNiche] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        include_bounce_risk: bool = True
    ) -> List[RawLead]:
        leads: List[RawLead] = []
        for i in range(count):
            # Only 1 in 4 leads (starting at index 3 or if specifically requested) is a bounce risk
            make_bounce = include_bounce_risk and count >= 3 and i == (count - 1)
            lead = SyntheticLeadGenerator.generate_lead(
                niche=niche,
                city=city,
                state=state,
                force_invalid_email=make_bounce
            )
            leads.append(lead)
        return leads


class SimulationProspectResponder:
    """
    Simulates prospect responses to Agent 4's outbound hooks.
    Generates realistic objections, inquiries, and positive intent.
    """

    PRESET_REPLIES = {
        "price_objection": [
            "Sounds interesting, but how much does this service cost per month? We are a small crew on a tight budget.",
            "What's the pricing on this? We don't want to get locked into an expensive software contract.",
            "Can you send over pricing details? Most of these tools charge an arm and a leg per minute."
        ],
        "complexity_objection": [
            "How complicated is the setup? We don't have an IT team to manage this.",
            "Does this replace our current phone system or integrate with our existing mobile lines? We don't want downtime.",
            "How long does it take to get up and running? We're currently in the middle of our busiest season."
        ],
        "already_have_objection": [
            "We already have an answering service that takes messages for us at night.",
            "Our dispatchers take turns holding the emergency phone overnight, so we have this covered."
        ],
        "positive_interest": [
            "Saw your email about our missed calls last weekend. Can I call the demo number right now from my cell?",
            "That estimated lost revenue is right on the money. We missed 3 calls just on Saturday. Can we test this?",
            "Sounds very relevant. How soon can we try the live voice test?"
        ],
        "unsubscribe": [
            "Please remove me from your mailing list immediately.",
            "Unsubscribe. We are not interested.",
            "Stop contacting this email address."
        ]
    }

    @staticmethod
    def create_simulated_reply(
        lead_id: str,
        company_name: str,
        sender_email: str,
        scenario: str = "price_objection",
        custom_text: Optional[str] = None
    ) -> InboundReply:
        if custom_text and custom_text.strip():
            content = custom_text.strip()
        else:
            templates = SimulationProspectResponder.PRESET_REPLIES.get(
                scenario, 
                SimulationProspectResponder.PRESET_REPLIES["price_objection"]
            )
            content = random.choice(templates)

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return InboundReply(
            lead_id=lead_id,
            company_name=company_name,
            channel="email",
            sender=sender_email,
            content=content,
            timestamp=now_str
        )

class SimulationManager:
    """
    Central Coordinator for the Swarm Simulation.
    Provides live activity logs, step execution, batch runs, and state querying for the UI.
    """

    def __init__(self, db: SwarmDatabase):
        self.db = db
        self.event_logs: List[Dict[str, Any]] = []
        self.current_step_index: int = 0
        self.steps_sequence = ["scout", "verify", "personalize", "dispatch", "reply", "close", "meta_review"]
        self.active_batch_leads: List[RawLead] = []
        self.active_hooks: List[Any] = []
        self.log_event("SYSTEM", "Simulation Manager initialized. Ready for simulation execution.", "info")

    def log_event(self, source: str, message: str, level: str = "info", metadata: Optional[Dict[str, Any]] = None):
        event = {
            "id": f"evt_{uuid.uuid4().hex[:6]}",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "source": source,
            "message": message,
            "level": level,
            "metadata": metadata or {}
        }
        self.event_logs.append(event)
        if len(self.event_logs) > 150:
            self.event_logs.pop(0)
        return event

    def get_event_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.event_logs[-limit:]

    def reset_simulation(self):
        self.db.reset_database()
        self.active_batch_leads.clear()
        self.active_hooks.clear()
        self.current_step_index = 0
        self.latest_refinement = None
        self.event_logs.clear()
        self.log_event("SYSTEM", "Simulation reset successfully. Database and pipeline cleared.", "warning")
        return {"status": "RESET_COMPLETE"}

    def get_state(self) -> Dict[str, Any]:
        metrics = self.db.get_metrics()
        step_name = self.steps_sequence[self.current_step_index] if self.current_step_index < len(self.steps_sequence) else "completed"
        return {
            "current_step_index": self.current_step_index,
            "current_step_name": step_name,
            "total_steps": len(self.steps_sequence),
            "active_batch_count": len(self.active_batch_leads),
            "metrics": metrics.model_dump(),
            "latest_refinement": self.latest_refinement.model_dump() if hasattr(self, "latest_refinement") and self.latest_refinement else None,
            "recent_logs": self.get_event_logs(20)
        }

    def step_next(
        self,
        niche: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        count: int = 2,
        scenario: str = "balanced"
    ) -> Dict[str, Any]:
        """Advances simulation by exactly one agent step."""
        from agents.scout_agent import LeadScoutAgent
        from agents.verifier_agent import VerificationSentryAgent
        from agents.personalizer_agent import HookPersonalizerAgent
        from agents.closer_agent import AutonomousCloserAgent
        from agents.meta_reviewer_agent import MetaReviewerAgent
        from core.llm import UniversalLLM

        llm = UniversalLLM()

        # Step 0: Scout Leads
        if self.current_step_index == 0:
            scout = LeadScoutAgent(db=self.db, llm=llm)
            self.log_event("AGENT 1: SCOUT", f"Scouting {count} synthetic contractor leads in {city or 'Dallas'}, {state or 'TX'} ({niche or 'Plumbing'})...")
            leads = scout.scout_leads(
                niche=niche,
                target_city=city,
                target_state=state,
                max_leads=count,
                use_synthetic_generator=True
            )
            self.active_batch_leads = leads
            self.current_step_index = 1
            self.log_event("AGENT 1: SCOUT", f"Discovered and saved {len(leads)} synthetic leads.", "success")
            return {"step": "scout", "leads": [l.model_dump() for l in leads], "next_step": "verify"}

        # Step 1: Verify Deliverability
        elif self.current_step_index == 1:
            verifier = VerificationSentryAgent(db=self.db)
            self.log_event("AGENT 2: VERIFIER", f"Auditing {len(self.active_batch_leads)} synthetic leads for syntax & carrier hygiene...")
            passed, results = verifier.verify_batch(self.active_batch_leads)
            self.active_batch_leads = passed
            self.current_step_index = 2
            self.log_event("AGENT 2: VERIFIER", f"Verified {len(passed)}/{len(results)} deliverable leads. Discarded {len(results)-len(passed)} bounce risks.", "success")
            return {"step": "verify", "passed_count": len(passed), "results": [r.model_dump() for r in results], "next_step": "personalize"}

        # Step 2: Personalize 3-Sentence ROI Hooks
        elif self.current_step_index == 2:
            personalizer = HookPersonalizerAgent(db=self.db, llm=llm)
            self.log_event("AGENT 3: PERSONALIZER", f"Synthesizing 3-sentence ROI hooks for {len(self.active_batch_leads)} verified contractors...")
            hooks = personalizer.generate_hooks_for_leads(self.active_batch_leads)
            self.active_hooks = hooks
            self.current_step_index = 3
            total_rev = sum(h.estimated_monthly_lost_revenue for h in hooks)
            self.log_event("AGENT 3: PERSONALIZER", f"Synthesized {len(hooks)} custom hooks. Total recoverable loss identified: ${total_rev:,.0f}/mo.", "success")
            return {"step": "personalize", "hooks": [h.model_dump() for h in hooks], "next_step": "dispatch"}

        # Step 3: Outbound Dispatch
        elif self.current_step_index == 3:
            closer = AutonomousCloserAgent(db=self.db, llm=llm)
            dispatches = []
            for h in self.active_hooks:
                res = closer.dispatch_initial_outreach(h, channel="email")
                dispatches.append(res)
                self.log_event("AGENT 4: CLOSER", f"Dispatched cold email touch to {h.company_name} (Subject: '{h.subject_line}')")
            self.current_step_index = 4
            return {"step": "dispatch", "dispatches": dispatches, "next_step": "reply"}

        # Step 4: Inbound Prospect Reply Simulation
        elif self.current_step_index == 4:
            replies = []
            reply_archetypes = ["price_objection", "complexity_objection", "positive_interest", "unsubscribe"]
            for idx, h in enumerate(self.active_hooks):
                # Pick scenario or alternate
                chosen_scene = scenario if scenario in SimulationProspectResponder.PRESET_REPLIES else reply_archetypes[idx % len(reply_archetypes)]
                lead_data = next((l for l in self.active_batch_leads if l.id == h.lead_id), None)
                sender = lead_data.email if lead_data else f"owner@{h.company_name.lower().replace(' ', '')}.simulated.test"
                reply = SimulationProspectResponder.create_simulated_reply(
                    lead_id=h.lead_id,
                    company_name=h.company_name,
                    sender_email=sender,
                    scenario=chosen_scene
                )
                replies.append(reply)
                self.log_event("PROSPECT (SIM)", f"Inbound reply received from {h.company_name}: \"{reply.content}\"", "info")

            self.pending_replies = replies
            self.current_step_index = 5
            return {"step": "reply", "replies": [r.model_dump() for r in replies], "next_step": "close"}

        # Step 5: Closer Objection Handling
        elif self.current_step_index == 5:
            closer = AutonomousCloserAgent(db=self.db, llm=llm)
            responses = []
            pending = getattr(self, "pending_replies", [])
            for r in pending:
                res = closer.process_inbound_reply(r)
                responses.append(res)
                self.log_event("AGENT 4: CLOSER", f"Classified intent [{res.detected_intent.value}] for {r.company_name} | Action: {res.action_taken}", "success")
            self.current_step_index = 6
            return {"step": "close", "closer_responses": [c.model_dump() for c in responses], "next_step": "meta_review"}

        # Step 6: Meta-Reviewer Evolutionary Optimization
        elif self.current_step_index == 6:
            meta = MetaReviewerAgent(db=self.db, llm=llm)
            self.log_event("AGENT 5: META-REVIEWER", "Evaluating campaign conversion metrics & running evolutionary prompt optimization...")
            refinement = meta.evaluate_and_optimize(batch_id=f"batch_{uuid.uuid4().hex[:4]}")
            self.latest_refinement = refinement
            self.current_step_index = 0 # reset back to 0 for next campaign loop
            self.log_event("AGENT 5: META-REVIEWER", f"Evolutionary optimization complete: {refinement.expected_conversion_gain}", "success")
            return {"step": "meta_review", "refinement": refinement.model_dump(), "next_step": "completed_ready_for_next_batch"}

        else:
            self.current_step_index = 0
            return {"step": "reset", "next_step": "scout"}

    def run_full_batch(
        self,
        niche: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        count: int = 3,
        scenario: str = "balanced"
    ) -> Dict[str, Any]:
        """Executes full end-to-end swarm execution across all 5 agents on synthetic leads."""
        self.current_step_index = 0
        step_outputs = {}

        # 1. Scout
        step_outputs["scout"] = self.step_next(niche=niche, city=city, state=state, count=count)
        # 2. Verify
        step_outputs["verify"] = self.step_next()
        # 3. Personalize
        step_outputs["personalize"] = self.step_next()
        # 4. Dispatch
        step_outputs["dispatch"] = self.step_next()
        # 5. Inbound Reply
        step_outputs["reply"] = self.step_next(scenario=scenario)
        # 6. Closer Response
        step_outputs["close"] = self.step_next()
        # 7. Meta-Reviewer
        step_outputs["meta_review"] = self.step_next()

        metrics = self.db.get_metrics()
        self.log_event("SYSTEM", "Full multi-agent simulation batch successfully finished!", "success")
        return {
            "status": "COMPLETED",
            "metrics": metrics.model_dump(),
            "step_outputs": step_outputs
        }

    def simulate_closer_reply(
        self,
        lead_id: str,
        scenario: str = "price_objection",
        custom_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """Simulates a prospect reply for a specific lead and runs Agent 4 Closer."""
        from agents.closer_agent import AutonomousCloserAgent
        from core.llm import UniversalLLM

        lead_detail = self.db.get_lead_detail(lead_id)
        if not lead_detail:
            raise ValueError(f"Lead {lead_id} not found in database.")

        lead_name = lead_detail.get("company_name", "Test Contractor")
        sender = lead_detail.get("email", "owner@simulated.test")

        reply = SimulationProspectResponder.create_simulated_reply(
            lead_id=lead_id,
            company_name=lead_name,
            sender_email=sender,
            scenario=scenario,
            custom_text=custom_text
        )

        self.log_event("PROSPECT (SIM)", f"Inbound message received from {lead_name}: \"{reply.content}\"")

        closer = AutonomousCloserAgent(db=self.db, llm=UniversalLLM())
        closer_res = closer.process_inbound_reply(reply)

        self.log_event(
            "AGENT 4: CLOSER", 
            f"Classified '{closer_res.detected_intent.value}' ({closer_res.confidence*100:.0f}%) | {closer_res.action_taken}",
            "success"
        )

        return {
            "inbound_reply": reply.model_dump(),
            "closer_response": closer_res.model_dump()
        }

    def run_meta_review(self, batch_id: Optional[str] = None) -> Dict[str, Any]:
        """Triggers Agent 5 Evolutionary Loop manually."""
        from agents.meta_reviewer_agent import MetaReviewerAgent
        from core.llm import UniversalLLM

        b_id = batch_id or f"batch_{uuid.uuid4().hex[:6]}"
        self.log_event("AGENT 5: META-REVIEWER", f"Manual trigger of meta-prompt evolutionary analysis for {b_id}...")
        meta = MetaReviewerAgent(db=self.db, llm=UniversalLLM())
        refinement = meta.evaluate_and_optimize(batch_id=b_id)
        self.latest_refinement = refinement
        self.log_event("AGENT 5: META-REVIEWER", f"Optimization complete: {refinement.expected_conversion_gain}", "success")
        return refinement.model_dump()

