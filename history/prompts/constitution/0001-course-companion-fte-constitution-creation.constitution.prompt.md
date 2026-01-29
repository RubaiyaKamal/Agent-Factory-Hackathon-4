---
id: 0001
title: Course Companion FTE Constitution Creation
stage: constitution
date: 2026-01-21
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Lap Zone
command: sp.constitution
labels: ["constitution", "architecture", "phase-based-development", "zero-backend-llm", "agent-factory"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (documentation artifact)
---

## Prompt

create a /sp.constitution file according to this docs . Work phase wise 1,2 and then 3 .   Course Companion FTE
Agent Factory Hackathon IV Document
Building a Digital Full-Time Equivalent Educational Tutor
A Dual-Frontend Architecture with Zero-Backend-LLM Default
→ Selective Hybrid Intelligence

Version 1.0 — January 2026
Prepared for Panaversity Agent Factory Development Hackathon

[Full hackathon documentation provided including:]

1. Executive Summary
   - Build a Course Companion FTE serving as 24/7 educational tutor
   - Digital FTE working 168 hours/week at 85-90% cost savings
   - General Agents manufacture Custom Agent using Spec-Driven Development
   - Dual Frontends (ChatGPT App + Web App)
   - Zero-Backend-LLM Default with Selective Hybrid Intelligence

2. Digital FTE Thesis
   - Human tutor vs Digital FTE comparison
   - Cost: $2,000-$5,000/month vs $200-$500/month
   - Scale: 20-50 students vs unlimited concurrent
   - Consistency: 85-95% vs 99%+
   - 99% cost reduction while maintaining quality

3. Project Overview
   - AI-Native Course Companion: teach, explain, quiz, track, adapt
   - Dual Frontend: ChatGPT App (Phase 1&2) + Web App (Phase 3)
   - Deterministic Backend (Phase 1), Hybrid Backend (Phase 2), Consolidated Backend (Phase 3)
   - Content Storage: Cloudflare R2

4. Architecture Overview
   - Agent Factory 8-layer architecture (L0-L7)
   - Phase 1: L3 (FastAPI) + L6 (Skills + MCP) - Deterministic
   - Phase 2: Add L4 + L5 (Hybrid SDK) for premium
   - Zero-Backend-LLM principle: ChatGPT does ALL intelligent work in Phase 1

5. Phase 1 Requirements
   - Zero backend LLM calls (STRICT)
   - 6 required features: Content Delivery, Navigation, Grounded Q&A, Rule-Based Quizzes, Progress Tracking, Freemium Gate
   - Disqualification if backend contains ANY LLM calls

6. Phase 2 Requirements
   - Maximum 2 hybrid features
   - Must be: feature-scoped, user-initiated, premium-gated, isolated, cost-tracked
   - Allowed: Adaptive Learning Path, LLM-Graded Assessments, Cross-Chapter Synthesis, AI Mentor Agent

7. Phase 3 Requirements
   - Full Next.js/React web application
   - Consolidated backend with all features
   - LMS dashboard, analytics, admin features

8. Agent Skills Design
   - concept-explainer, quiz-master, socratic-tutor, progress-motivator

9. Cost Analysis Framework
   - Phase 1: $0.002-$0.004 per user
   - Phase 2 hybrid costs: $0.014-$0.090 per request
   - Monetization: Free, Premium ($9.99), Pro ($19.99), Team ($49.99)

10. Golden Rules
    - Zero-Backend-LLM is default
    - Hybrid intelligence must be selective, justified, and premium
    - Spec is source code

## Response snapshot

Constitution v1.0.0 created with the following structure:

**Core Principles (7):**
1. Zero-Backend-LLM Architecture (Default) - Mandatory for Phase 1, strict disqualification rules
2. Phase-Based Development Progression - Phase 1 (Zero-LLM), Phase 2 (Hybrid), Phase 3 (Web App)
3. Agent Factory 8-Layer Architecture - Layer assignment by phase
4. Spec-Driven Development (SDD) - Mandatory artifacts (spec, plan, tasks), PHR routing, ADR suggestions
5. Cost Efficiency & Scalability - Budget targets, monetization tiers
6. Educational Quality Standards - 99%+ consistency, 24/7 availability, 6 required features, 4 agent skills
7. Security & Compliance - Authentication, user isolation, source-grounded responses, auditability

**Technical Stack Requirements:**
- Frontend: OpenAI Apps SDK (Phase 1&2), Next.js/React (Phase 3)
- Backend: FastAPI (Python 3.11+), Pydantic, SQLAlchemy/Prisma
- Storage: Cloudflare R2, Neon/Supabase
- Hybrid: Claude Sonnet (Phase 2 only)
- Infrastructure: gVisor, Kafka, Dapr, Agent SDKs (Phase 2&3)

**Development Workflow & Quality Gates:**
- Execution contract: 6-step process for every request
- Minimum acceptance criteria
- Human as Tool Strategy

**Governance:**
- Amendment process with semantic versioning
- Compliance review requirements
- 5 Golden Rules (non-negotiable)

**Sync Impact Report included:**
- Version: Initial → 1.0.0 (MAJOR)
- All 7 principles documented
- Templates validated for alignment
- No placeholders remaining

## Outcome

- ✅ Impact: Comprehensive constitution created defining architectural principles, phase-based progression, and quality standards for Course Companion FTE project
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: Created .specify/memory/constitution.md (331 lines)
- 🔁 Next prompts: Begin Phase 1 spec creation for first feature (Content Delivery API or ChatGPT App Frontend)
- 🧠 Reflection: Constitution successfully captures all hackathon requirements with clear enforcement rules, especially Zero-Backend-LLM mandate for Phase 1 and phased progression strategy

## Evaluation notes (flywheel)

- Failure modes observed: None. Constitution created successfully with all placeholders filled and requirements captured.
- Graders run and results (PASS/FAIL): Manual validation PASS - all 7 principles defined, no placeholder tokens remaining, semantic versioning applied, Sync Impact Report included
- Prompt variant (if applicable): N/A (initial creation)
- Next experiment (smallest change to try): Validate constitution against first feature spec to ensure architectural constraints are enforceable in practice
