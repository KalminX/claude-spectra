# Comprehensive Opportunity & Job Brief: Claude & n8n Lead Management Automation (GoHighLevel)

## 1. Executive Summary & Opportunity Overview
- **Project Title:** Claude Code & n8n AI Automation Developer Needed
- **Engagement Model:** Fixed-Price Milestone ($600.00, Intermediate tier with explicit **Contract-to-Hire** potential for ongoing agency automation).
- **Core Objective:** Build an end-to-end, enterprise-grade inbound lead processing and qualification engine using **n8n** and **Anthropic Claude (Claude 3.5 Sonnet)** that captures leads across multi-channel ad campaigns (Facebook Lead Ads, Typeform, web forms), enriches and scores them with AI, syncs records into **GoHighLevel (GHL)**, notifies sales reps in Slack, and triggers personalized email sequences.
- **Listing Source:** Upwork (Job URL: `https://www.upwork.com/jobs/~022084319561951551556`)
- **Required Connects:** 11 | **Competition:** 50+ proposals | **Activity:** 0 interviewing.

---

## 2. Client Profile & Business Context
- **Client Location:** Ibadan, Nigeria (WAT — UTC+1 timezone).
- **Business Domain:** Fast-growing digital marketing and lead generation agency running high-volume paid media campaigns for multiple B2B/B2C clients.
- **Strategic Pain Point:** Rising lead volume has created manual administrative bottlenecks in lead qualification, CRM entry, and rep routing, slowing response times and pulling the internal team away from closing deals.
- **Future Engagement:** Successful delivery of this pipeline serves as the foundation for broader agency internal tooling and long-term automation contracts.

---

## 3. End-to-End System Architecture Blueprint

```
+-----------------------------------------------------------------------------------+
|                        N8N + CLAUDE LEAD AUTOMATION ENGINE                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [MULTI-CHANNEL INGESTION]                                                        |
|  Facebook Lead Ads Webhook ──┐                                                    |
|  Typeform Submission Hook ───┼──> [n8n Master Ingestion Webhook]                  |
|  Website Forms (Elementor) ──┘           │                                        |
|                                          v                                        |
|                             [Step 1: Data Normalization]                          |
|                             Clean phone/email, deduplicate records                |
|                                          │                                        |
|                                          v                                        |
|                             [Step 2: Enrichment API]                              |
|                             Apollo / Clearbit / Hunter API data fetch             |
|                                          │                                        |
|                                          v                                        |
|                             [Step 3: Claude AI Engine]                            |
|                             - Anthropic Claude 3.5 Sonnet API                     |
|                             - Lead Fit & Intent Scoring (0–100)                   |
|                             - Executive 3-bullet Lead Summary                     |
|                             - Output: Strict JSON Schema                          |
|                                          │                                        |
|         +────────────────────────────────+────────────────────────────────+       |
|         │                                │                                │       |
|         v                                v                                v       |
|  [Step 4: GoHighLevel]         [Step 5: Team Alert]            [Step 6: Follow-up]|
|  - Create/Update Contact       - Formatted Slack Alert         - Trigger Smart    |
|  - Set Opportunity Stage       - Lead Score & Summary          - Email Sequence   |
|  - Assign to Sales Rep         - 1-Click Action Buttons        - SMS / WhatsApp   |
|         │                                │                                │       |
|         +────────────────────────────────┴────────────────────────────────+       |
|                                          │                                        |
|                                          v                                        |
|                       [Step 7: Analytics & Data Logging]                          |
|                       Airtable / Google Sheets Master Reporting                   |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 4. Scope of Work & Technical Deliverables

### A. Ingestion & Pre-Processing Layer
- **Multi-Source Webhook Listeners:** Configuring reliable n8n webhook nodes for Facebook Graph API Lead Ads, Typeform responses, and custom WordPress/HTML forms.
- **Data Hygiene & Deduplication:** Normalizing phone numbers (E.164), cleaning email strings, and checking existing records in CRM to avoid duplicates.

### B. Enrichment & Claude AI Scoring Layer
- **Third-Party Data Enrichment:** Calling enrichment APIs (Apollo.io, Hunter, Clearbit) to append company size, industry, revenue, and job titles.
- **Claude 3.5 Sonnet Prompt Architecture:**
  - Structured prompt analyzing lead inputs against Ideal Customer Profile (ICP) criteria.
  - Generates numerical Lead Score (1–100), Tier category (Hot / Warm / Disqualified), and a concise 3-bullet executive briefing.
  - Strict JSON mode output schema for 100% deterministic downstream parsing.

### C. CRM & Pipeline Routing Layer (GoHighLevel)
- **GoHighLevel API v2 Integration:**
  - Automatically creating or updating Contacts, Custom Fields, and Notes.
  - Moving leads to the appropriate Pipeline Stage (e.g., *New Inbound*, *Hot Qualified*, *Nurture*).
  - Dynamic user assignment: Round-robin or rules-based routing to specific sales reps based on lead geography, budget, or service line.

### D. Multi-Channel Notifications & Nurturing
- **Interactive Slack Notifications:** Rich Block Kit formatting in designated Slack channels featuring lead name, company, score badge, Claude summary, and a direct link to the GHL record.
- **Automated Follow-Up Sequences:** Triggering tailored email/SMS sequences in GoHighLevel or SendGrid based on the AI-assigned lead tier.

### E. Reporting, Error Handling & Governance
- **Centralized Data Warehousing:** Real-time logging of all incoming leads, scores, timestamps, and routing decisions in Google Sheets or Airtable.
- **Enterprise Resilience in n8n:**
  - Dedicated Error Trigger workflows with automated Slack/Email alerts if an upstream API fails.
  - Automated retry queues for temporary rate limits (HTTP 429) or network timeouts.

---

## 5. Technology Stack Summary

| Layer | Recommended Technology |
| :--- | :--- |
| **Workflow Orchestrator** | n8n (Self-Hosted Docker or n8n Cloud) |
| **AI Intelligence Engine** | Anthropic Claude API (`claude-3-5-sonnet`) / Claude Code |
| **CRM & Automation** | GoHighLevel (GHL) REST API v2 |
| **Data Enrichment** | Apollo.io / Clearbit / Hunter APIs |
| **Internal Notifications**| Slack Webhooks / Slack API (Block Kit) |
| **Reporting & Logging** | Google Sheets API / Airtable API |

---

## 6. Proposal Strategy & Submission Answers

### Screening Question 1: Similar Projects in Scope
*Highlight a specific case study of a production n8n lead engine:*
> *"Built an enterprise lead intake pipeline in n8n connecting Meta Lead Ads and Typeform to Claude 3.5 Sonnet for real-time lead qualification and scoring, enriching records via Apollo API, syncing opportunities into GoHighLevel, and dispatching rich Block Kit Slack alerts to reps in under 3 seconds."*

### Screening Question 2: Recent Relevant Experience
*Detail technical depth across the required stack:*
> *"Extensive hands-on experience building complex n8n workflows with custom JavaScript function nodes, OAuth2 credential management, error-handling sub-workflows, GoHighLevel API v2 endpoints (Contacts, Pipelines, Custom Fields), and deterministic Claude JSON schemas for AI scoring."*

### Value-Add Positioning
- Reassure the client on clean architecture, modular n8n node structure, full documentation, and post-launch support as part of the transition into long-term contract-to-hire automation.
