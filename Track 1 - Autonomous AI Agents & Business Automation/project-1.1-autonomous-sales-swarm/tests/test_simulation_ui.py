import sys
from pathlib import Path
import pytest

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from core.simulation import SyntheticLeadGenerator, SimulationProspectResponder, SimulationManager

from core.database import SwarmDatabase
from core.schemas import TradeNiche, ReplyIntentType
from api.webhook_server import app, db as server_db

@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "sim_test.db"
    return SwarmDatabase(str(db_path))

@pytest.fixture
def sim_manager(test_db):
    return SimulationManager(db=test_db)

@pytest.fixture
def client():
    return TestClient(app)

def test_synthetic_lead_generator_safety():
    """Verify that generated leads strictly contain synthetic data and no real PII."""
    lead = SyntheticLeadGenerator.generate_lead(
        niche=TradeNiche.PLUMBING,
        city="Dallas",
        state="TX"
    )
    assert "[Simulated]" in lead.company_name
    assert ".simulated.test" in lead.email
    assert "+1-214-555-01" in lead.phone
    assert ".simulated.test" in lead.website
    assert len(lead.reviews) >= 2
    assert any(r.mentions_missed_call for r in lead.reviews)

def test_synthetic_batch_generation():
    batch = SyntheticLeadGenerator.generate_batch(count=4, niche=TradeNiche.HVAC)
    assert len(batch) == 4
    assert all(".simulated.test" in l.email for l in batch)

def test_simulation_prospect_responder():
    reply = SimulationProspectResponder.create_simulated_reply(
        lead_id="test_lead_01",
        company_name="Apex Rooter [Simulated]",
        sender_email="marcus@apex.simulated.test",
        scenario="price_objection"
    )
    assert reply.lead_id == "test_lead_01"
    assert "cost" in reply.content.lower() or "pricing" in reply.content.lower()

def test_simulation_manager_step_lifecycle(sim_manager):
    """Test step-by-step advancement of all 5 agents."""
    # Step 1: Scout
    out1 = sim_manager.step_next(niche="Plumbing", city="Austin", state="TX", count=2)
    assert out1["step"] == "scout"
    assert len(out1["leads"]) == 2

    # Step 2: Verify
    out2 = sim_manager.step_next()
    assert out2["step"] == "verify"
    assert out2["passed_count"] > 0

    # Step 3: Personalize
    out3 = sim_manager.step_next()
    assert out3["step"] == "personalize"
    assert len(out3["hooks"]) > 0

    # Step 4: Dispatch
    out4 = sim_manager.step_next()
    assert out4["step"] == "dispatch"
    assert len(out4["dispatches"]) > 0

    # Step 5: Inbound Reply
    out5 = sim_manager.step_next()
    assert out5["step"] == "reply"
    assert len(out5["replies"]) > 0

    # Step 6: Close
    out6 = sim_manager.step_next()
    assert out6["step"] == "close"
    assert len(out6["closer_responses"]) > 0

    # Step 7: Meta-Review
    out7 = sim_manager.step_next()
    assert out7["step"] == "meta_review"
    assert "refinement" in out7

def test_simulation_manager_run_full_batch(sim_manager):
    res = sim_manager.run_full_batch(niche="HVAC", count=2)
    assert res["status"] == "COMPLETED"
    assert res["metrics"]["total_leads_scouted"] >= 2
    assert res["metrics"]["outreach_sent"] >= 1

def test_simulation_manager_reset(sim_manager):
    sim_manager.run_full_batch(niche="Plumbing", count=2)
    assert len(sim_manager.db.get_all_leads()) > 0
    sim_manager.reset_simulation()
    assert len(sim_manager.db.get_all_leads()) == 0
    assert sim_manager.current_step_index == 0

def test_ui_dashboard_endpoint(client):
    """Verify that the Web Dashboard HTML is served with correct status code and title."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "AUTONOMOUS SALES SWARM" in response.text
    assert "100% SIMULATION" in response.text

def test_simulation_api_endpoints(client):
    # Reset first
    client.post("/api/simulation/reset")

    # Check initial state
    res_state = client.get("/api/simulation/state")
    assert res_state.status_code == 200
    data = res_state.json()
    assert "metrics" in data
    assert "current_step_name" in data

    # Run batch via API
    batch_payload = {
        "niche": "Roofing",
        "city": "Denver",
        "state": "CO",
        "count": 2,
        "scenario": "price_objection"
    }
    res_batch = client.post("/api/simulation/run-batch", json=batch_payload)
    assert res_batch.status_code == 200
    batch_data = res_batch.json()
    assert batch_data["status"] == "COMPLETED"

    # List leads
    res_leads = client.get("/api/simulation/leads")
    assert res_leads.status_code == 200
    leads = res_leads.json()
    assert len(leads) >= 2

    # Get single lead detail
    first_lead_id = leads[0]["id"]
    res_lead = client.get(f"/api/simulation/leads/{first_lead_id}")
    assert res_lead.status_code == 200
    lead_detail = res_lead.json()
    assert lead_detail["id"] == first_lead_id

    # Test Agent 4 Closer Sandbox reply endpoint
    closer_payload = {
        "lead_id": first_lead_id,
        "scenario": "price_objection",
        "custom_text": "Is there any monthly fee for small 2-truck contractors?"
    }
    res_closer = client.post("/api/simulation/closer-reply", json=closer_payload)
    assert res_closer.status_code == 200
    closer_data = res_closer.json()
    assert "closer_response" in closer_data
    assert closer_data["closer_response"]["detected_intent"] in [ReplyIntentType.OBJECTION_PRICE.value, ReplyIntentType.POSITIVE_INTEREST.value]

    # Test Meta-Reviewer trigger
    res_meta = client.post("/api/simulation/meta-review")
    assert res_meta.status_code == 200
    meta_data = res_meta.json()
    assert "improved_subject_lines" in meta_data
