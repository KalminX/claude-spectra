# Comprehensive Opportunity & Job Brief: Full-Stack AI Developer — Claude + Canva + Business Dashboard

## 1. Executive Summary & Opportunity Overview
- **Project Title:** Full-Stack AI Developer — Claude + Canva + Business Dashboard (Module 1)
- **Engagement Model:** Fixed-Price Milestone ($50.00 initial paid module with strong **Contract-to-Hire** progression for ongoing platform phases; Intermediate tier).
- **Core Objective:** Architect and develop **Module 1** of an AI-powered business operations suite. Module 1 focuses on building a production-grade full-stack dashboard foundation (Next.js/TypeScript/PostgreSQL) and integrating the official **Claude + Canva AI Connector / MCP (Model Context Protocol)** to enable automated, brand-aligned editable design creation from natural language prompts.
- **Listing Source:** Upwork (Job URL: `https://www.upwork.com/jobs/~022093794762280221271`)
- **Required Connects:** 9 | **Competition:** 10–15 proposals | **Activity:** 1 hire recorded, 5 interviewing, 3 invites sent.

---

## 2. Client Profile & Strategic Roadmap
- **Client Location:** Gujranwala, Pakistan (PKT — UTC+5 timezone).
- **Platform Track Record:** 100% hire rate, payment and phone verified, 2 active hires.
- **Project Philosophy:** Quality and architectural rigor over bloated, half-finished features. The client emphasizes validating official platform capabilities (specifically the official Claude + Canva Teams integration) rather than fabricating unsupported custom workarounds.
- **Pre-Development Gate:** The client requires a structured technical architecture plan across 9 specific dimensions before full implementation begins.

---

## 3. Module 1 Architectural Framework & Deliverables

```
+-----------------------------------------------------------------------------------+
|                  CLAUDE + CANVA BUSINESS PLATFORM (MODULE 1)                      |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Authenticated Dashboard UI] (Next.js 14 / TypeScript / TailwindCSS / shadcn/ui) |
|   ├── 1. Overview / Metrics Hub                                                   |
|   ├── 2. Claude Design Studio                                                     |
|   ├── 3. Company & Brand Knowledge Manager                                        |
|   └── 4. Workspace & Role Settings                                                |
|                               │                                                   |
|                               v                                                   |
|  [Backend API & Security Orchestrator] (Node.js Route Handlers / PostgreSQL DB)   |
|   ├── Role-Based Access Control (Admin / Manager / Staff)                         |
|   ├── Secure Server-Side Anthropic API Key & OAuth Token Storage                  |
|   └── Brand Knowledge Retrieval Engine (System Prompt Context Assembly)           |
|                               │                                                   |
|                               v                                                   |
|  [Claude Intelligence Layer] (Claude 3.5 Sonnet / Claude Messages API)            |
|   ├── Ingests Brand Guidelines (Voice, Hex Colors, Typography, Logo Assets)       |
|   ├── Interprets Natural Language Design Request                                  |
|   └── Formulates Canva MCP Tool Calls (Search, Template Selection, Asset Binding) |
|                               │                                                   |
|                               v                                                   |
|  [Official Canva Teams MCP / Connectors Integration]                              |
|   ├── Query & Select Brand Kit / Templates                                         |
|   ├── Generate / Populate Editable Canva Design URL                               |
|   └── Return Live Canva Edit Link to Dashboard for Human Review & Export          |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 4. Deep-Dive: The 5 Core Functional Pillars

### 1. Professional Dashboard Foundation
- **UI/UX:** Clean, modular interface built with Next.js App Router, React, TypeScript, and TailwindCSS (using shadcn/ui components).
- **Information Architecture:** Four distinct navigation views:
  - `Overview`: Recent design generations, usage stats, quick actions.
  - `Claude Design`: The interactive design studio and generation queue.
  - `Company Knowledge`: Admin-editable brand, product, and asset repository.
  - `Settings`: User profiles, API credentials, and workspace settings.

### 2. Claude AI & Security Architecture
- **Anthropic Integration:** Claude 3.5 Sonnet via official Anthropic SDK for high-fidelity prompt reasoning and tool calling.
- **Security:** Zero client-side API key exposure; all LLM calls routed through server-side proxy routes with strict input sanitization.

### 3. Claude + Canva Official Integration (The Core Feature)
- **Target User Flow:** `User Prompt` $\rightarrow$ `Dashboard` $\rightarrow$ `Claude Context Assembly` $\rightarrow$ `Canva MCP Call` $\rightarrow$ `Editable Canva Design URL` $\rightarrow$ `Human Review/Refinement`.
- **Supported Capabilities to Leverage:**
  - Referencing Canva Teams Brand Kits (colors, fonts, logos).
  - Searching existing templates and assets in Canva.
  - Generating editable design drafts (social posts, banners, marketing collateral).
  - Returning direct deep links into Canva for final human touch-ups.

### 4. Company & Brand Knowledge Base
- **Admin Configuration Interface:** An easy-to-update management module storing:
  - Company overview, product/service descriptions.
  - Brand voice guidelines and copy rules.
  - Visual guidelines: primary/secondary hex palettes, typography, SVG/PNG logo URLs.
  - Sample high-performing designs and specialized AI system instructions.

### 5. Authentication & Role-Based Access Control (RBAC)
- **Auth Layer:** NextAuth.js / Supabase Auth / Clerk supporting secure email/password and OAuth.
- **Permissions:** Three distinct roles:
  - **Admin:** Full access (Knowledge base edits, API key config, user management).
  - **Manager:** Create/review designs, manage templates, view team activity.
  - **Staff:** Submit design requests, view generated designs.

---

## 5. Pre-Development Technical Plan Framework
*The 9-point plan to deliver prior to code execution:*
1. **Dashboard Architecture:** Component tree, server vs. client boundaries, database schema.
2. **Claude Integration Approach:** System prompt structuring, prompt caching, token budgets.
3. **Canva Connector Approach:** Authentication/OAuth bridge, MCP server endpoints, tool calling schemas.
4. **Auth & RBAC Schema:** User roles, session middleware, protected route enforcement.
5. **Knowledge Base Schema:** JSON/PostgreSQL schema for dynamic brand asset injection.
6. **Recommended Tech Stack:** Next.js (TypeScript), TailwindCSS, PostgreSQL (Prisma/Drizzle), NextAuth.js, Anthropic SDK.
7. **Current Canva Capabilities:** Verified feature set supported under the Canva Teams AI Connector.
8. **Limitations & Risks:** Canva API rate limits, OAuth token refresh cycles, template customization boundaries.
9. **Module 1 Delivery Schedule:** 5–7 day milestone breakdown.

---

## 6. Proposal Strategy & Answers to Mandatory Questions

1. **Experience with Claude/Anthropic:** Detail production builds with Claude 3.5 Sonnet, prompt caching, structured JSON schemas, and streaming Messages API.
2. **Experience with MCP:** Cite concrete examples of local/remote MCP servers built (e.g., PostgreSQL, Git, filesystem, third-party REST MCP bridges).
3. **Canva AI Integration Experience:** Describe experience with the Canva Developer Platform / Connect APIs and Canva AI integrations.
4. **Approach to Claude + Canva:** Prioritize the official Canva MCP / Connect integration, testing Canva Teams Brand Kit endpoints and returning direct editable design links.
5. **Recommended Stack & Rationale:** Next.js (App Router) + TypeScript + TailwindCSS + PostgreSQL. Provides unified full-stack architecture, rapid iteration, and enterprise security.
6. **Relevant Projects:** Share 2–3 live URLs / repos of full-stack AI dashboards.
7. **Estimated Timeline:** 5 to 7 business days for a polished Module 1 release.
8. **Key Risks & Mitigations:** Documenting Canva API endpoint limitations upfront and establishing graceful fallback to Canva template deep-linking.
