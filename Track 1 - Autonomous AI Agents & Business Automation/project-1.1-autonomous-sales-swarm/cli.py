import time
import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent))
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich import print as rprint

from core.database import SwarmDatabase
from core.llm import UniversalLLM
from core.schemas import InboundReply, ReplyIntentType
from agents.scout_agent import LeadScoutAgent
from agents.verifier_agent import VerificationSentryAgent
from agents.personalizer_agent import HookPersonalizerAgent
from agents.closer_agent import AutonomousCloserAgent
from agents.meta_reviewer_agent import MetaReviewerAgent
from core.state import create_swarm_graph
from config import settings

import argparse

console = Console()

def print_banner(live_mode: bool, llm: UniversalLLM):
    mode_badge = (
        "[bold white on green] LIVE REAL-TIME AI CONNECTED [/bold white on green] (Google Gemini 2.5 Flash / Claude Engine)"
        if llm.provider == "gemini" and llm.gemini_client
        else "[bold yellow on black] ZERO-COST SANDBOX MODE [/bold yellow on black]"
    )
    search_badge = (
        "[bold white on blue] LIVE GOOGLE SEARCH ACTIVE [/bold white on blue]"
        if live_mode
        else "[dim]FIXTURE MODE[/dim]"
    )
    banner_text = f"""
[bold cyan]╔════════════════════════════════════════════════════════════════════════════╗
║             AUTONOMOUS CLAUDE MARKETING & SALES AGENT SWARM                ║
║           5-Agent Outbound Engine for SkillsVital Voice AI Receptionist     ║
╚════════════════════════════════════════════════════════════════════════════╝[/bold cyan]
{mode_badge} | {search_badge}
[dim]Presented Model: [bold green]{settings.DISPLAY_MODEL}[/bold green] | Core Provider: [bold yellow]{settings.LLM_PROVIDER.upper()}[/bold yellow][/dim]
"""
    console.print(banner_text)

def run_interactive_swarm(live: bool = True, city: str = "Dallas", state: str = "TX", niche: str = "Plumbing", count: int = 2):
    db = SwarmDatabase(settings.DATABASE_PATH)
    llm = UniversalLLM()
    print_banner(live_mode=live, llm=llm)

    # Step 1: Scout
    console.print(f"\n[bold cyan]━━━━━━━━━━ AGENT 1: LEAD SCOUT & PROSPECTOR ({'LIVE GOOGLE SEARCH' if live else 'FIXTURE DIRECTORY'}) ━━━━━━━━━━[/bold cyan]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task_desc = f"Searching Google live for active {niche} contractors in {city}, {state}..." if live else f"Scanning contractor fixtures in {city}, {state}..."
        progress.add_task(description=task_desc, total=None)
        scout = LeadScoutAgent(db=db, llm=llm)
        leads = scout.scout_leads(
            niche=niche,
            target_city=city,
            target_state=state,
            max_leads=count,
            use_live_search=live
        )

    lead_table = Table(title="[bold green]Discovered Trade Contractor Leads[/bold green]", show_lines=True)
    lead_table.add_column("ID", style="cyan", width=12)
    lead_table.add_column("Company", style="bold white", width=30)
    lead_table.add_column("Niche", style="yellow", width=12)
    lead_table.add_column("Location", style="white", width=16)
    lead_table.add_column("Phone & 24/7 Claim", style="magenta", width=22)

    for l in leads:
        claim_badge = "[green]Yes (24/7)[/green]" if l.has_24_7_service_claim else "[dim]Standard[/dim]"
        lead_table.add_row(l.id, l.company_name, l.niche.value, f"{l.city}, {l.state}", f"{l.phone}\n{claim_badge}")
    console.print(lead_table)

    # Step 2: Verifier
    console.print("\n[bold cyan]━━━━━━━━━━ AGENT 2: VERIFICATION & DATA HYGIENE SENTRY ━━━━━━━━━━[/bold cyan]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Running ZeroBounce syntax check and Twilio carrier line-type audit...", total=None)
        time.sleep(1.2)
        verifier = VerificationSentryAgent(db=db)
        passed_leads, v_results = verifier.verify_batch(leads)

    v_table = Table(title="[bold green]Verification & Deliverability Audit[/bold green]", show_lines=True)
    v_table.add_column("Company", style="bold white", width=30)
    v_table.add_column("Line Type", style="yellow", width=12)
    v_table.add_column("Score", style="cyan", width=8)
    v_table.add_column("Status", style="bold", width=14)
    v_table.add_column("Hygiene Decision", style="dim white")

    for res in v_results:
        status_style = "[green]PASSED[/green]" if res.status.value == "PASSED" else "[red]DISCARDED[/red]"
        v_table.add_row(res.company_name, res.phone_type.value.upper(), f"{res.email_deliverability_score*100:.0f}%", status_style, res.reason)
    console.print(v_table)
    console.print(f"[bold green]✔ {len(passed_leads)}/{len(leads)} leads approved for outreach dispatch (Domain reputation protected).[/bold green]")

    # Step 3: Personalizer
    console.print("\n[bold cyan]━━━━━━━━━━ AGENT 3: CONTEXT & PERSONALIZATION ENGINE ━━━━━━━━━━[/bold cyan]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description=f"Parsing customer reviews and synthesizing 3-sentence ROI hooks with {settings.DISPLAY_MODEL}...", total=None)
        time.sleep(1.5)
        personalizer = HookPersonalizerAgent(db=db, llm=llm)
        hooks = personalizer.generate_hooks_for_leads(passed_leads)

    for h in hooks:
        hook_panel = Panel(
            f"[bold yellow]Subject:[/bold yellow] {h.subject_line}\n\n"
            f"[bold cyan]Email Body (3 Sentences):[/bold cyan]\n{h.email_body_3_sentences}\n\n"
            f"[bold magenta]Calculated ROI Loss:[/bold magenta] [bold red]${h.estimated_monthly_lost_revenue:,.0f}/month[/bold red] "
            f"([dim]{h.estimated_monthly_missed_calls} missed calls @ ${h.estimated_ticket_value:.0f} avg ticket[/dim])\n"
            f"[bold green]SMS Alternative:[/bold green] {h.sms_body}",
            title=f"[bold white]{h.company_name}[/bold white]",
            border_style="cyan"
        )
        console.print(hook_panel)

    # Step 4: Closer Outbound Dispatch
    console.print("\n[bold cyan]━━━━━━━━━━ AGENT 4: MULTI-TOUCH OUTBOUND & CLOSER DISPATCH ━━━━━━━━━━[/bold cyan]")
    closer = AutonomousCloserAgent(db=db, llm=llm)
    for h in hooks:
        dispatch = closer.dispatch_initial_outreach(h, channel="email")
        console.print(f"[green]✔ Dispatched Outbound Pitch[/green] to [bold]{h.company_name}[/bold] via Smartlead rotation.")

    # Step 5: Inbound Reply & Objection Handling Simulation
    console.print("\n[bold cyan]━━━━━━━━━━ AGENT 4: INBOUND OBJECTION HANDLING SIMULATION ━━━━━━━━━━[/bold cyan]")
    sample_replies = [
        InboundReply(
            lead_id=hooks[0].lead_id,
            company_name=hooks[0].company_name,
            channel="email",
            sender=passed_leads[0].email,
            content="Sounds interesting, but how much does this service cost per month? We're on a tight budget.",
            timestamp="10 mins later"
        ),
        InboundReply(
            lead_id=hooks[1].lead_id,
            company_name=hooks[1].company_name,
            channel="email",
            sender=passed_leads[1].email,
            content="Can you call me on Monday? I want to hear how the receptionist sounds in real time.",
            timestamp="15 mins later"
        )
    ]

    for reply in sample_replies:
        console.print(f"\n[bold yellow]Incoming Reply from {reply.company_name}:[/bold yellow] \"{reply.content}\"")
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description=f"Classifying intent and formulating autonomous closer response with {settings.DISPLAY_MODEL}...", total=None)
            time.sleep(1.0)
            closer_res = closer.process_inbound_reply(reply)

        reply_panel = Panel(
            f"[bold yellow]Classified Intent:[/bold yellow] [bold green]{closer_res.detected_intent.value}[/bold green] (Confidence: {closer_res.confidence*100:.0f}%)\n"
            f"[bold cyan]Agent Reasoning:[/bold cyan] {closer_res.reasoning}\n"
            f"[bold magenta]Action Taken:[/bold magenta] {closer_res.action_taken}\n\n"
            f"[bold white]Autonomous Response Sent:[/bold white]\n{closer_res.response_message}",
            title=f"[bold green]Autonomous Closer Decision: {reply.company_name}[/bold green]",
            border_style="green"
        )
        console.print(reply_panel)

    # Step 6: Agent 5 Evolutionary Feedback
    console.print("\n[bold cyan]━━━━━━━━━━ AGENT 5: META-REVIEWER & SELF-IMPROVEMENT LOOP ━━━━━━━━━━[/bold cyan]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Evaluating campaign conversion metrics and auto-refactoring prompt parameters...", total=None)
        time.sleep(1.2)
        meta_reviewer = MetaReviewerAgent(db=db, llm=llm)
        refinement = meta_reviewer.evaluate_and_optimize(batch_id="batch_001")

    opt_panel = Panel(
        f"[bold white]Analysis Summary:[/bold white]\n{refinement.analysis_summary}\n\n"
        f"[bold red]Weak Patterns Isolated:[/bold red]\n• " + "\n• ".join(refinement.weak_patterns_detected) + "\n\n"
        f"[bold green]Auto-Refactored Subject Lines for Next Batch:[/bold green]\n• " + "\n• ".join(refinement.improved_subject_lines) + "\n\n"
        f"[bold yellow]Adjusted Hook Angles:[/bold yellow]\n• " + "\n• ".join(refinement.adjusted_hook_angles) + "\n\n"
        f"[bold cyan]Projected Conversion Velocity Gain:[/bold cyan] [bold green]{refinement.expected_conversion_gain}[/bold green]",
        title="[bold yellow]Agent 5: Evolutionary Meta-Prompt Refinement[/bold yellow]",
        border_style="yellow"
    )
    console.print(opt_panel)

    # Summary Metrics
    metrics = db.get_metrics()
    metrics_table = Table(title="[bold green]Final Swarm Campaign Performance Metrics[/bold green]", show_lines=True)
    metrics_table.add_column("Total Scouted", style="cyan")
    metrics_table.add_column("Verified Safe", style="green")
    metrics_table.add_column("Dispatched", style="yellow")
    metrics_table.add_column("Replies", style="magenta")
    metrics_table.add_column("Positive", style="bold green")
    metrics_table.add_column("Objections Handled", style="bold yellow")
    metrics_table.add_column("Demos Triggered", style="bold cyan")

    metrics_table.add_row(
        str(metrics.total_leads_scouted),
        str(metrics.verified_leads),
        str(metrics.outreach_sent),
        str(metrics.replies_received),
        str(metrics.positive_replies),
        str(metrics.objections_handled),
        str(metrics.demos_booked)
    )
    console.print("\n", metrics_table)
    console.print("\n[bold green]✔ Autonomous Multi-Agent Swarm execution complete with 0 manual human touches![/bold green]\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Sales Swarm Runner")
    parser.add_argument("--sandbox", action="store_true", help="Force $0 sandbox fixture mode")
    parser.add_argument("--city", default="Dallas", help="Target city (e.g. Dallas, Miami, Phoenix)")
    parser.add_argument("--state", default="TX", help="Target state code (e.g. TX, FL, AZ)")
    parser.add_argument("--niche", default="Plumbing", help="Trade niche (Plumbing, HVAC, Roofing, Electrical)")
    parser.add_argument("--count", type=int, default=2, help="Number of leads to scout")
    args = parser.parse_args()

    run_interactive_swarm(
        live=not args.sandbox,
        city=args.city,
        state=args.state,
        niche=args.niche,
        count=args.count
    )
