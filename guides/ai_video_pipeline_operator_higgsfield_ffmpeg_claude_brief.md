# Comprehensive Opportunity & Job Brief: AI Video Pipeline Operator (Higgsfield + FFmpeg + Claude)

## 1. Executive Summary & Opportunity Overview
- **Project Title:** AI Video Pipeline Operator (Higgsfield + FFmpeg + Claude)
- **Engagement Model:** Hourly ($8.00 – $30.00/hr, starting with a paid trial leading into long-term high-volume production > 6 months).
- **Core Role:** High-velocity AI Video Pipeline Operator. The client produces hundreds of 20–30 second cinematic shorts in a locked aesthetic. The role is focused on rapid generation, prompt-debugging via Claude/ChatGPT, lightweight FFmpeg automation (concatenation, cropping, subtitles), rigorous QC, and queue throughput.
- **Listing Source:** Upwork (Job URL: `https://www.upwork.com/jobs/~022094833903259408397`)
- **Required Connects:** 26 | **Competition:** 15–20 proposals | **Activity:** 0 interviewing.

---

## 2. Client Profile, Track Record & Production Scale
- **Client Identity & Location:** Nick & Adam (Ontro / Media Brand), United States (Johnston, US timezone).
- **Track Record:** 106 jobs posted, 45% hire rate, **$87,000+ total spent**, 50 hires with 10 currently active, 9,600+ billed hours ($7.40/hr average rate across team).
- **Client Operating Style:** High-volume, systems-driven studio. They supply the scripts, character reference packs, brand guidelines, and active Higgsfield accounts. They expect high operational velocity: *"Generate, check, ship. Do not rebuild commercials by hand unless the one-shot failed."*

---

## 3. Operational Philosophy & Workflow Blueprint

```
+-----------------------------------------------------------------------------------+
|                         AI VIDEO OPERATOR QUEUE PIPELINE                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Input: Script & Character Pack]                                                 |
|               │                                                                   |
|               v                                                                   |
|  [Step 1: One-Shot Generation] ──> Higgsfield (Seedance) / Kling / FAL API        |
|               │                                                                   |
|               ├── (Pass) ──────────┐                                              |
|               │                    │                                              |
|               └── (Miss / Flaw)    │                                              |
|                       │            │                                              |
|                       v            │                                              |
|          [Step 2: Prompt Copilot]  │                                              |
|          Claude / ChatGPT Prompt   │                                              |
|          Refactor (No Re-rolls)    │                                              |
|                       │            │                                              |
|                       v            │                                              |
|          [Step 3: FFmpeg Glue] <───┘                                              |
|          - Concat scenes, Crop 9:16, Burn Captions, Audio Normalization           |
|                       │                                                           |
|                       v                                                           |
|          [Step 4: Strict QC Pass]                                                 |
|          - Identity drift check                                                   |
|          - On-screen artifact / typo inspection                                   |
|          - Audio sync & level check                                               |
|                       │                                                           |
|                       ├── (Clean) ───> [SHIP TO QUEUE & NEXT CLIP]                |
|                       │                                                           |
|                       └── (Edge Failure) ──> Fast Traditional Cut & Ship          |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 4. Technical Toolchain & Operator Responsibilities

### A. AI Video Generation & Identity Preservation
- **Primary Generator:** Higgsfield / Seedance using custom character packs (preserving realistic business owner identities across varying cinematic indoor/outdoor environments without green-screen UGC look).
- **Alternative/Supplementary Generators:** Kling, FAL.ai, Runway Gen-3 Alpha, Luma Dream Machine.

### B. Prompt Engineering & Copilot Loop (Claude / ChatGPT)
- **Zero Brute-Force Re-rolls:** Rather than wasting generation credits and time on repeated random seeds, use Claude to analyze generation failures (camera angle errors, lighting inconsistencies, anatomical distortions) and surgically rewrite prompt descriptors, camera motion tokens, and negative prompts.

### C. CLI Post-Processing & Scripting Glue (FFmpeg + Python)
- **Fast CLI Automation:** Rapid execution of FFmpeg commands for:
  - Vertical 9:16 smart cropping and padding.
  - Subtitle burning and kinetic caption alignment.
  - Stream concat without re-encoding when codecs match.
  - Audio normalization and fade-in/fade-out transitions.
- **Python Pipeline Glue (Bonus):** Automated scripts to pull generations from APIs, run batch FFmpeg transforms, and stage files for QC inspection.

### D. Quality Control (QC) & Edge Case Fallback
- **Inspection Checklist:**
  - [ ] Facial & character identity consistency across all scene cuts.
  - [ ] Text accuracy & zero hallucinated glyphs/typos.
  - [ ] Audio-visual synchronization and seamless sound transitions.
  - [ ] Absence of unnatural AI warp/melt artifacts.
- **Fallback Protocol:** If an AI generation fails after one prompt adjustment, perform a fast 2-minute traditional edit (trim/overlay/mask) to ship immediately and keep the queue moving.

---

## 5. Mandatory Application Questions & Proposal Checklist

The client has set strict proposal filters. Proposals must adhere exactly to the required format:

### 1. Keyword Verification
- **Must start proposal with:** `PIPELINE`

### 2. Connected Generators & Claude Copilot Loop
- List specific platforms used (e.g., Higgsfield, Seedance, Kling, FAL.ai, Runway).
- Detail how Claude/ChatGPT is used as a real-time prompt debugger to adjust lighting, motion parameters, lens tags, and character anchors.

### 3. Production FFmpeg Command
Include a tested, real-world command demonstrating multi-pass post-processing (e.g., cropping to 9:16 and burning subtitles with audio normalization):
```bash
ffmpeg -i input_scene.mp4 -vf "crop=ih*(9/16):ih,subtitles=captions.srt:force_style='FontSize=18,Bold=1,PrimaryColour=&H00FFFFFF,Outline=2'" -c:a aac -b:a 192k -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:v libx264 -crf 18 -preset fast output_vertical_short.mp4
```

### 4. Portfolio Links
- Provide direct URLs to 2–3 short-form AI-generated videos demonstrating cinematic realism and character consistency.

### 5. Availability & Timezone
- State weekly available hours (e.g., 20–30 hrs/week) and local timezone.
