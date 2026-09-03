import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from core.schemas import InboundReply, CloserResponse, ReplyIntentType, PersonalizedHook
from core.database import SwarmDatabase
from core.llm import UniversalLLM
from config import settings

logger = logging.getLogger("Agent4_Closer")

class AutonomousCloserAgent:
    """
    AGENT 4: Multi-Touch Outbound & Autonomous Closer
    Handles multi-touch dispatch, ingests prospect replies in real-time,
    classifies intent (Positive, Price Objection, Setup Complexity, Already Have, Unsubscribe),
    and autonomously issues rebuttals, demo line numbers, or suppression updates.
    """

    def __init__(self, db: SwarmDatabase, llm: Optional[UniversalLLM] = None):
        self.db = db
        self.llm = llm or UniversalLLM()
        self.objection_library = self._load_objection_library()

    def _load_objection_library(self) -> Dict[str, Any]:
        obj_file = Path(__file__).parent.parent / "data" / "objection_library.json"
        if obj_file.exists():
            with open(obj_file, "r") as f:
                return json.load(f).get("objections", {})
        return {}

    def dispatch_initial_outreach(self, hook: PersonalizedHook, channel: str = "email") -> Dict[str, Any]:
        """
        Simulates dispatch of the initial personalized cold touch via Smartlead/Twilio.
        """
        logger.info(f"[Agent 4: Closer] Dispatching initial {channel.upper()} outreach to {hook.company_name}...")
        
        message_body = hook.email_body_3_sentences if channel == "email" else hook.sms_body
        self.db.log_message(
            lead_id=hook.lead_id,
            direction="OUTBOUND",
            channel=channel.upper(),
            message=message_body,
            intent="INITIAL_PITCH",
            confidence=1.0,
            action="SENT_INITIAL_HOOK"
        )
        return {
            "lead_id": hook.lead_id,
            "status": "DISPATCHED",
            "channel": channel,
            "subject": hook.subject_line,
            "content": message_body
        }

    def process_inbound_reply(self, reply: InboundReply) -> CloserResponse:
        """
        Ingests an incoming prospect reply, classifies intent, and issues an autonomous response.
        """
        logger.info(f"[Agent 4: Closer] Inbound reply received from {reply.company_name}: '{reply.content}'")
        
        # Log inbound message to conversation history
        self.db.log_message(
            lead_id=reply.lead_id,
            direction="INBOUND",
            channel=reply.channel.upper(),
            message=reply.content
        )

        # 1. Quick rule-based filter for explicit unsubscribes
        lower_content = reply.content.lower().strip()
        if any(w in lower_content for w in ["unsubscribe", "remove me", "stop", "take me off", "not interested"]):
            self.db.suppress_contact(email=reply.sender, reason="Prospect requested unsubscribe")
            response = CloserResponse(
                lead_id=reply.lead_id,
                company_name=reply.company_name,
                detected_intent=ReplyIntentType.UNSUBSCRIBE,
                confidence=0.99,
                reasoning="Explicit unsubscribe keyword detected. Zero-touch suppression triggered.",
                response_message="Understood! You've been removed from our list. Wishing you continued success.",
                action_taken="SUPPRESSED_FROM_CRM",
                demo_link_included=False
            )
            self.db.log_message(
                lead_id=reply.lead_id,
                direction="OUTBOUND",
                channel=reply.channel.upper(),
                message=response.response_message,
                intent=response.detected_intent.value,
                confidence=response.confidence,
                action=response.action_taken
            )
            return response

        # 2. LLM Intent Classification & Response Formulation
        system_prompt = (
            "You are an autonomous AI closing agent for SkillsVital Voice AI (https://skillsvital.com/voice). "
            "Your job is to classify inbound prospect messages from home service contractors into exact intent categories "
            "and craft a conversational, helpful, non-pushy reply. Address objections directly and offer our live demo line."
        )

        prompt = f"""
        Company: {reply.company_name}
        Sender: {reply.sender}
        Incoming Message: "{reply.content}"
        Demo Line: {settings.DEMO_PHONE_NUMBER}
        Booking Calendar: {settings.CALENDLY_URL}

        Objection Knowledge Base Reference:
        {json.dumps(self.objection_library, indent=2)}

        Classify into one of these intents:
        - POSITIVE_INTEREST
        - OBJECTION_PRICE
        - OBJECTION_COMPLEXITY
        - OBJECTION_ALREADY_HAVE
        - UNSUBSCRIBE
        - UNCLEAR

        Provide:
        1. detected_intent
        2. confidence (0.0 to 1.0)
        3. reasoning (Why this intent was chosen)
        4. response_message (Direct, friendly response in 2-3 sentences max)
        5. action_taken ("SENT_DEMO_LINK", "SENT_OBJECTION_REBUTTAL", "SUPPRESSED_FROM_CRM", "ESCALATED")
        6. demo_link_included (bool)
        """

        # Deterministic sandbox responses
        sandbox_data = self._generate_sandbox_reply(reply)

        closer_res = self.llm.generate_structured(
            prompt=prompt,
            schema=CloserResponse,
            system_instruction=system_prompt,
            sandbox_fallback_data=sandbox_data
        )

        # Ensure ID consistency
        closer_res.lead_id = reply.lead_id
        closer_res.company_name = reply.company_name

        # Log closer outbound action
        self.db.log_message(
            lead_id=reply.lead_id,
            direction="OUTBOUND",
            channel=reply.channel.upper(),
            message=closer_res.response_message,
            intent=closer_res.detected_intent.value,
            confidence=closer_res.confidence,
            action=closer_res.action_taken
        )

        logger.info(f"[Agent 4: Closer] Classified intent: {closer_res.detected_intent.value} | Action: {closer_res.action_taken}")
        return closer_res

    def _generate_sandbox_reply(self, reply: InboundReply) -> Dict[str, Any]:
        text = reply.content.lower()
        if "how much" in text or "cost" in text or "price" in text:
            intent = ReplyIntentType.OBJECTION_PRICE
            action = "SENT_OBJECTION_REBUTTAL"
            reason = "Prospect asking about pricing/cost structure."
            msg = (
                f"It's a flat $497/month with no setup fees or contracts. For a contractor your size, saving just one "
                f"emergency job pays for the entire year. You can test it yourself right now on your phone by calling "
                f"our live demo line at {settings.DEMO_PHONE_NUMBER}."
            )
            demo = True
        elif "complicated" in text or "setup" in text or "time" in text:
            intent = ReplyIntentType.OBJECTION_COMPLEXITY
            action = "SENT_OBJECTION_REBUTTAL"
            reason = "Prospect worried about setup time and technological complexity."
            msg = (
                f"Zero software to install on your end. It connects via standard carrier forwarding: whenever your line "
                f"rings for 4 rings or after hours, it routes to the AI receptionist. Takes under 5 minutes to activate. "
                f"Call {settings.DEMO_PHONE_NUMBER} to hear how it works."
            )
            demo = True
        else:
            intent = ReplyIntentType.POSITIVE_INTEREST
            action = "SENT_DEMO_LINK"
            reason = "Prospect expressing curiosity and wanting to see it in action."
            msg = (
                f"Glad to hear! The fastest way to see it is to dial our live contractor demo line directly at {settings.DEMO_PHONE_NUMBER} "
                f"from your cell. It will answer as an AI receptionist so you can test how natural it sounds. If you prefer a 10-min screen share, here's our calendar: {settings.CALENDLY_URL}"
            )
            demo = True

        return {
            "lead_id": reply.lead_id,
            "company_name": reply.company_name,
            "detected_intent": intent.value,
            "confidence": 0.94,
            "reasoning": reason,
            "response_message": msg,
            "action_taken": action,
            "demo_link_included": demo
        }
