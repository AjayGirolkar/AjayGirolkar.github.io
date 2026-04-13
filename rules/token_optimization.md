# 🚀 AI Agent Token Optimization Guide
## High Efficiency + High Quality Output Framework

This document defines how the AI agent should behave to:
- Minimize token consumption
- Maximize output quality
- Avoid unnecessary regeneration
- Work in structured, modular steps

---

# 🎯 CORE PRINCIPLES

## 1. Work Step-by-Step (MANDATORY)
- Never generate full solution in one go
- Always break tasks into smaller steps
- Wait for confirmation before moving to next step

---

## 2. Avoid Repetition
- Do NOT repeat previous outputs
- Do NOT restate context unless necessary
- Reference previous work instead of rewriting

---

## 3. Generate Only What is Asked
- Do not add extra features
- Do not assume additional requirements
- Keep scope strictly limited to the current step

---

## 4. Optimize for Token Efficiency
- Keep explanations minimal
- Focus on actionable output
- Avoid long descriptions unless explicitly requested

---

## 5. Prefer Incremental Updates
Instead of:
❌ Regenerating full code

Use:
✅ Modify only the requested section

---

# 🧠 EXECUTION STRATEGY

## Phase 1: Discovery (Low Token Mode)
Goal: Define direction without heavy generation

Agent Instructions:
- Provide options instead of full solutions
- Keep responses concise
- No code generation

Example Tasks:
- Define portfolio styles
- Suggest structure
- Compare approaches

---

## Phase 2: Planning (Blueprint Mode)
Goal: Lock structure before building

Agent Instructions:
- Generate only:
  - Sitemap
  - Section list
  - Content outline
- No UI code yet

Output Example:
- Hero Section
- About
- Services
- Portfolio
- Contact

---

## Phase 3: Design System (Lightweight)
Goal: Define visual consistency

Agent Instructions:
- Define:
  - Colors
  - Typography
  - Spacing
  - UI style
- No full UI implementation

---

## Phase 4: Content Generation (Chunked)
Goal: Create content in small parts

Agent Instructions:
- Generate one section at a time
- Do not generate full page content

Example:
- First: Hero section text
- Then: About section
- Then: Services

---

## Phase 5: Code Generation (Modular)
Goal: Build UI in independent components

Agent Instructions:
- Generate ONE section per request
- Use reusable components
- Do not combine everything at once

Example:
- Create Hero component
- Create Services component
- Create Portfolio component

---

## Phase 6: Assembly
Goal: Combine all components

Agent Instructions:
- Integrate previously created modules
- Avoid rewriting components
- Focus only on layout composition

---

# ⚡ TOKEN SAVING RULES

## Rule 1: No Full Regeneration
- Never rewrite entire project for small changes

---

## Rule 2: Use Targeted Updates
Always prefer:
"Modify only this section: [code snippet]"

---

## Rule 3: Avoid Verbose Explanations
- Keep explanations under 3–5 lines unless asked

---

## Rule 4: Context Reset Strategy
If conversation becomes long:
- Start new session
- Provide final summary as fresh input

---

## Rule 5: Output Control
Always follow:
- Concise
- Structured
- No unnecessary comments in code

---

# 🧩 CODE GENERATION RULES

## General
- Clean, production-ready code
- Minimal comments
- No duplicate logic

---

## UI Development
- Use reusable components
- Follow consistent design system
- Avoid over-engineering

---

## Performance
- Optimize for readability + performance
- Avoid unnecessary dependencies

---

# 🧪 QUALITY CONTROL

Before generating output, ensure:

- Is this step necessary?
- Is this repeating previous work?
- Can this be smaller?
- Is this aligned with the current phase?

---

# 🎯 RESPONSE FORMAT

Every response must follow:

1. ✅ What is being delivered (1 line)
2. 🔧 Output (main content)
3. ⏭️ Next step suggestion (optional, 1 line)

---

# 🚫 STRICT DON'TS

- Do NOT generate full website in one go
- Do NOT rewrite existing sections unnecessarily
- Do NOT add features not requested
- Do NOT produce overly long responses

---

# 🏁 FINAL GOAL

- Efficient token usage
- High-quality output
- Clear, modular development
- Zero wasted generation

---

# 🔥 MASTER CONTROL PROMPT

Use this at the start of every session:

"Follow AI Agent Token Optimization Guide strictly.
Work step-by-step.
Do not repeat previous outputs.
Keep responses concise.
Generate only what is requested."