# Comprehensive Opportunity & Job Brief: System Claude Code + CapCut (YouTube Shorts Automation)

## 1. Executive Summary & Opportunity Overview
- **Project Title:** System Claude code CapCut — Automated Football YouTube Shorts Creation Pipeline
- **Engagement Model:** Hourly (< 30 hrs/week, estimated duration < 1 month).
- **Core Objective:** The client operates a football (soccer) YouTube channel and wants to establish an automated, semi-automated, or streamlined production pipeline to produce high-retention, storytelling-style YouTube Shorts (similar to viral football narrative Shorts).
- **Listing Source:** Upwork (Job URL: `https://www.upwork.com/jobs/~022094727136503571011`)
- **Required Connects:** 11 | **Competition:** 5–10 proposals submitted | **Interviewing:** 0

---

## 2. Reference Style & Benchmark Content
- **Reference Examples:**
  - `https://youtube.com/shorts/kqojH1cI5iI`
  - `https://www.youtube.com/shorts/EBPTzvI6Rqc`
- **Characteristics of Target Style:**
  - High-tempo narrative/storytelling pacing with strong hook in first 2 seconds.
  - Deep, professional cinematic voiceover with dramatic delivery.
  - Fast-paced visual transitions, zoom-ins, overlays, motion graphics, and animated emojis.
  - Contextual B-roll clips (football match highlights, player reactions, archival footage).
  - Kinetic, word-by-word styled subtitles/captions with color highlights.

---

## 3. Client Pain Points & Questions to Solve

### 1. Voice Generation & Audio Engineering
- **Question:** How to achieve professional studio-quality voiceover? (AI vs. Human Mic).
- **Solution Blueprint:** Deep-dive into AI voice synthesis (e.g., ElevenLabs with custom voice cloning, dynamic pacing, stability/clarity tuning) vs. recorded voiceover with processing chains (EQ, compression, noise removal).

### 2. Dynamic Video Editing & Visual Effects
- **Question:** How are dynamic edits, animated emojis, sound design, and kinetic captions created? Can CapCut do this?
- **Solution Blueprint:** CapCut templates, keyframing, auto-captions with custom animation styles, visual asset packs, SFX layers (whooshes, risers, hits), and motion graphics presets.

### 3. Clip Sourcing, Cataloging & Asset Management
- **Question:** How do creators gather, organize, and retrieve relevant football clips? Is Claude used to match scripts to footage?
- **Solution Blueprint:**
  - Building a structured B-roll library tagged by player, emotion, action, and match context.
  - Using Claude to generate structured script tables with explicit B-roll cues and timestamp/search query mapping.
  - Automated clipping and metadata tagging workflows.

### 4. Automation & Tooling (Claude Code + CapCut)
- **Primary Goal:** Automate as much of the video creation and editing pipeline as possible using Claude / Claude Code and CapCut integration, replacing repetitive manual timeline editing.
- **Solution Architecture:**
  - **Script & Prompt Engine:** Claude Code / API generating retention-optimized storytelling scripts, scene breakdown JSON, and ElevenLabs voice prompts.
  - **Automated Voiceover Generation:** API script calling ElevenLabs / TTS to output audio with word-level timestamps.
  - **Video Assembly Automation Options:**
    - *Option A: Programmatic Video Generation* using Python (`moviepy`, `ffmpeg`, `Remotion`, or CapCut template automation / draft generator scripts).
    - *Option B: Semi-Automated CapCut Workflow* where Claude generates the draft project file / structured asset pack, and final touches (or templates) are applied in CapCut Desktop.
    - *Option C: Workflow Automation (n8n / Python)* stitching script generation -> voiceover -> B-roll selection -> draft video rendering.

---

## 4. Client Profile & Job Context
- **Location:** France (Neulise — CET timezone, UTC+1 / UTC+2).
- **Client Type:** Individual creator / entrepreneur in Sports & Recreation.
- **Account History:** Newly registered account (Sep 1, 2026), payment and phone verified.
- **Hiring Pattern:** 4 total jobs posted concurrently (all 4 currently open, 0% hire rate yet), including:
  1. *System Claude code CapCut* (Hourly)
  2. *CapCut Claude* (Hourly)
  3. *Help YouTube channel* (Hourly)
  4. *Build System with Claude Code* (Fixed-price)
  - *Note:* The client is actively looking for the right consultant/builder across multiple postings for the same overarching vision.

---

## 5. Recommended Implementation Roadmap for Client

```
+-----------------------------------------------------------------------------------+
|                           END-TO-END AUTOMATION PIPELINE                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Step 1: Ideation & Scripting]                                                   |
|  Topic / Match Event ---> Claude Prompt / Claude Code                             |
|                           |---> 50-second Retention Script (Hook, Story, Climax)  |
|                           |---> Structured Scene Breakdown & B-Roll Search Tags   |
|                                                                                   |
|  [Step 2: Voiceover & Timing]                                                     |
|  Script Text -------------> ElevenLabs API (Deep Cinematic Voice)                 |
|                             |---> Master Audio Track (.mp3/.wav)                  |
|                             |---> Word-level Timestamps (for sync captions)       |
|                                                                                   |
|  [Step 3: Footage & Asset Alignment]                                              |
|  Scene Tags --------------> Clip Library / Sourcing Automation                     |
|                             |---> Automated slice & resize to 9:16 vertical       |
|                                                                                   |
|  [Step 4: Automated Assembly & FX]                                                |
|  Audio + Clips + Captions -> Python / FFmpeg / CapCut Draft API Generator         |
|                              |---> Dynamic kinetic subtitles (word-by-word)       |
|                              |---> Motion zooms, sound effects, animated emojis   |
|                                                                                   |
|  [Step 5: Output & Quality Polish]                                                |
|  Automated Draft ---------> CapCut Project File or Rendered Short (.mp4)          |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 6. Proposal Strategy & Pitch Recommendations
- **Positioning:** Position as an AI Automation Engineer & YouTube Workflow Architect who understands both the technical tooling (Claude Code, Python, APIs, FFmpeg/n8n) and YouTube Shorts retention mechanics (hooks, pacing, sound design).
- **Core Value Proposition to Pitch:**
  1. **Answer the 3 questions directly:** Explain clearly how top creators produce voice (ElevenLabs Adam/Antoni voice models + master compression), edit in CapCut (keyframe presets + dynamic captions), and organize footage.
  2. **Demonstrate Automation Feasibility:** Explain how Claude Code can generate structured timeline data (JSON/CapCut draft files or Python FFmpeg pipeline) to eliminate 80%+ of manual video editing time.
  3. **Offer a Consulting + Build Hybrid:** Propose a 2-part milestone plan:
     - *Phase 1 (Setup & Architecture):* Establish the script-to-voice and clip sourcing template workflow, setting up ElevenLabs + CapCut presets/scripts.
     - *Phase 2 (Automation Build):* Build the Claude Code / Python automation pipeline to generate complete or near-complete Shorts drafts automatically.
