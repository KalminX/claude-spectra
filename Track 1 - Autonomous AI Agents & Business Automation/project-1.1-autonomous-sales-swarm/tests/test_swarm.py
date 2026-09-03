import os
import sys
import pytest
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import SwarmDatabase
from core.llm import UniversalLLM
from core.schemas import (
    RawLead, 
    TradeNiche, 
    ReviewItem, 
    InboundReply, 
    ReplyIntentType, 
    VerificationStatus, 
    PhoneLineType
)
from agents.scout_agent import LeadScoutAgent
from agents.verifier_agent import VerificationSentryAgent
from agents.personalizer_agent import HookPersonalizerAgent
from agents.closer_agent import AutonomousCloserAgent
from agents.meta_reviewer_agent import MetaReviewerAgent
from core.state import create_swarm_graph

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_swarm.db"
    return SwarmDatabase(str(db_file))

@pytest.fixture
def llm():
    # Uses sandbox mode by default in tests ($0 cost, 100% deterministic)
    return UniversalLLM(provider="sandbox")

def test_scout_agent(temp_db):
    scout = LeadScoutAgent(db=temp_db)
    leads = scout.scout_leads(max_leads=2)
    assert len(leads) == 2
    assert leads[0].id is not None
    assert len(leads[0].reviews) > 0

def test_verifier_agent_filters_invalid(temp_db):
    verifier = VerificationSentryAgent(db=temp_db)
    
    valid_lead = RawLead(
        id="test_001",
        company_name="Valid Plumbing",
        niche=TradeNiche.PLUMBING,
        city="Austin",
        state="TX",
        phone="+1-512-555-0182",
        email="owner@validplumbing.com",
        website="https://validplumbing.com"
    )
    res_valid = verifier.verify_lead(valid_lead)
    assert res_valid.status == VerificationStatus.PASSED
    assert res_valid.phone_type == PhoneLineType.MOBILE

    invalid_lead = RawLead(
        id="test_002",
        company_name="Defunct Roofing",
        niche=TradeNiche.ROOFING,
        city="Orlando",
        state="FL",
        phone="+1-407-555-0922",
        email="invalid-bounce@defunct.com",
        website="https://defunct.com"
    )
    res_invalid = verifier.verify_lead(invalid_lead)
    assert res_invalid.status == VerificationStatus.DISCARDED

def test_personalizer_hook_generation(temp_db, llm):
    personalizer = HookPersonalizerAgent(db=temp_db, llm=llm)
    lead = RawLead(
        id="test_hook_001",
        company_name="LoneStar Air",
        niche=TradeNiche.HVAC,
        city="Dallas",
        state="TX",
        phone="+1-214-555-0182",
        email="lead@lonestarair.com",
        website="https://lonestarair.com",
        has_24_7_service_claim=True,
        reviews=[
            ReviewItem(author="Jane", rating=1, text="Voicemail full on Saturday evening.", date="2026-08-01", mentions_missed_call=True)
        ]
    )
    hook = personalizer.generate_hook(lead)
    assert hook.lead_id == lead.id
    assert hook.estimated_monthly_lost_revenue > 0
    assert len(hook.email_body_3_sentences) > 20
    assert len(hook.subject_line) > 0

def test_closer_handles_price_objection(temp_db, llm):
    closer = AutonomousCloserAgent(db=temp_db, llm=llm)
    reply = InboundReply(
        lead_id="test_001",
        company_name="LoneStar Air",
        sender="lead@lonestarair.com",
        content="How much does this cost? We are a small crew.",
        timestamp="now"
    )
    response = closer.process_inbound_reply(reply)
    assert response.detected_intent == ReplyIntentType.OBJECTION_PRICE
    assert response.demo_link_included is True
    assert "$497" in response.response_message or "recovered" in response.response_message.lower()

def test_closer_handles_unsubscribe(temp_db, llm):
    closer = AutonomousCloserAgent(db=temp_db, llm=llm)
    reply = InboundReply(
        lead_id="test_002",
        company_name="LoneStar Air",
        sender="lead@lonestarair.com",
        content="Please unsubscribe me immediately.",
        timestamp="now"
    )
    response = closer.process_inbound_reply(reply)
    assert response.detected_intent == ReplyIntentType.UNSUBSCRIBE
    assert response.action_taken == "SUPPRESSED_FROM_CRM"
    assert temp_db.is_suppressed("lead@lonestarair.com") is True

def test_meta_reviewer_optimization(temp_db, llm):
    meta_reviewer = MetaReviewerAgent(db=temp_db, llm=llm)
    refinement = meta_reviewer.evaluate_and_optimize("batch_test")
    assert len(refinement.improved_subject_lines) >= 2
    assert len(refinement.weak_patterns_detected) >= 2

def test_full_langgraph_swarm_workflow(temp_db, llm):
    graph = create_swarm_graph(db=temp_db, llm=llm)
    initial_state = {
        "target_niche": None,
        "target_state": None,
        "raw_leads": [],
        "verified_leads": [],
        "verification_results": [],
        "hooks": [],
        "dispatches": [],
        "inbound_replies": [
            InboundReply(
                lead_id="lead_tx_001",
                company_name="Apex Rapid Plumbing & Rooter",
                sender="marcus@apexrapidplumbing.com",
                content="Sounds neat, does it integrate with ServiceTitan?",
                timestamp="now"
            )
        ],
        "closer_responses": [],
        "refinement": None,
        "current_status": "Starting test..."
    }
    final_state = graph.invoke(initial_state)
    assert len(final_state["raw_leads"]) > 0
    assert len(final_state["verified_leads"]) > 0
    assert len(final_state["hooks"]) > 0
    assert len(final_state["dispatches"]) > 0
    assert len(final_state["closer_responses"]) == 1
    assert final_state["refinement"] is not None
