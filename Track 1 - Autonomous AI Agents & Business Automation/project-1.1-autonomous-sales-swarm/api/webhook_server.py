import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import SwarmDatabase
from core.llm import UniversalLLM
from core.schemas import InboundReply, CloserResponse, CampaignMetrics
from core.simulation import SimulationManager
from agents.closer_agent import AutonomousCloserAgent
from core.state import create_swarm_graph
from config import settings
from api.dashboard_html import get_dashboard_html
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Autonomous Sales & Closer Swarm — Simulation & Control Center",
    description="Interactive Web Dashboard & Simulation API for 5-Agent Outbound Swarm.",
    version="2.0.0"
)

frontend_dir = Path(__file__).parent.parent / "frontend"
if (frontend_dir / "css").exists():
    app.mount("/css", StaticFiles(directory=str(frontend_dir / "css")), name="css")
if (frontend_dir / "js").exists():
    app.mount("/js", StaticFiles(directory=str(frontend_dir / "js")), name="js")

db = SwarmDatabase(settings.DATABASE_PATH)
llm = UniversalLLM()
closer_agent = AutonomousCloserAgent(db=db, llm=llm)
sim_manager = SimulationManager(db=db)

# --- Request Schemas ---

class InboundPayload(BaseModel):
    lead_id: str
    company_name: str
    channel: str = "email"
    sender: str
    content: str

class RunCampaignRequest(BaseModel):
    niche: Optional[str] = None
    target_state: Optional[str] = None

class SimulationStepRequest(BaseModel):
    niche: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    count: int = 2
    scenario: str = "balanced"

class CloserSandboxRequest(BaseModel):
    lead_id: str
    scenario: str = "price_objection"
    custom_text: Optional[str] = None

# --- Web UI Routes ---

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Renders the comprehensive monitoring and control dashboard."""
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text())
    return HTMLResponse(content=get_dashboard_html())

@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard_alias():
    return serve_dashboard()


# --- Simulation API Endpoints ---

@app.get("/api/simulation/state")
def get_simulation_state():
    """Returns real-time pipeline status, active agent, metrics, and logs."""
    return sim_manager.get_state()

@app.get("/api/simulation/leads")
def list_simulated_leads():
    """Returns all leads in the database enriched with verification and hook statuses."""
    return db.get_all_leads(limit=100)

@app.get("/api/simulation/leads/{lead_id}")
def get_lead_details(lead_id: str):
    """Returns single lead record with complete conversation history and verification audit."""
    lead = db.get_lead_detail(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail=f"Lead {lead_id} not found")
    return lead

@app.post("/api/simulation/step")
def step_simulation(req: SimulationStepRequest):
    """Advances the simulation by exactly one agent step."""
    return sim_manager.step_next(
        niche=req.niche,
        city=req.city,
        state=req.state,
        count=req.count,
        scenario=req.scenario
    )

@app.post("/api/simulation/run-batch")
def run_simulation_batch(req: SimulationStepRequest):
    """Executes a full end-to-end swarm lifecycle on synthetic leads."""
    return sim_manager.run_full_batch(
        niche=req.niche,
        city=req.city,
        state=req.state,
        count=req.count,
        scenario=req.scenario
    )

@app.post("/api/simulation/closer-reply")
def simulate_closer_reply(req: CloserSandboxRequest):
    """Simulates an inbound prospect response and runs Agent 4 Closer."""
    try:
        return sim_manager.simulate_closer_reply(
            lead_id=req.lead_id,
            scenario=req.scenario,
            custom_text=req.custom_text
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/simulation/meta-review")
def run_meta_reviewer():
    """Manually triggers Agent 5 Meta-Reviewer evolutionary optimization."""
    return sim_manager.run_meta_review()

@app.post("/api/simulation/reset")
def reset_simulation():
    """Clears all simulated leads, hooks, conversations, and resets state."""
    return sim_manager.reset_simulation()

@app.get("/api/simulation/logs")
def get_event_logs():
    """Returns the latest in-memory execution event log."""
    return sim_manager.get_event_logs(limit=50)

# --- Existing / Legacy Compatible Endpoints ---

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "mode": "simulation",
        "product": settings.PRODUCT_NAME,
        "active_model": settings.DISPLAY_MODEL,
        "llm_provider": llm.provider
    }

@app.get("/api/metrics", response_model=CampaignMetrics)
def get_metrics():
    return db.get_metrics()

@app.post("/api/webhook/reply", response_model=CloserResponse)
def handle_inbound_reply(payload: InboundPayload):
    reply = InboundReply(
        lead_id=payload.lead_id,
        company_name=payload.company_name,
        channel=payload.channel,
        sender=payload.sender,
        content=payload.content,
        timestamp="now"
    )
    response = closer_agent.process_inbound_reply(reply)
    return response

@app.post("/api/campaign/run")
def trigger_swarm_run(req: RunCampaignRequest):
    graph = create_swarm_graph(db=db, llm=llm)
    initial_state = {
        "target_niche": req.niche,
        "target_state": req.target_state,
        "raw_leads": [],
        "verified_leads": [],
        "verification_results": [],
        "hooks": [],
        "dispatches": [],
        "inbound_replies": [],
        "closer_responses": [],
        "refinement": None,
        "current_status": "Starting swarm execution..."
    }
    final_state = graph.invoke(initial_state)
    return {
        "status": "COMPLETED",
        "scouted": len(final_state["raw_leads"]),
        "verified": len(final_state["verified_leads"]),
        "hooks_generated": len(final_state["hooks"]),
        "dispatches": len(final_state["dispatches"]),
        "optimization": final_state["refinement"]
    }
