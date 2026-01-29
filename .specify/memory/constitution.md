<!--
Sync Impact Report - Constitution v1.0.0 Creation
=================================================
Version Change: Initial → 1.0.0 (MAJOR - new constitution)
Rationale: Initial constitution defining Course Companion FTE architectural principles

Modified Principles:
- [NEW] I. Zero-Backend-LLM Architecture (Default)
- [NEW] II. Phase-Based Development Progression
- [NEW] III. Agent Factory 8-Layer Architecture
- [NEW] IV. Spec-Driven Development (SDD)
- [NEW] V. Cost Efficiency & Scalability
- [NEW] VI. Educational Quality Standards
- [NEW] VII. Security & Compliance

Added Sections:
- Core Principles (7 principles)
- Technical Stack Requirements
- Development Workflow & Quality Gates
- Governance

Removed Sections: None (initial version)

Templates Requiring Updates:
✅ spec-template.md - Validated alignment with architectural constraints
✅ plan-template.md - Validated alignment with phase-based progression
✅ tasks-template.md - Validated alignment with required features
⚠ phr-template.prompt.md - Review for constitution stage routing

Follow-up TODOs: None

Files Modified:
- .specify/memory/constitution.md (created)
-->

# Course Companion FTE Constitution

## Core Principles

### I. Zero-Backend-LLM Architecture (Default)

**MANDATORY for Phase 1. Hybrid intelligence must be exceptional, justified, and premium.**

Backend MUST NOT contain:
- LLM API calls (ChatGPT, Claude, or any inference service)
- RAG summarization or semantic reasoning
- Prompt orchestration or agent loops
- Dynamic content generation via AI models

Backend MUST provide:
- Deterministic content APIs serving verbatim material from storage
- Rule-based navigation (next/previous chapter sequencing)
- Keyword and semantic search (embedding-based, but no LLM generation)
- Progress tracking and streak calculation
- Access control and freemium gating
- Rule-based quiz grading with predefined answer keys

**Rationale**: Zero-Backend-LLM ensures:
- Predictable costs ($0.002-$0.004 per user)
- Linear scalability (10 to 100,000+ users)
- High correctness (source-grounded, no hallucination)
- Simple operations (no model versioning, token optimization, or prompt management)
- Clear compliance audit trail

**Disqualification Rule**: Any backend LLM inference in Phase 1 results in immediate project disqualification.

### II. Phase-Based Development Progression

**Development MUST follow strict phase boundaries with independent validation.**

**Phase 1 - Zero-Backend-LLM (ChatGPT App)**
- ChatGPT App frontend using OpenAI Apps SDK
- Deterministic FastAPI backend
- All 6 required features (content, navigation, Q&A, quizzes, progress, freemium)
- Cost target: <$50/month for 10,000 users
- Validation: Code audit confirms zero backend LLM calls

**Phase 2 - Hybrid Intelligence (Selective Premium)**
- Add maximum 2 hybrid features
- Each feature MUST be: feature-scoped, user-initiated, premium-gated, isolated, cost-tracked
- Allowed features: Adaptive Learning Path, LLM-Graded Assessments, Cross-Chapter Synthesis, AI Mentor Agent
- Cost tracking: Per-user LLM costs monitored and documented
- Validation: Architecture review confirms isolation, premium gating functional

**Phase 3 - Full Web App**
- Standalone Next.js/React web application
- Consolidated backend serving all features
- LMS dashboard with progress visualization
- Admin features and analytics
- Validation: Full feature parity, responsive design, production-ready

**Rationale**: Phased progression prevents over-engineering, validates cost model early, and ensures each phase delivers production value independently.

### III. Agent Factory 8-Layer Architecture

**System MUST align with Agent Factory reference architecture.**

**Layer Assignment by Phase:**

| Layer | Technology | Phase 1 | Phase 2 | Phase 3 |
|-------|-----------|---------|---------|---------|
| L0: Sandbox | gVisor | - | Required | Required |
| L1: Events | Apache Kafka | - | Required | Required |
| L2: Infra | Dapr + Workflows | - | Required | Required |
| L3: HTTP | FastAPI | Required | Required | Required |
| L4: High-Level | OpenAI Agents SDK | - | Required | Required |
| L5: Agentic | Claude Agent SDK | - | Required | Required |
| L6: Skills | Runtime Skills + MCP | Required | Required | Required |
| L7: A2A | Agent-to-Agent Protocol | - | Required | Required |

**Phase 1 Focus**: L3 (FastAPI HTTP interface) + L6 (Agent Skills + MCP tools)

**Rationale**: Layered architecture enables:
- Clear separation of concerns
- Independent layer testing
- Incremental complexity addition
- Standard integration patterns

### IV. Spec-Driven Development (SDD)

**All work MUST originate from specs, plans, and tasks.**

**Mandatory Artifacts:**
- `specs/<feature>/spec.md` - Feature requirements and acceptance criteria
- `specs/<feature>/plan.md` - Architectural decisions and design
- `specs/<feature>/tasks.md` - Testable implementation tasks

**Mandatory Documentation:**
- Prompt History Records (PHRs) for every user interaction (except `/sp.phr` itself)
- Architectural Decision Records (ADRs) for significant decisions (suggested, user-approved)

**PHR Routing (automatic under `history/prompts/`):**
- Constitution stage → `history/prompts/constitution/`
- Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/`
- General stage → `history/prompts/general/`

**ADR Significance Test** (all three MUST be true):
- Impact: Long-term consequences (framework, data model, API, security, platform)
- Alternatives: Multiple viable options considered
- Scope: Cross-cutting, influences system design

When significant, suggest: "📋 Architectural decision detected: [brief] — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"

**Rationale**: Spec is source code. If excellence can be described, AI can build it. PHRs enable learning and traceability. ADRs preserve reasoning.

### V. Cost Efficiency & Scalability

**System MUST demonstrate predictable, sub-linear cost scaling.**

**Phase 1 Cost Budget (10,000 users/month):**
- Cloudflare R2: $5
- Database (Neon/Supabase): $0-25
- Compute (Fly.io/Railway): $10
- Domain + SSL: $1
- **Total**: $16-41 ($0.002-$0.004 per user)
- **ChatGPT Usage**: $0 to developer (users access via subscription)

**Phase 2 Hybrid Feature Costs:**
- Adaptive Learning Path: ~$0.018 per request (Claude Sonnet, ~2K tokens)
- LLM-Graded Assessment: ~$0.014 per request (~1.5K tokens)
- Cross-Chapter Synthesis: ~$0.027 per request (~3K tokens)
- AI Mentor Session: ~$0.090 per session (~10K tokens)

**Monetization Tiers:**
- Free: $0 (First 3 chapters, basic quizzes, ChatGPT tutoring)
- Premium: $9.99/mo (All chapters, quizzes, progress tracking)
- Pro: $19.99/mo (Premium + Adaptive Path + LLM Assessments)
- Team: $49.99/mo (Pro + Analytics + Multiple seats)

**Rationale**: Cost predictability enables confident pricing. Sub-linear scaling ensures profitability at scale. Hybrid features are justified by premium revenue.

### VI. Educational Quality Standards

**System MUST deliver consistent, high-quality educational experiences.**

**Required Quality Metrics:**
- Consistency: 99%+ in educational delivery
- Availability: 24/7 (168 hours/week)
- Scalability: 10 to 100,000 users without linear cost increase
- Correctness: Predictable, auditable, source-grounded responses
- Personalization: ChatGPT adapts tone, complexity, analogies without backend AI

**Required Features (All Phases):**
1. **Content Delivery** - Backend serves verbatim; ChatGPT explains at learner's level
2. **Navigation** - Backend sequences chapters; ChatGPT suggests optimal path
3. **Grounded Q&A** - Backend returns sections; ChatGPT answers using content only
4. **Rule-Based Quizzes** - Backend grades with answer key; ChatGPT presents and encourages
5. **Progress Tracking** - Backend stores completion/streaks; ChatGPT motivates
6. **Freemium Gate** - Backend checks access; ChatGPT explains premium gracefully

**Required Agent Skills (Runtime):**
- `concept-explainer`: Explain concepts at various complexity levels (triggers: "explain", "what is", "how does")
- `quiz-master`: Guide students through quizzes with encouragement (triggers: "quiz", "test me", "practice")
- `socratic-tutor`: Guide learning through questions, not answers (triggers: "help me think", "I'm stuck")
- `progress-motivator`: Celebrate achievements, maintain motivation (triggers: "my progress", "streak", "how am I doing")

**Rationale**: Clear quality standards ensure the Digital FTE delivers value comparable to human tutors while maintaining AI advantages (availability, scale, cost).

### VII. Security & Compliance

**System MUST protect user data and maintain audit compliance.**

**Security Requirements:**
- Never hardcode secrets or tokens; use `.env` files with gitignore
- All API endpoints require authentication (JWT or session-based)
- User data isolation: users can only access their own progress, quizzes, content access
- Freemium access control: enforce tier limits at backend (not frontend-only)
- HTTPS required for all endpoints (Cloudflare R2 signed URLs)

**Compliance Requirements:**
- Source-grounded responses: ChatGPT answers only from provided content (reduces hallucination risk to LOW)
- Auditable deterministic logic: All backend decisions (quiz grading, progress, access) are rule-based and logged
- Cost tracking: Per-user hybrid feature usage logged for billing and analysis
- Clear separation: Deterministic vs hybrid logic isolated in separate API routes

**Rationale**: Education involves sensitive data (student progress, performance). Deterministic backend enables compliance. Source-grounded responses reduce liability.

## Technical Stack Requirements

**Mandatory Technologies:**

**Frontend (Phase 1 & 2):**
- ChatGPT App: OpenAI Apps SDK
- Conversational interface for 800M+ ChatGPT users
- App manifest (YAML) defining agent capabilities

**Frontend (Phase 3):**
- Web App: Next.js 14+ with React 18+
- TypeScript required
- Responsive design (mobile, tablet, desktop)
- Progress visualization components

**Backend (All Phases):**
- FastAPI (Python 3.11+)
- Pydantic for request/response validation
- SQLAlchemy or Prisma for database ORM
- Python type hints required

**Storage (All Phases):**
- Cloudflare R2 for content storage (courses, media, quiz banks)
- Neon or Supabase for relational data (users, progress, access)

**Hybrid Intelligence (Phase 2 Only):**
- Claude Sonnet (Anthropic API) for premium features
- Token usage tracking per request
- Rate limiting per user tier

**Infrastructure (Phase 2 & 3):**
- L0: gVisor for agent sandboxing
- L1: Apache Kafka for event backbone
- L2: Dapr for workflows and infrastructure abstraction
- L4: OpenAI Agents SDK for high-level orchestration
- L5: Claude Agent SDK for agentic execution
- L7: A2A Protocol for multi-agent collaboration

## Development Workflow & Quality Gates

**Execution Contract for Every Request:**

1. **Confirm Surface and Success Criteria** (one sentence)
   - Example: "Build content delivery API that serves course chapters verbatim from R2"

2. **List Constraints, Invariants, Non-Goals**
   - Constraints: Must use Cloudflare R2 signed URLs, max 5MB per chapter
   - Invariants: Content never modified by backend
   - Non-Goals: Content generation, summarization

3. **Produce Artifact with Acceptance Checks**
   - Code with inline tests or checkboxes
   - Example: `✅ Returns 404 for non-existent chapters`

4. **Add Follow-Ups and Risks (Max 3 Bullets)**
   - Follow-up: Add caching layer for frequently accessed chapters
   - Risk: R2 rate limits under high load

5. **Create PHR** (in appropriate `history/prompts/` subdirectory)

6. **Surface ADR Suggestion** (if decisions meet significance test)

**Minimum Acceptance Criteria:**
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant (e.g., `src/api/content.py:45-67`)

**Quality Gates:**
- Phase 1: Zero backend LLM calls (code audit)
- Phase 2: Hybrid features are premium-gated and isolated (functional test)
- Phase 3: Full responsive design, >80% test coverage (automated tests)

**Human as Tool Strategy:**
- Ambiguous requirements: Ask 2-3 targeted clarifying questions before proceeding
- Unforeseen dependencies: Surface dependencies and ask for prioritization
- Architectural uncertainty: Present options with tradeoffs, get user's preference
- Completion checkpoint: Summarize what was done, confirm next steps

## Governance

**This constitution supersedes all other development practices.**

**Amendment Process:**
1. Propose amendment with rationale and impact analysis
2. Update version following semantic versioning:
   - MAJOR: Backward-incompatible governance changes or principle removal
   - MINOR: New principle or materially expanded guidance
   - PATCH: Clarifications, wording fixes, non-semantic refinements
3. Document in Sync Impact Report
4. Update dependent templates (spec, plan, tasks)
5. Commit with message: `docs: amend constitution to vX.Y.Z (brief description)`

**Compliance Review:**
- All specs must verify compliance with Zero-Backend-LLM (Phase 1)
- All plans must justify hybrid features against cost/value criteria (Phase 2)
- All tasks must reference specs and include acceptance criteria
- All PRs reviewed for principle adherence before merge

**Version Increment Decision Criteria:**
- Adding/removing a principle → MINOR (unless removes existing requirement → MAJOR)
- Changing principle from SHOULD to MUST → MAJOR
- Clarifying existing principle wording → PATCH
- Adding new section (e.g., security standards) → MINOR

**Golden Rules (Non-Negotiable):**
1. Zero-Backend-LLM is the default. Hybrid intelligence must be selective, justified, and premium.
2. Your Spec is your Source Code. If you can describe excellence, AI can build it.
3. Start zero-LLM → add hybrid only where value is proven.
4. Phase 1 backend with any LLM calls → immediate disqualification.
5. All work originates from specs, plans, tasks. All decisions captured in PHRs and ADRs.

**Version**: 1.0.0 | **Ratified**: 2026-01-21 | **Last Amended**: 2026-01-21
