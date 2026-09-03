import logging
from typing import TypedDict, List, Optional, Dict, Any
from langgraph.graph import StateGraph, START, END

from core.schemas import (
    RawLead, 
    VerificationResult, 
    PersonalizedHook, 
    InboundReply, 
    CloserResponse, 
    PromptRefinement
)
from core.database import SwarmDatabase
from core.llm import UniversalLLM
from agents.scout_agent import LeadScoutAgent
from agents.verifier_agent import VerificationSentryAgent
from agents.personalizer_agent import HookPersonalizerAgent
from agents.closer_agent import AutonomousCloserAgent
from agents.meta_reviewer_agent import MetaReviewerAgent

logger = logging.getLogger("SwarmOrchestrator")

class SwarmState(TypedDict):
    target_niche: Optional[str]
    target_state: Optional[str]
    raw_leads: List[RawLead]
    verified_leads: List[RawLead]
    verification_results: List[VerificationResult]
    hooks: List[PersonalizedHook]
    dispatches: List[Dict[str, Any]]
    inbound_replies: List[InboundReply]
    closer_responses: List[CloserResponse]
    refinement: Optional[PromptRefinement]
    current_status: str

def create_swarm_graph(db: SwarmDatabase, llm: Optional[UniversalLLM] = None):
    """
    Constructs the LangGraph multi-agent state graph connecting all 5 agents:
    [Scout] -> [Verifier] -> [Personalizer] -> [Closer Dispatch] -> [Inbound Handler] -> [Meta-Reviewer]
    """
    llm_instance = llm or UniversalLLM()
    
    scout_agent = LeadScoutAgent(db=db)
    verifier_agent = VerificationSentryAgent(db=db)
    personalizer_agent = HookPersonalizerAgent(db=db, llm=llm_instance)
    closer_agent = AutonomousCloserAgent(db=db, llm=llm_instance)
    meta_reviewer = MetaReviewerAgent(db=db, llm=llm_instance)

    # Node 1: Scout
    def scout_node(state: SwarmState) -> Dict[str, Any]:
        leads = scout_agent.scout_leads(
            niche=state.get("target_niche"),
            target_state=state.get("target_state"),
            max_leads=10
        )
        return {
            "raw_leads": leads,
            "current_status": f"Scouted {len(leads)} leads."
        }

    # Node 2: Verifier
    def verifier_node(state: SwarmState) -> Dict[str, Any]:
        passed, results = verifier_agent.verify_batch(state.get("raw_leads", []))
        return {
            "verified_leads": passed,
            "verification_results": results,
            "current_status": f"Verified {len(passed)}/{len(results)} deliverable leads."
        }

    # Node 3: Personalizer
    def personalizer_node(state: SwarmState) -> Dict[str, Any]:
        hooks = personalizer_agent.generate_hooks_for_leads(state.get("verified_leads", []))
        return {
            "hooks": hooks,
            "current_status": f"Synthesized {len(hooks)} personalized ROI hooks."
        }

    # Node 4: Closer Outbound Dispatch
    def dispatch_node(state: SwarmState) -> Dict[str, Any]:
        dispatches = []
        for hook in state.get("hooks", []):
            dispatch_res = closer_agent.dispatch_initial_outreach(hook, channel="email")
            dispatches.append(dispatch_res)
        return {
            "dispatches": dispatches,
            "current_status": f"Dispatched {len(dispatches)} initial outbound pitches."
        }

    # Node 5: Inbound Reply & Objection Handling
    def inbound_handler_node(state: SwarmState) -> Dict[str, Any]:
        # Process any pending inbound replies
        closer_responses = []
        for reply in state.get("inbound_replies", []):
            res = closer_agent.process_inbound_reply(reply)
            closer_responses.append(res)
        return {
            "closer_responses": closer_responses,
            "current_status": f"Handled {len(closer_responses)} inbound prospect replies."
        }

    # Node 6: Meta-Reviewer Evolutionary Feedback
    def meta_review_node(state: SwarmState) -> Dict[str, Any]:
        refinement = meta_reviewer.evaluate_and_optimize(batch_id="batch_001")
        return {
            "refinement": refinement,
            "current_status": "Completed evolutionary prompt refactoring."
        }

    # Build Graph
    builder = StateGraph(SwarmState)
    builder.add_node("scout", scout_node)
    builder.add_node("verifier", verifier_node)
    builder.add_node("personalizer", personalizer_node)
    builder.add_node("dispatch", dispatch_node)
    builder.add_node("inbound_handler", inbound_handler_node)
    builder.add_node("meta_review", meta_review_node)

    builder.add_edge(START, "scout")
    builder.add_edge("scout", "verifier")
    builder.add_edge("verifier", "personalizer")
    builder.add_edge("personalizer", "dispatch")
    builder.add_edge("dispatch", "inbound_handler")
    builder.add_edge("inbound_handler", "meta_review")
    builder.add_edge("meta_review", END)

    return builder.compile()
