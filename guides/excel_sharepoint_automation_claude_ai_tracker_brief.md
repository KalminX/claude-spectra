# Comprehensive Opportunity & Job Brief: Excel & SharePoint Automation Using Claude AI

## 1. Executive Summary & Opportunity Overview
- **Project Title:** Automation of Existing SharePoint Excel Tracker Using Claude AI
- **Engagement Model:** Fixed-Price Milestone ($10.00 initial feasibility/discovery milestone with ongoing implementation; Intermediate tier).
- **Core Objective:** Transform an existing, manually intensive Microsoft Excel operational tracking spreadsheet stored in Microsoft SharePoint into a secure, automated, and globally accessible management system powered by Anthropic Claude and Microsoft 365 cloud automation (Power Automate, Office Scripts, Teams/Outlook).
- **Listing Source:** Upwork (Job URL: `https://www.upwork.com/jobs/~022094833903259408397` / `https://www.upwork.com/jobs/~022090109754424905803`)
- **Required Connects:** 11 | **Competition:** 10–15 proposals | **Activity:** 1 interviewing.

---

## 2. Client Profile & Non-Negotiable Core Requirement
- **Client Location:** Singapore (SGT — UTC+8 timezone).
- **Platform Track Record:** 4.71 / 5.00 rating across 7 reviews, 30 jobs posted, 34% hire rate.
- **The Non-Negotiable Constraint (Global Cloud Portability):**
  - The solution **must not** rely on Python scripts running locally on an individual developer's computer.
  - The final solution must reside natively within the company’s **Microsoft 365 / SharePoint environment**, allowing global team members across APAC, EMEA, and Americas to collaborate concurrently through Excel Online / SharePoint without installing custom desktop software.

---

## 3. End-to-End System Architecture Blueprint

```
+-----------------------------------------------------------------------------------+
|               MICROSOFT 365 & SHAREPOINT + CLAUDE AI ARCHITECTURE                 |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Central SharePoint Document Library] (Single Controlled Source of Truth)        |
|  └── Master Operational Tracker (.xlsx in Excel Online)                           |
|            │                                                                      |
|            ├── (Trigger: Schedule / Data Mutation / User Action)                  |
|            │                                                                      |
|            v                                                                      |
|  [Microsoft Power Automate Cloud Engine] (M365 Integration Layer)                 |
|  ├── Read/Write rows via Microsoft Graph API / Excel Online (Business) Connector  |
|  ├── Office Scripts (TypeScript) for high-speed calculation & formatting         |
|  └── Custom HTTP / Secure REST Connector $\rightarrow$ Anthropic Claude API      |
|            │                                                                      |
|            v                                                                      |
|  [Anthropic Claude Intelligence Layer] (Claude 3.5 Sonnet / Haiku)                |
|  ├── Ingests spreadsheet records, comments & regional metadata                    |
|  ├── Automated Data Quality Audit (Missing fields, duplicates, status flags)      |
|  ├── Natural-Language Query Engine ("Summarize overdue actions in APAC")         |
|  └── Executive Narrative Synthesis (Monthly/Quarterly management briefs)          |
|            │                                                                      |
|            +───────────────────────+───────────────────────+                      |
|            │                       │                       │                      |
|            v                       v                       v                      |
|  [M365 Notifications]      [Human Approval Gate]   [Interactive AI Query Hub]     |
|  - Outlook Email Alerts    - Power Automate        - Microsoft Teams Bot /        |
|  - Teams Channel Pushes      Approvals before        Excel Script Web Sidebar     |
|  - Escalations to Owners     mutating master data  - Direct Q&A on live data      |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 4. Scope of Work & The 10 Functional Modules

### 1. Existing Workflow & Spreadsheet Audit
- Map all worksheet tabs, column data types, formulas, lifecycle statuses, and current manual reporting overhead.

### 2. Claude AI Core Integration
- Secure connection between SharePoint/Excel Online and Claude API to analyze records, categorize issues, and answer natural language inquiries.

### 3. Automated Routine Spreadsheet Operations
- Automated calculations: completion percentages, automated lifecycle progression (`Open` $\rightarrow$ `In Progress` $\rightarrow$ `Pending` $\rightarrow$ `Closed`), duplicate detection, and missing field alerts.

### 4. Global Cloud SharePoint Deployment
- Zero local software dependencies. Deployed as a native M365 package (Power Automate flows + Office Scripts) that inherits existing SharePoint permissions and role-based access control (RBAC).

### 5. Natural Language Querying Engine
- Enables stakeholders to ask plain-English questions (e.g., *"Which site has the highest number of overdue actions?"*, *"Summarize this month's performance vs. last quarter"*) and receive instant, data-backed summaries.

### 6. Automated Action Lifecycle & Overdue Tracking
- Automated daily crons evaluating due dates against current timestamps, tagging overdue rows, and escalating long-outstanding items.

### 7. Multi-Channel M365 Notification System
- Automated notification dispatch via **Microsoft Outlook** (personalized email reminders to action owners) and **Microsoft Teams** (management alerts for high-priority items).

### 8. Executive Dashboard & Narrative Management Reports
- Automated KPI summary tab in Excel + Claude-authored monthly executive briefs highlighting macro trends, systemic risks, and required management interventions.

### 9. SharePoint Data Integrity & Version Control
- Preserves native SharePoint version history, change audit trails, and concurrent co-authoring without file-locking issues.

### 10. Enterprise Security & AI Governance
- **Human-in-the-Loop:** Critical record modifications and status closures require user confirmation. Zero destructive automated overwrites.

---

## 5. Technical Implementation Approaches

| Approach | Technology | Pros | Best For |
| :--- | :--- | :--- | :--- |
| **Option A (Recommended): Power Automate + Claude API** | Power Automate Cloud Flow + Excel Online Connector + Claude REST API | 100% cloud native, zero installation for users, enterprise M365 security, automated email/Teams triggers. | End-to-end global automation and scheduled tracking. |
| **Option B: Excel Office Scripts + API Webhook** | Office Scripts (TypeScript) inside Excel Online | Executes directly within the Excel browser interface with 1-click execution. | In-sheet data validation and real-time formatting. |
| **Option C: Microsoft Teams AI Assistant Hub** | Power Virtual Agents / Teams Bot + Power Automate + Claude | Allows team members to query the SharePoint Excel data directly from Microsoft Teams chat. | Executive mobile and desktop natural language Q&A. |

---

## 6. Proposal Strategy & Submission Blueprint
1. **Directly Address the Portability Mandate in Line 1:** Reassure the client that your architecture uses **native Microsoft 365 cloud tools (Power Automate + Office Scripts + Claude API)** so that any authorized global user can access it directly in SharePoint without local script execution.
2. **Detail the Governance & Safety Model:** Explain your human-in-the-loop validation process ensuring Claude never overwrites master rows without approval.
3. **Outline the Delivery Milestones:**
   - *Milestone 1:* Workbook review, schema mapping, and Power Automate-to-Claude API pipeline setup.
   - *Milestone 2:* Automated overdue tracking, Outlook/Teams notification flows, and NL query interface.
   - *Milestone 3:* Executive dashboard, UAT testing in SharePoint, and handover documentation.
