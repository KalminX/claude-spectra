import os
import json
import logging
import uuid
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel
from core.schemas import RawLead, TradeNiche, ReviewItem
from core.database import SwarmDatabase
from core.llm import UniversalLLM
from core.simulation import SyntheticLeadGenerator

logger = logging.getLogger("Agent1_Scout")

class LeadScoutAgent:
    """
    AGENT 1: Lead Scout & Prospector (Simulation Engine)
    Operates in 100% Synthetic Simulation Mode.
    Generates realistic trade contractor profiles, customer review sentiments,
    and missed-call patterns without touching real businesses or real PII.
    """

    def __init__(self, db: SwarmDatabase, llm: Optional[UniversalLLM] = None):
        self.db = db
        self.llm = llm or UniversalLLM()
        self.data_dir = Path(__file__).parent.parent / "data"

    def scout_leads(
        self,
        niche: Optional[str] = None,
        target_city: Optional[str] = None,
        target_state: Optional[str] = None,
        max_leads: int = 3,
        use_live_search: bool = False,
        use_synthetic_generator: bool = True
    ) -> List[RawLead]:
        """
        Scouts synthetic contractor leads. 
        Zero real data: strictly generates synthetic test profiles or loads curated synthetic fixtures.
        """
        city = target_city or "Dallas"
        state = target_state or "TX"
        trade_str = niche or "Plumbing"

        # Map string to TradeNiche enum
        niche_map = {
            "plumbing": TradeNiche.PLUMBING,
            "hvac": TradeNiche.HVAC,
            "roofing": TradeNiche.ROOFING,
            "electrical": TradeNiche.ELECTRICAL
        }
        mapped_niche = niche_map.get(trade_str.lower(), TradeNiche.PLUMBING)

        logger.info(f"[Agent 1: Scout] [SIMULATION] Generating synthetic prospects for niche={trade_str} in {city}, {state}...")

        discovered: List[RawLead] = []

        # If synthetic procedural generation is enabled (default)
        if use_synthetic_generator:
            batch = SyntheticLeadGenerator.generate_batch(
                count=max_leads,
                niche=mapped_niche,
                city=city,
                state=state,
                include_bounce_risk=True
            )
            for lead in batch:
                self.db.save_lead(lead)
                discovered.append(lead)
            logger.info(f"[Agent 1: Scout] Synthesized {len(discovered)} simulated leads via procedural generator.")
            return discovered

        # Secondary mode: Load curated synthetic fixtures from sample_leads.json
        sample_file = self.data_dir / "sample_leads.json"
        if sample_file.exists():
            with open(sample_file, "r") as f:
                raw_data = json.load(f)

            for item in raw_data:
                lead = RawLead(**item)
                if niche and lead.niche.value.lower() != trade_str.lower():
                    continue
                if target_state and lead.state.lower() != state.lower():
                    continue

                self.db.save_lead(lead)
                discovered.append(lead)
                if len(discovered) >= max_leads:
                    break

        if not discovered:
            # Fallback to generator if fixtures had no matching niche
            discovered = SyntheticLeadGenerator.generate_batch(
                count=max_leads,
                niche=mapped_niche,
                city=city,
                state=state
            )
            for lead in discovered:
                self.db.save_lead(lead)

        logger.info(f"[Agent 1: Scout] Registered {len(discovered)} simulated contractor leads.")
        return discovered
