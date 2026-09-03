# Comprehensive Portfolio Roadmap: Claude AI & Agentic Systems

> **Strategic Objective:** A master collection of real-world, high-leverage AI engineering projects categorized into structured domain tracks. Building these projects creates an undeniable, end-to-end portfolio covering autonomous agent swarms, enterprise ERP/SharePoint integrations, full-stack AI SaaS platforms, programmatic media pipelines, and developer tooling.

---

## Table of Contents
- [Track 1: Autonomous AI Agent Swarms & Lead Gen Engines](#track-1-autonomous-ai-agent-swarms--lead-gen-engines)
  - [Project 1.1: Autonomous 5-Agent Outbound Sales & Closer Swarm](#project-11-autonomous-5-agent-outbound-sales--closer-swarm)
  - [Project 1.2: End-to-End n8n Lead Management & GoHighLevel Engine](#project-12-end-to-end-n8n-lead-management--gohighlevel-engine)
  - [Project 1.3: Autonomous Email Attachment & Google Drive Auto-Filer](#project-13-autonomous-email-attachment--google-drive-auto-filer)
- [Track 2: Full-Stack AI Web Applications & SaaS Dashboards](#track-2-full-stack-ai-web-applications--saas-dashboards)
  - [Project 2.1: Claude + Canva Design Studio & Multi-Tenant Business Dashboard](#project-21-claude--canva-design-studio--multi-tenant-business-dashboard)
  - [Project 2.2: Client-Facing AI Chat Assistant with Live Tool Calling](#project-22-client-facing-ai-chat-assistant-with-live-tool-calling)
  - [Project 2.3: Production Dual-Layer Web Application](#project-23-production-dual-layer-web-application)
- [Track 3: Enterprise Workflow Automation & Systems Integration](#track-3-enterprise-workflow-automation--systems-integration)
  - [Project 3.1: ERPNext / Frappe Claude MCP Agent & Approval Gatekeeper](#project-31-erpnext--frappe-claude-mcp-agent--approval-gatekeeper)
  - [Project 3.2: SharePoint Excel Cloud Tracker & Power Automate AI Copilot](#project-32-sharepoint-excel-cloud-tracker--power-automate-ai-copilot)
  - [Project 3.3: Natural Language Google Sheets Auto-Fill Connector](#project-33-natural-language-google-sheets-auto-fill-connector)
- [Track 4: Developer Tooling, Multi-Session Orchestration & Swarms](#track-4-developer-tooling-multi-session-orchestration--swarms)
  - [Project 4.1: Claude Code Multi-Session Orchestration Console & Notification Plane](#project-41-claude-code-multi-session-orchestration-console--notification-plane)
  - [Project 4.2: Multi-Client Agent Swarm Architecture & Token Optimization](#project-42-multi-client-agent-swarm-architecture--token-optimization)
  - [Project 4.3: Windows & WSL2 Developer Environment Tuning & Coaching Framework](#project-43-windows--wsl2-developer-environment-tuning--coaching-framework)
- [Track 5: AI Media, Content Engines & Automated Video Pipelines](#track-5-ai-media-content-engines--automated-video-pipelines)
  - [Project 5.1: Football YouTube Shorts Pipeline (Claude Code + ElevenLabs + CapCut)](#project-51-football-youtube-shorts-pipeline-claude-code--elevenlabs--capcut)
  - [Project 5.2: High-Velocity AI Video Pipeline (Higgsfield + FFmpeg + Claude)](#project-52-high-velocity-ai-video-pipeline-higgsfield--ffmpeg--claude)
  - [Project 5.3: Multi-Brand Instagram AI Marketing Director & Content Engine](#project-53-multi-brand-instagram-ai-marketing-director--content-engine)
- [Track 6: AI Design Systems, Workspace Operations & Education](#track-6-ai-design-systems-workspace-operations--education)
  - [Project 6.1: Brand Design System as Code (React Components + Design Tokens)](#project-61-brand-design-system-as-code-react-components--design-tokens)
  - [Project 6.2: Multi-Company Claude Cowork & Skills Executive Assistant](#project-62-multi-company-claude-cowork--skills-executive-assistant)
  - [Project 6.3: Studio 2-Hour Video Masterclass Course Production](#project-63-studio-2-hour-video-masterclass-course-production)

---

# Track 1: Autonomous AI Agent Swarms & Lead Gen Engines

## Project 1.1: Autonomous 5-Agent Outbound Sales & Closer Swarm
- **Target Offer / Domain:** Autonomous outbound customer acquisition engine for B2B Voice AI SaaS (`skillsvital.com/voice`) targeting local trade contractors (Plumbing, HVAC, Roofing).
- **Core Architecture:**
  - **Agent 1 (Scout):** Scrapes local business directories and maps for service businesses with missed-call vulnerabilities.
  - **Agent 2 (Verifier):** Validates email deliverability (ZeroBounce) and checks phone carrier lines (Twilio Lookup).
  - **Agent 3 (Context & Hook Engine):** Claude 3.5 Sonnet parses customer reviews, calculates estimated revenue lost from missed calls, and writes hyper-personalized 3-sentence hooks.
  - **Agent 4 (Outbound & Closer):** Manages multi-touch sequences, classifies inbound replies, handles objections dynamically, and issues direct demo lines & checkout links.
  - **Agent 5 (Meta-Reviewer):** Analyzes weekly conversion metrics and auto-refactors prompt parameters for higher reply velocity.
- **Tech Stack:** Python (LangGraph), n8n, Anthropic Claude 3.5 Sonnet, Smartlead.ai, Twilio API, Supabase PostgreSQL.
- **Source Brief:** [`autonomous_claude_marketing_sales_agent_swarm_brief.md`](file:///Users/kalmin/startups/claude-spectra/autonomous_claude_marketing_sales_agent_swarm_brief.md)

```
+-----------------------------------------------------------------------------------+
|               AUTONOMOUS CLAUDE MARKETING & CLOSER AGENT SWARM                    |
+-----------------------------------------------------------------------------------+
|  [Agent 1: Scout] ──> [Agent 2: Verifier] ──> [Agent 3: Claude Hook Personalizer] |
|                                                        │                          |
|  [Agent 5: Self-Improving Feedback Loop] <── [Agent 4: Multi-Touch Closer]        |
+-----------------------------------------------------------------------------------+
```

---

## Project 1.2: End-to-End n8n Lead Management & GoHighLevel Engine
- **Target Offer / Domain:** Digital marketing agency managing multi-channel paid ad campaigns (Meta Lead Ads, Typeform, Webforms).
- **Core Architecture:**
  - Ingests inbound leads in real time via webhooks.
  - Third-party enrichment via Apollo / Clearbit / Hunter APIs.
  - Claude 3.5 Sonnet scores lead fit/intent (0–100) and outputs a structured 3-bullet executive brief in JSON.
  - Syncs contacts and pipeline stages in **GoHighLevel (GHL)** with dynamic sales rep assignment.
  - Sends rich Block Kit Slack notifications with 1-click action buttons and triggers automated nurture emails.
- **Tech Stack:** n8n Cloud / Docker, Anthropic Claude 3.5 Sonnet, GoHighLevel REST API v2, Slack API, Google Sheets / Airtable.
- **Source Brief:** [`claude_n8n_lead_management_automation_gohighlevel_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_n8n_lead_management_automation_gohighlevel_brief.md)

---

## Project 1.3: Autonomous Email Attachment & Google Drive Auto-Filer
- **Target Offer / Domain:** Zero-touch document management system for invoices, contracts, receipts, and supplier reports.
- **Core Architecture:**
  - Automated ingestion from incoming emails (Gmail / Outlook).
  - Claude inspects email body metadata and performs OCR/text analysis on attached PDFs/images.
  - Extracts Entity Name, Document Type, Reference Number, and Date into structured JSON.
  - Standardizes filenames: `YYYY-MM-DD_[Entity]_[DocType]_[RefNumber].[ext]`.
  - Automatically files document into target Google Drive folders with a dedicated `_Needs_Review_Inbox` fallback queue for ambiguous cases.
- **Tech Stack:** Python (Serverless Cloud Run / AWS Lambda) or Google Apps Script, Gmail API, Google Drive API, Claude 3.5 Haiku / Sonnet.
- **Source Brief:** [`autonomous_claude_agent_email_attachments_google_drive_brief.md`](file:///Users/kalmin/startups/claude-spectra/autonomous_claude_agent_email_attachments_google_drive_brief.md)

---

# Track 2: Full-Stack AI Web Applications & SaaS Dashboards

## Project 2.1: Claude + Canva Design Studio & Multi-Tenant Business Dashboard
- **Target Offer / Domain:** Multi-role enterprise SaaS dashboard featuring official Claude + Canva AI Connector / MCP workflows.
- **Core Architecture:**
  - Modern dashboard with 4 core views: `Overview`, `Claude Design`, `Company Knowledge`, and `Settings`.
  - Authentication with Role-Based Access Control (Admin, Manager, Staff).
  - Admin-managed Brand Knowledge Base (voice, guidelines, hex palettes, fonts, logo assets).
  - Direct integration with Canva Teams MCP: `Natural Language Prompt` $\rightarrow$ `Claude Context Assembly` $\rightarrow$ `Canva MCP Call` $\rightarrow$ `Live Editable Canva Design URL` $\rightarrow$ `Human Review & Export`.
- **Tech Stack:** Next.js 14 (App Router), TypeScript, TailwindCSS (shadcn/ui), PostgreSQL (Prisma/Drizzle), NextAuth.js, Anthropic SDK, Canva Connect/MCP API.
- **Source Brief:** [`full_stack_ai_developer_claude_canva_business_dashboard_brief.md`](file:///Users/kalmin/startups/claude-spectra/full_stack_ai_developer_claude_canva_business_dashboard_brief.md)

```
+-----------------------------------------------------------------------------------+
|                  CLAUDE + CANVA BUSINESS PLATFORM ARCHITECTURE                    |
+-----------------------------------------------------------------------------------+
|  [Next.js Dashboard] ──> [Backend Route Handler] ──> [Brand Knowledge Engine]     |
|                                                              │                    |
|  [Editable Canva Design URL] <── [Canva Teams MCP] <── [Claude 3.5 Sonnet]        |
+-----------------------------------------------------------------------------------+
```

---

## Project 2.2: Client-Facing AI Chat Assistant with Live Tool Calling
- **Target Offer / Domain:** Interactive client-facing assistant prototype with production-ready real-time streaming and tool integration.
- **Core Architecture:**
  - Responsive chat UI with low-latency Server-Sent Events (SSE) token streaming.
  - Multi-turn conversation state persistence across turns.
  - Config-driven system prompt isolation (JSON/YAML) for easy non-technical edits.
  - Functional tool calling wired to external REST APIs or local databases with automated error handling and rate-limit backoff.
- **Tech Stack:** Next.js / React or Python (FastAPI), Anthropic Claude Messages API, TailwindCSS, Vercel AI SDK.
- **Source Brief:** [`claude_api_developer_client_facing_assistant_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_api_developer_client_facing_assistant_brief.md)

---

## Project 2.3: Production Dual-Layer Web Application
- **Target Offer / Domain:** Custom web product where Claude acts as both the rapid development engine and an embedded intelligence feature.
- **Core Architecture:**
  - Modular full-stack application engineered with Claude Code.
  - Live embedded Claude intelligence layer for content generation, document synthesis, and automated business workflows.
  - Secure server-side API key proxying, rate-limiting, custom domain routing, and comprehensive developer documentation.
- **Tech Stack:** Next.js (TypeScript) / Node.js or Python FastAPI, TailwindCSS, PostgreSQL / Supabase, Anthropic SDK.
- **Source Brief:** [`experienced_claude_developer_custom_web_product_brief.md`](file:///Users/kalmin/startups/claude-spectra/experienced_claude_developer_custom_web_product_brief.md)

---

# Track 3: Enterprise Workflow Automation & Systems Integration

## Project 3.1: ERPNext / Frappe Claude MCP Agent & Approval Gatekeeper
- **Target Offer / Domain:** Enterprise ERP automation across Sales, CRM, Accounting, Inventory, and HR.
- **Core Architecture:**
  - Custom Frappe application exposing Model Context Protocol (MCP) tool calling endpoints to Claude.
  - Agent performs complex queries, financial report synthesis, and exception detection.
  - **Human-in-the-Loop Approval Gate:** Sensitive database mutations (Journal Entries, Purchase Orders, credit updates) generate draft proposals and diff summaries requiring managerial approval prior to commit.
  - Enforces native Frappe Role-Based Access Control (RBAC).
- **Tech Stack:** Python, Frappe Framework / ERPNext, MariaDB, Anthropic Claude API (MCP / Tool Calling), Redis / RQ background workers.
- **Source Brief:** [`erpnext_developer_claude_ai_agent_integration_brief.md`](file:///Users/kalmin/startups/claude-spectra/erpnext_developer_claude_ai_agent_integration_brief.md)

```
+-----------------------------------------------------------------------------------+
|                        ERPNEXT + CLAUDE AGENTIC ARCHITECTURE                      |
+-----------------------------------------------------------------------------------+
|  [ERP Event / Query] ──> [Claude MCP Orchestrator] ──> [Analytical / Read Tools] |
|                                   │                                               |
|                                   v                                               |
|  [Master DB Updated] <── [Manager Approval Gate] <── [Action / Mutation Tools]    |
+-----------------------------------------------------------------------------------+
```

---

## Project 3.2: SharePoint Excel Cloud Tracker & Power Automate AI Copilot
- **Target Offer / Domain:** Global operational tracking spreadsheet stored in Microsoft SharePoint / Excel Online.
- **Core Architecture:**
  - **100% Cloud-Native M365 Portability:** Operates natively in SharePoint without relying on local developer scripts.
  - Power Automate cloud flows + Office Scripts (TypeScript) connecting Excel Online to Claude API.
  - Automated status tracking (`Open` $\rightarrow$ `In Progress` $\rightarrow$ `Closed`), formula calculations, and duplicate detection.
  - Natural language Q&A interface in Teams/Excel (*"Show me all overdue actions for APAC"*).
  - Automated email reminders via Outlook and management escalations via Teams.
- **Tech Stack:** Microsoft SharePoint, Excel Online (Graph API), Power Automate Cloud Flows, Office Scripts (TypeScript), Anthropic Claude REST API.
- **Source Brief:** [`excel_sharepoint_automation_claude_ai_tracker_brief.md`](file:///Users/kalmin/startups/claude-spectra/excel_sharepoint_automation_claude_ai_tracker_brief.md)

---

## Project 3.3: Natural Language Google Sheets Auto-Fill Connector
- **Target Offer / Domain:** In-sheet and desktop natural language spreadsheet automation for e-commerce and operations.
- **Core Architecture:**
  - User pastes raw, unstructured text (supplier lists, orders, customer notes) into Claude Desktop or an in-sheet sidebar.
  - Claude understands target spreadsheet column schemas, normalizes data, and executes programmatic batch writes (`append_row` / `update_cells`) via Google Sheets API.
- **Tech Stack:** Claude Desktop Google Sheets MCP Server, Google Apps Script, Google Sheets REST API, OAuth2.
- **Source Brief:** [`claude_ai_google_sheets_auto_fill_integration_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_ai_google_sheets_auto_fill_integration_brief.md)

---

# Track 4: Developer Tooling, Multi-Session Orchestration & Swarms

## Project 4.1: Claude Code Multi-Session Orchestration Console & Notification Plane
- **Target Offer / Domain:** Centralized management plane for running multiple concurrent Claude Code CLI instances across separate accounts.
- **Core Architecture:**
  - **Headless Supervisor Daemon:** Wraps CLI instances with stdout stream listeners.
  - **Notification & Remote Reply Loop:** Alerts operator via Telegram/Slack when a session halts on an interactive prompt/approval; user replies on mobile to resume context stream.
  - **Multi-Tab Web Console:** Single web dashboard (`xterm.js`) to switch between sessions seamlessly.
  - **Multi-Tenant Cloud Config Isolation:** Injects account-specific `.env` secrets and MCP connectors via Doppler / Infisical.
- **Tech Stack:** Node.js / Python Daemon, WebSockets, Next.js / xterm.js, Telegram / Slack Bot API, Infisical / Doppler.
- **Source Brief:** [`claude_code_multi_session_orchestration_console_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_code_multi_session_orchestration_console_brief.md)

```
+-----------------------------------------------------------------------------------+
|                        OPTION 1: AGENT DAEMON & BOT PLANE                         |
+-----------------------------------------------------------------------------------+
|  [Multi-Account CLI Daemons] ──> [Session Event Router]                           |
|                                         │                                         |
|         +───────────────────────────────┴───────────────────────────────+         |
|         v                                                               v         |
|  [Web Terminal Console (xterm.js)]                 [Slack/Telegram Remote Reply]  |
+-----------------------------------------------------------------------------------+
```

---

## Project 4.2: Multi-Client Agent Swarm Architecture & Token Optimization
- **Target Offer / Domain:** Scaling software engineering and content delivery across 6 concurrent client workloads.
- **Core Architecture:**
  - Directory structure isolating client rules (`CLAUDE.md`) and `.claudeignore` to eliminate token bloat.
  - Hierarchical swarm orchestration: Leader orchestrator delegating to specialized worker subagents operating in isolated Git worktrees.
  - Automated verification loops (linters, unit test suites, type-checkers) before human sign-off.
- **Tech Stack:** Claude Code CLI, Git Worktrees, Python / Bash automation, MCP tools, Jest / Pytest.
- **Source Brief:** [`claude_code_specialist_sparring_agent_swarms_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_code_specialist_sparring_agent_swarms_brief.md)

---

## Project 4.3: Windows & WSL2 Developer Environment Tuning & Coaching Framework
- **Target Offer / Domain:** Optimizing developer workstations for high-efficiency Claude Code agentic coding.
- **Core Architecture:**
  - Benchmarking native Windows vs. WSL2 Ubuntu I/O and terminal setups.
  - Fast CLI navigation tooling (`fzf`, `ripgrep`, `fd`, Starship prompt).
  - Local MCP server authoring (PostgreSQL, Git, Filesystem, Browser automation) on Windows.
  - Context hygiene protocols, token budgeting, and TDD agentic refactoring loops.
- **Tech Stack:** Windows 11, WSL2 (Ubuntu), Windows Terminal, PowerShell, Node.js, Python, MCP SDK.
- **Source Brief:** [`ai_agentic_development_claude_code_windows_coaching_brief.md`](file:///Users/kalmin/startups/claude-spectra/ai_agentic_development_claude_code_windows_coaching_brief.md)

---

# Track 5: AI Media, Content Engines & Automated Video Pipelines

## Project 5.1: Football YouTube Shorts Pipeline (Claude Code + ElevenLabs + CapCut)
- **Target Offer / Domain:** Automated storytelling YouTube Shorts generation for sports media channels.
- **Core Architecture:**
  - Claude Code generates 50-second retention-optimized narrative scripts and structured scene breakdown tables.
  - ElevenLabs API produces deep cinematic voiceovers with word-level timestamps.
  - Automated asset matching against categorized football highlight B-roll libraries.
  - Programmatic video assembly / CapCut draft automation with dynamic word-by-word highlighted captions, sound effects, and motion zooms.
- **Tech Stack:** Claude Code / Claude 3.5 Sonnet, ElevenLabs API, Python (`moviepy`, `ffmpeg`), CapCut Desktop automation, YouTube Data API.
- **Source Brief:** [`system_claude_code_capcut_youtube_shorts_automation_brief.md`](file:///Users/kalmin/startups/claude-spectra/system_claude_code_capcut_youtube_shorts_automation_brief.md)

```
+-----------------------------------------------------------------------------------+
|                           END-TO-END AUTOMATION PIPELINE                          |
+-----------------------------------------------------------------------------------+
|  [Claude Code Script] ──> [ElevenLabs Voiceover] ──> [Clip Sourcing Automation]   |
|                                                              │                    |
|  [Rendered YouTube Short / CapCut Draft] <── [FFmpeg / CapCut Assembly Engine]    |
+-----------------------------------------------------------------------------------+
```

---

## Project 5.2: High-Velocity AI Video Pipeline (Higgsfield + FFmpeg + Claude)
- **Target Offer / Domain:** High-volume cinematic commercial short production (hundreds of 20–30s clips).
- **Core Architecture:**
  - Higgsfield / Seedance video generation using consistent character reference packs.
  - Claude / ChatGPT prompt copilot: surgical prompt rewriting to fix visual defects without expensive random re-rolls.
  - Fast CLI post-processing in FFmpeg (9:16 crop, concatenation, subtitle burning, loudness normalization).
  - Strict Quality Control (QC) sentry checking for identity drift, artifact warping, and audio sync before marking complete.
- **Tech Stack:** Higgsfield / Seedance API, Kling, FAL.ai, Claude 3.5 Sonnet, FFmpeg CLI, Python automation.
- **Source Brief:** [`ai_video_pipeline_operator_higgsfield_ffmpeg_claude_brief.md`](file:///Users/kalmin/startups/claude-spectra/ai_video_pipeline_operator_higgsfield_ffmpeg_claude_brief.md)

---

## Project 5.3: Multi-Brand Instagram AI Marketing Director & Content Engine
- **Target Offer / Domain:** Regional Sports Group managing 5 distinct sub-brands (*Regional Sports, Wolves Academy, Al Maha, Fitfam, RSM*).
- **Core Architecture:**
  - Context-isolated Claude Projects storing brand guidelines, visual palettes, and target demographics for each sub-brand.
  - Ingests Meta/Instagram Graph API metrics to produce weekly executive performance digests.
  - Generates 7-day multi-format content calendars, viral hooks, captions, and on-field videographer filming shot-lists.
  - Connects Canva MCP for visual mockup generation and audits Meta Ads performance to recommend budget shifts and creative refreshes.
- **Tech Stack:** Anthropic Claude Projects / API, Meta Graph API, Canva MCP, Meta Business Suite, Metricool.
- **Source Brief:** [`claude_ai_marketing_director_instagram_sports_group_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_ai_marketing_director_instagram_sports_group_brief.md)

---

# Track 6: AI Design Systems, Workspace Operations & Education

## Project 6.1: Brand Design System as Code (React Components + Design Tokens)
- **Target Offer / Domain:** Converting corporate PowerPoint and PDF brand books into a machine-readable code repository for Claude Design.
- **Core Architecture:**
  - Programmatic extraction of color palettes, font stacks, and spatial rules from PowerPoint theme XML (`ppt/theme/theme1.xml`).
  - Master `tokens.json` and semantic CSS custom properties (`tokens.css`).
  - 10+ Tokenized React UI components (Button, Card, Table, Typography, KPI Block, Chart Wrapper, Header, Footer) with **zero hardcoded values**.
  - 3 department page layout templates and an LLM-optimized `README.md` containing explicit constraints so Claude Design outputs flawless on-brand artifacts.
- **Tech Stack:** React, TypeScript, CSS Custom Properties / Design Tokens, Vite / Storybook, XML / python-pptx parser.
- **Source Brief:** [`claude_ai_design_system_react_tokens_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_ai_design_system_react_tokens_brief.md)

```
brand-system/
├── README.md                 # Machine-readable brand rules for Claude Design
├── tokens/tokens.json        # Design token definitions
├── src/styles/tokens.css     # CSS Custom Properties (--color-surface-primary, etc.)
├── src/components/           # 10+ strictly tokenized React components
└── src/layouts/              # 3 Department page templates
```

---

## Project 6.2: Multi-Company Claude Cowork & Skills Executive Assistant
- **Target Offer / Domain:** Multi-business operator managing marketing, operations, proposals, and CRM.
- **Core Architecture:**
  - Multi-company workspace hierarchy separating corporate knowledge bases across distinct entities.
  - Custom Claude Skills with explicit input schemas and standardized output formats for proposals, email triage, and CRM logging.
  - MCP connectors wiring Claude directly to **Microsoft 365 / Outlook**, **GoHighLevel (GHL)**, **Gamma AI**, and **Make.com**.
  - Scheduled background tasks for daily morning executive briefings and pipeline status checks.
- **Tech Stack:** Claude Cowork / Projects, Custom Claude Skills, Model Context Protocol (MCP), Microsoft 365, GoHighLevel, Make.com.
- **Source Brief:** [`claude_cowork_expert_live_setup_configuration_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_cowork_expert_live_setup_configuration_brief.md)

---

## Project 6.3: Studio 2-Hour Video Masterclass Course Production
- **Target Offer / Domain:** Comprehensive developer course on Claude AI engineering for founders and engineers.
- **Core Architecture:**
  - 5-module syllabus covering Claude Architecture & Context Economics, Product PRDs & Spec Engineering, Hands-On Development with Claude Code, Advanced Tooling & MCP, and Production Deployment QC.
  - 4K screen capture paired with studio-grade talking-head presentation and broadcast-standard audio mastering (-14 LUFS).
  - Downloadable student starter code repositories, prompt cheat-sheets, and interactive exercise files.
- **Tech Stack:** Screenflow / OBS Studio, Adobe Premiere Pro / DaVinci Resolve, Shure SM7B Audio Chain, Claude Code CLI, Next.js starter repo.
- **Source Brief:** [`claude_video_masterclass_course_creator_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_video_masterclass_course_creator_brief.md)

---

## Complete Workspace Briefs Master Index
All original individual detailed briefs are maintained in this workspace:
1. [`autonomous_claude_marketing_sales_agent_swarm_brief.md`](file:///Users/kalmin/startups/claude-spectra/autonomous_claude_marketing_sales_agent_swarm_brief.md)
2. [`claude_n8n_lead_management_automation_gohighlevel_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_n8n_lead_management_automation_gohighlevel_brief.md)
3. [`autonomous_claude_agent_email_attachments_google_drive_brief.md`](file:///Users/kalmin/startups/claude-spectra/autonomous_claude_agent_email_attachments_google_drive_brief.md)
4. [`full_stack_ai_developer_claude_canva_business_dashboard_brief.md`](file:///Users/kalmin/startups/claude-spectra/full_stack_ai_developer_claude_canva_business_dashboard_brief.md)
5. [`claude_api_developer_client_facing_assistant_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_api_developer_client_facing_assistant_brief.md)
6. [`experienced_claude_developer_custom_web_product_brief.md`](file:///Users/kalmin/startups/claude-spectra/experienced_claude_developer_custom_web_product_brief.md)
7. [`erpnext_developer_claude_ai_agent_integration_brief.md`](file:///Users/kalmin/startups/claude-spectra/erpnext_developer_claude_ai_agent_integration_brief.md)
8. [`excel_sharepoint_automation_claude_ai_tracker_brief.md`](file:///Users/kalmin/startups/claude-spectra/excel_sharepoint_automation_claude_ai_tracker_brief.md)
9. [`claude_ai_google_sheets_auto_fill_integration_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_ai_google_sheets_auto_fill_integration_brief.md)
10. [`claude_code_multi_session_orchestration_console_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_code_multi_session_orchestration_console_brief.md)
11. [`claude_code_specialist_sparring_agent_swarms_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_code_specialist_sparring_agent_swarms_brief.md)
12. [`ai_agentic_development_claude_code_windows_coaching_brief.md`](file:///Users/kalmin/startups/claude-spectra/ai_agentic_development_claude_code_windows_coaching_brief.md)
13. [`system_claude_code_capcut_youtube_shorts_automation_brief.md`](file:///Users/kalmin/startups/claude-spectra/system_claude_code_capcut_youtube_shorts_automation_brief.md)
14. [`ai_video_pipeline_operator_higgsfield_ffmpeg_claude_brief.md`](file:///Users/kalmin/startups/claude-spectra/ai_video_pipeline_operator_higgsfield_ffmpeg_claude_brief.md)
15. [`claude_ai_marketing_director_instagram_sports_group_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_ai_marketing_director_instagram_sports_group_brief.md)
16. [`claude_ai_design_system_react_tokens_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_ai_design_system_react_tokens_brief.md)
17. [`claude_cowork_expert_live_setup_configuration_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_cowork_expert_live_setup_configuration_brief.md)
18. [`claude_video_masterclass_course_creator_brief.md`](file:///Users/kalmin/startups/claude-spectra/claude_video_masterclass_course_creator_brief.md)
