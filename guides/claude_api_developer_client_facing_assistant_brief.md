# Comprehensive Opportunity & Job Brief: Claude API Developer (Client-Facing AI Assistant)

## 1. Executive Summary & Opportunity Overview
- **Project Title:** Claude API Developer — Build a Client-Facing AI Assistant
- **Engagement Model:** Fixed-Price Initial Milestone ($100.00) with direct Contract-to-Hire potential.
- **Strategic Purpose:** The client is seeking a reliable, hands-on AI engineer to develop an extensible proof-of-concept (POC) client-facing chat assistant powered by Anthropic's Claude API. This engagement serves as a paid technical assessment and Phase 1 foundation for a broader product roadmap. High-quality execution is intended to transition directly into ongoing development work.
- **Listing Source:** Upwork (Job URL: `https://www.upwork.com/jobs/~022094781704250769177`)
- **Required Connects:** 16 | **Competition:** 20–50 proposals submitted | **Interviewing:** 0

---

## 2. Business Context & Strategic Objectives
- **Phase 1 Proof-of-Concept:** Deliver a lightweight, fully functional chat application demonstrating core LLM agent capabilities without bloated frameworks or unnecessary abstractions.
- **Maintainability & Handover:** The code must be cleanly architected so the client's internal team can easily inspect, configure, and extend it in subsequent phases.
- **Contract-to-Hire Pathway:** The client explicitly states this is the entry gate for a long-term engagement to build out their broader AI and client-facing product suite.

---

## 3. Scope of Work & Deliverables Breakdown

### A. Core LLM & Chat Interface
- **Claude Messages API Integration:** Seamless integration using Anthropic's latest SDK and Messages API endpoint.
- **Real-Time Token Streaming:** Server-Sent Events (SSE) or WebSocket streaming to deliver a low-latency, responsive conversational UX.
- **Multi-Turn Context Management:** Persistent conversation history maintained across user and assistant turns within the active session.
- **Configurable Prompt Engineering:** Isolated, well-structured system prompt stored in an external configuration file (JSON/YAML/ENV) allowing non-developers to modify behavior and tone without altering application logic.

### B. Tool Calling & External Integration
- **Function / Tool Calling:** Implementation of at least one operational Claude tool definition mapped to an external data source (e.g., public REST API or structured local JSON database).
- **Tool Execution Loop:** Proper handling of model-generated tool arguments, execution of the tool, returning tool results to Claude, and synthesizing the final natural language answer for the user.

### C. Reliability & Error Handling
- **API Rate Limiting & Backoff:** Graceful handling of Anthropic API rate limits (HTTP 429) and network timeouts.
- **Tool Failures:** Resilient fallback mechanisms if the external API or JSON fetch fails or returns unexpected data.
- **User-Facing Error Messaging:** Non-technical, clean feedback shown in the UI when upstream issues arise.

### D. Deployment, Repository & Documentation
- **Clean Repository:** Private GitHub repository adhering to clean code standards and minimal dependency footprint.
- **Developer Documentation (`README.md`):**
  - Step-by-step local setup instructions.
  - Environment variable specifications (e.g., `ANTHROPIC_API_KEY`, API base URLs).
  - Guide on swapping keys and adjusting configuration files.
- **Live Cloud Deployment:** Accessible, publicly hosted prototype on modern hosting platforms (Vercel, Render, Railway, or AWS/Fly.io).

---

## 4. Technical Architecture & Stack Flexibility
- **Client Preference:** "Keep it simple and readable; no heavy framework layers we'd have to unpick later."
- **Recommended Options:**
  - **Full-Stack TypeScript / JavaScript:** Next.js (App Router), React, TailwindCSS, Vercel AI SDK / Anthropic SDK.
  - **Python / Modern Web Frontend:** FastAPI / Flask backend with a lightweight React or vanilla JS frontend.
- **Key Architecture Expectation:** Separation of concerns between UI presentation, backend API orchestration/security (never exposing the Anthropic API key to the browser), and tool definitions.

---

## 5. Client Profile, Track Record & Collaboration Style
- **Location & Timezone:** Coimbatore, India (IST — Indian Standard Time). Responsive during IST business hours.
- **Client Reputation:** 5.00 / 5.00 rating across previous contracts, payment and phone verified.
- **Hiring History & Nature of Work:**
  - 14 total jobs posted with a 15% hire rate.
  - Past projects highlight complex, innovative technical tasks:
    1. *Multi-Agent System* integrating customer and product signals across Gong, GitHub, Zendesk, Slack, and G2 (awarded 5.0 rating).
    2. *Full Stack Interactive Floor Plan MVP* in React/Next.js (awarded 5.0 rating).
  - Feedback indicates the client provides well-scoped briefs, clear communication, fast review turnaround, and positive collaborative relationships.

---

## 6. Candidate Fit & Selection Criteria
- **Target Profile:** Intermediate-to-senior software engineer with real-world production experience deploying Claude or OpenAI API applications.
- **Core Competencies:** Deep familiarity with token economics, context window management, streaming protocols, function calling schemas, and maintainable software engineering.
- **Communication:** Proactive communicator who flags roadblocks early and writes code designed for team collaboration.

---

## 7. Proposal Strategy & Required Submission Format
The client explicitly filters out generic boilerplate and agency spam. To be considered, proposals must directly answer:
1. **Proven Track Record:** Direct link to a shipped product, live demo, or public GitHub repository demonstrating hands-on work with Claude or OpenAI APIs.
2. **Stack Justification:** 1–2 sentences explaining the chosen technology stack (e.g., Next.js vs FastAPI) and why it fits this rapid, clean prototype build.
3. **Realistic Timeline:** Clear, upfront estimate of turnaround time to deliver the working demo and repo.
