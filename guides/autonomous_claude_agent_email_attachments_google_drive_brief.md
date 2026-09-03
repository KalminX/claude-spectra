# Comprehensive Opportunity & Job Brief: Autonomous Claude Agent for Email Attachments & Google Drive

## 1. Executive Summary & Opportunity Overview
- **Project Title:** Autonomous Claude agent for email attachments and Google Drive
- **Engagement Model:** Fixed-Price One-Time Milestone ($50.00, Entry / Streamlined scope).
- **Core Objective:** Build a fully autonomous background pipeline that ingests incoming email attachments (invoices, signed contracts, supplier reports), leverages Anthropic Claude to inspect document content and metadata, automatically renames files using a strict standardized taxonomy, and uploads them to the correct designated Google Drive folders without requiring manual approval.
- **Listing Source:** Upwork (Job URL: `https://www.upwork.com/jobs/~022088385600274146261`)
- **Required Connects:** 14 | **Competition:** 50+ proposals | **Status:** 1 hire recorded on posting / ongoing opportunity.

---

## 2. Client Profile & Track Record
- **Client Location:** Stirling, United Kingdom (BST / UTC+1 timezone).
- **Client Reputation:** 4.99 / 5.00 rating across **1,942 reviews**.
- **Platform Track Record:** High-velocity systemized employer with **2,083 jobs posted**, a near-perfect **99% hire rate**, and **2,071 completed hires**.
- **Client Mindset:** Pragmatic, systems-driven business owner who delegates defined, modular micro-tasks with clear operational goals. Values fast turnaround and zero maintenance friction.

---

## 3. Core Problem Statement & Workflow Requirements

### The Current Operational Bottleneck
- High influx of varied email attachments: vendor invoices, customer signed contracts, logistics receipts, and supplier reports.
- Manual saving and renaming results in lost files, misfiled folders, and generic filename clutter (e.g., `document final 2.pdf`, `Invoice_scan.pdf`).

### The Target Autonomous Behavior
1. **Zero-Touch Background Ingestion:** Operates automatically on an event trigger (new incoming email) or high-frequency polling cron.
2. **Context-Aware Classification (Claude API):** Inspects the email subject, sender address, body text, and the attachment's internal text/PDF OCR to identify:
   - Document Type (e.g., Invoice, Contract, Supplier Report, Receipt, Statement).
   - Entity / Counterparty (Vendor name, Customer name, Supplier).
   - Relevant Dates & Reference Numbers (Invoice #, Agreement Date).
3. **Deterministic File Renaming:** Formats filenames to a strict convention, such as:
   `YYYY-MM-DD_[EntityName]_[DocumentType]_[RefNumber].[ext]`
4. **Targeted Google Drive Folder Routing:** Automatically places the file into the corresponding Drive directory (e.g., `/Invoices/2026/`, `/Contracts/Signed/`, `/Suppliers/Reports/`).
5. **Smart Fallback Triage:** If Claude cannot classify a document with high certainty, it files the document in a designated `_Needs_Review_Inbox` folder and flags it for quick manual sorting.

---

## 4. End-to-End System Architecture Blueprint

```
+-----------------------------------------------------------------------------------+
|                     AUTONOMOUS EMAIL-TO-DRIVE CLAUDE PIPELINE                     |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Incoming Email with Attachment] (Gmail / IMAP / Outlook)                        |
|                     │                                                             |
|                     v                                                             |
|  [Ingestion Trigger] (Webhook / Cloud Run / n8n / Google Apps Script)             |
|                     │                                                             |
|                     ├──> Extract Email Metadata (Sender, Subject, Body)           |
|                     └──> Parse Attachment (PDF text / OCR / Image)                |
|                                     │                                             |
|                                     v                                             |
|                    [Claude Messages API Analysis]                                 |
|                    System Prompt: Classify doc, extract Entity, Date, Type        |
|                    Output: Structured JSON payload                                |
|                                     │                                             |
|                     +---------------+---------------+                             |
|                     │                               │                             |
|              (High Confidence)              (Low / Ambiguous)                     |
|                     │                               │                             |
|                     v                               v                             |
|         [Apply Standard Naming]          [Name: YYYY-MM-DD_Unclassified_[Original]|
|         YYYY-MM-DD_Vendor_Invoice_#123              │                             |
|                     │                               │                             |
|                     v                               v                             |
|         [Upload to Specific Drive]       [Upload to "_Needs_Review" Folder]       |
|         e.g., /Drive/Accounting/2026/               │                             |
|                     │                               │                             |
|                     v                               v                             |
|        [Mark Email Processed / Apply Label (e.g., "Filed-by-AI")]                 |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 5. Implementation Approaches

### Approach A: Cloud Serverless Python Script (Recommended for Robustness)
- **Tech Stack:** Python 3.11, Google Workspace APIs (Gmail API + Google Drive API), Anthropic Claude SDK (`claude-3-5-haiku` or `claude-3-7-sonnet` for fast, cost-effective document classification), hosted on Google Cloud Run or AWS Lambda with a 5-minute cron trigger.
- **Cost:** Virtually free serverless tier + fractions of a cent per document classification.

### Approach B: No-Code / Low-Code Automation (n8n / Make.com)
- **Tech Stack:** n8n / Make.com workflow connecting Gmail $\rightarrow$ Claude API node (structured JSON extraction) $\rightarrow$ Google Drive upload node $\rightarrow$ Gmail label update.
- **Pros:** Visual debugging interface, easily maintained by non-developers.

### Approach C: Native Google Apps Script (Zero External Hosting)
- **Tech Stack:** Google Apps Script triggered on time-driven intervals inside Google Workspace, calling Anthropic API via `UrlFetchApp` and manipulating Drive files natively without third-party server hosting.

---

## 6. Proposal Strategy & Submission Blueprint
1. **Emphasize True Autonomy & Safeguards:** Confirm that the agent will be 100% autonomous for all confident classifications, with a clean `_Needs_Review` fallback folder so zero documents are ever lost or misplaced.
2. **Present the 3 Deployment Options:** Briefly present the 3 deployment architectures (Google Apps Script for zero-cost hosting, Python serverless, or Make/n8n) and let the client choose their preferred maintenance style.
3. **Highlight Fast Turnaround:** Propose delivering the working script, Drive folder schema, and live test run within 24–48 hours.
