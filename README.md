# Course Companion FTE - Agent Factory Hackathon IV

**A Digital Full-Time Equivalent Educational Tutor**
Building a 24/7 course companion using Zero-Backend-LLM architecture (Phase 1) with selective Hybrid Intelligence (Phase 2) and full Web App (Phase 3).

---

## Project Overview

Course Companion FTE is a production-ready educational platform that serves as a digital tutor working 168 hours/week at 85-90% cost savings compared to human tutors, while maintaining 99%+ consistency in educational delivery.

### Key Metrics
- **Availability**: 24/7 (168 hours/week)
- **Cost**: $0.002-$0.004 per user (Phase 1)
- **Scalability**: 10 to 100,000 users without linear cost increase
- **Consistency**: 99%+ in educational delivery
- **Quality**: Predictable, auditable, source-grounded responses

---

## Architecture

### Phase-Based Development

**Phase 1 - Zero-Backend-LLM (ChatGPT App)** ← Completed
- ChatGPT App frontend (OpenAI Apps SDK)
- Deterministic FastAPI backend
- NO backend LLM calls (constitutional requirement)
- Cost target: <$50/month for 10,000 users

**Phase 2 - Hybrid Intelligence (Selective Premium)** ← Completed
- Add max 2 hybrid features (premium-gated)
- Backend LLM calls for specific features only
- Cost tracking per user

**Phase 3 - Full Web App** ← Completed
- Next.js/React web application
- Consolidated backend
- LMS dashboard + analytics
- User authentication & profiles
- Course browsing & navigation
- Quiz interface & assessment tools
- Responsive design & accessibility
- Performance optimization

### Agent Factory 8-Layer Architecture

| Layer | Technology | Phase 1 | Phase 2 | Phase 3 |
|-------|-----------|---------|---------|---------|
| L0: Sandbox | gVisor | - | ✅ | ✅ |
| L1: Events | Apache Kafka | - | ✅ | ✅ |
| L2: Infra | Dapr + Workflows | - | ✅ | ✅ |
| L3: HTTP | FastAPI | ✅ | ✅ | ✅ |
| L4: High-Level | OpenAI Agents SDK | - | ✅ | ✅ |
| L5: Agentic | Claude Agent SDK | - | ✅ | ✅ |
| L6: Skills | Runtime Skills + MCP | ✅ | ✅ | ✅ |
| L7: A2A | Agent-to-Agent Protocol | - | ✅ | ✅ |

---

## Project Structure

```
Agent-Factory-Hackathon-4/
├── .claude/                          # Claude Code configuration
│   ├── commands/                     # Custom slash commands
│   └── skills/                       # Agent runtime skills
│       ├── concept-explainer/        # Explain concepts at various levels
│       ├── quiz-master/              # Guide quizzes with encouragement
│       ├── socratic-tutor/           # Guide learning through questions
│       └── progress-motivator/       # Celebrate achievements, motivate
│
├── .specify/                         # Spec-Driven Development artifacts
│   ├── memory/
│   │   └── constitution.md           # Project constitution (v1.0.0)
│   ├── templates/                    # SDD templates
│   └── scripts/                      # Automation scripts
│
├── specs/                            # Feature specifications
│   └── phase-1-chatgpt-app/
│       ├── spec.md                   # Phase 1 requirements
│       ├── plan.md                   # Architecture decisions (TBD)
│       └── tasks.md                  # Implementation tasks (TBD)
│
├── backend/                          # FastAPI backend
│   ├── api/
│   │   ├── routes/                   # API endpoints
│   │   ├── models/                   # Database models (SQLModel)
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   └── middleware/               # Auth, CORS, logging
│   ├── core/                         # Config, constants, utils
│   ├── db/                           # Database connection, migrations
│   ├── services/                     # Business logic
│   └── tests/
│       ├── unit/                     # Unit tests
│       └── integration/              # Integration tests
│
├── chatgpt-app/                      # ChatGPT App frontend (Phase 1 & 2)
│   ├── src/                          # App source
│   ├── config/                       # App manifest (YAML)
│   └── tests/                        # App tests
│
├── content/                          # Course content storage
│   ├── courses/                      # Course material (markdown, code)
│   ├── quizzes/                      # Quiz banks (JSON)
│   └── assets/                       # Images, media
│
├── docs/                             # Documentation
│   ├── api/                          # API documentation (OpenAPI/Swagger)
│   ├── architecture/                 # Architecture diagrams, ADRs
│   └── guides/                       # Setup, deployment guides
│
├── scripts/                          # Utility scripts
│   ├── data/                         # Data migration, seed scripts
│   └── deployment/                   # Deployment automation
│
├── history/                          # Spec-Driven Development history
│   ├── prompts/                      # Prompt History Records (PHRs)
│   │   ├── constitution/             # Constitution-related PHRs
│   │   ├── phase-1-chatgpt-app/      # Feature-specific PHRs
│   │   └── general/                  # General PHRs
│   └── adr/                          # Architectural Decision Records
│
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── CLAUDE.md                         # Claude Code rules & guidelines
├── README.md                         # This file
└── requirements.txt                  # Python dependencies
```

---

## Features (Phase 1)

### 1. Content Delivery
- **Backend**: Serves content verbatim from Cloudflare R2
- **ChatGPT**: Explains at learner's level with adaptive complexity

### 2. Navigation
- **Backend**: Returns next/previous chapter sequencing
- **ChatGPT**: Suggests optimal learning path based on progress

### 3. Grounded Q&A
- **Backend**: Returns relevant content sections via search
- **ChatGPT**: Answers using ONLY retrieved content (source-grounded)

### 4. Rule-Based Quizzes
- **Backend**: Grades with predefined answer keys (exact match/regex)
- **ChatGPT**: Presents questions, encourages, explains answers

### 5. Progress Tracking
- **Backend**: Stores completion, streaks, quiz scores
- **ChatGPT**: Motivates and celebrates milestones

### 6. Freemium Gate
- **Backend**: Enforces access control by tier
- **ChatGPT**: Gracefully explains premium benefits

---

## Agent Skills

### Concept Explainer
**Triggers**: "explain", "what is", "how does"
**Purpose**: Adapt course content explanations to learner's level
**Techniques**: Analogies, examples, complexity matching

### Quiz Master
**Triggers**: "quiz me", "test me", "practice"
**Purpose**: Conduct engaging quizzes with encouraging feedback
**Techniques**: Celebration, growth mindset framing, specific praise

### Socratic Tutor
**Triggers**: "help me think", "I'm stuck"
**Purpose**: Guide learning through questions, not answers
**Techniques**: Strategic questioning, scaffolding, discovery

### Progress Motivator
**Triggers**: "my progress", "how am I doing"
**Purpose**: Celebrate achievements, maintain motivation
**Techniques**: Gamification, milestones, personalized insights

---

## Technology Stack

### Frontend (Phase 1)
- **ChatGPT App**: OpenAI Apps SDK
- **Interface**: Conversational UI

### Backend (All Phases)
- **Framework**: FastAPI (Python 3.11+)
- **Validation**: Pydantic v2
- **ORM**: SQLModel or Prisma
- **Type Safety**: Python type hints (required)

### Storage (All Phases)
- **Content**: Cloudflare R2
- **Database**: Neon or Supabase (PostgreSQL)

### Deployment (Phase 1)
- **Backend**: Fly.io or Railway
- **Storage**: Cloudflare R2
- **Database**: Neon (serverless PostgreSQL)

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+ (for ChatGPT App development)
- Git
- Cloudflare account (for R2 storage)
- Neon or Supabase account (for database)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Agent-Factory-Hackathon-4
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Run database migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

5. **Start backend development server**
   ```bash
   uvicorn backend.main:app --reload
   ```

6. **Access API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Development Workflow

1. **Create feature spec** in `specs/<feature-name>/spec.md`
2. **Create plan** in `specs/<feature-name>/plan.md`
3. **Break down tasks** in `specs/<feature-name>/tasks.md`
4. **Implement with TDD** (Red-Green-Refactor)
5. **Document with PHR** after completing
6. **Suggest ADR** for architecturally significant decisions

---

## Constitutional Requirements

### Zero-Backend-LLM (Phase 1 - NON-NEGOTIABLE)

**Backend MUST NOT contain:**
- ❌ LLM API calls (ChatGPT, Claude, any inference)
- ❌ RAG summarization or semantic reasoning
- ❌ Prompt orchestration or agent loops
- ❌ Dynamic content generation via AI

**Backend MUST provide:**
- ✅ Deterministic content APIs (verbatim from R2)
- ✅ Rule-based navigation
- ✅ Keyword/semantic search (pre-computed embeddings)
- ✅ Progress tracking and calculations
- ✅ Access control enforcement
- ✅ Rule-based quiz grading (exact match/regex)

**⚠️ DISQUALIFICATION RULE**: Any backend LLM inference in Phase 1 results in immediate project disqualification.

---

## Cost Budget (Phase 1)

**Target: $0.002-$0.004 per user**

| Component | Monthly Cost (10K users) |
|-----------|-------------------------|
| Cloudflare R2 | ~$5 |
| Database (Neon/Supabase) | $0-$25 |
| Compute (Fly.io/Railway) | ~$10 |
| Domain + SSL | ~$1 |
| **TOTAL** | **$16-$41** |

**ChatGPT Usage**: $0 to developer (users access via their ChatGPT subscription)

---

## Testing Strategy

### Unit Tests (>80% coverage)
```bash
pytest backend/tests/unit/
```

### Integration Tests
```bash
pytest backend/tests/integration/
```

### API Tests
```bash
pytest backend/tests/api/
```

### ChatGPT App Tests
```bash
cd chatgpt-app
npm test
```

---

## Deployment

### Phase 1 Deployment

1. **Deploy Backend to Fly.io**
   ```bash
   fly deploy
   ```

2. **Configure Cloudflare R2**
   - Create bucket
   - Upload course content
   - Set CORS policies

3. **Configure Database**
   - Provision Neon PostgreSQL
   - Run migrations
   - Seed initial data

4. **Deploy ChatGPT App**
   - Follow OpenAI Apps deployment guide
   - Configure backend URL
   - Test in ChatGPT

---

## Monitoring & Observability

### Metrics to Track
- API response times (p50, p95, p99)
- Error rates by endpoint
- Database query performance
- Storage bandwidth usage
- User activity patterns
- Cost per user

### Logging
- Structured JSON logs
- Request/response logging
- Error tracking with stack traces
- User action audit trail

---

## Contributing

### Development Principles
1. **Spec-Driven Development**: All work starts with specs
2. **TDD (Test-Driven Development)**: Tests before implementation
3. **Constitutional Compliance**: Verify against `.specify/memory/constitution.md`
4. **Documentation**: Update docs alongside code
5. **PHR Creation**: Record significant user interactions

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types**: feat, fix, docs, test, refactor, chore

---

## Course Content Options

Choose ONE course topic to build FTE around:

- **Option A**: AI Agent Development (Claude Agent SDK, MCP, Agent Skills)
- **Option B**: Cloud-Native Python (FastAPI, Containers, Kubernetes)
- **Option C**: Generative AI Fundamentals (LLMs, Prompting, RAG, Fine-tuning)
- **Option D**: Modern Python (Modern Python with Typing)

**Selected**: [TO BE DETERMINED]

---

## License

[TO BE DETERMINED]

---

## Acknowledgments

- **Panaversity** - Agent Factory Development Hackathon IV
- **Agent Factory Architecture** - 8-layer reference architecture
- **Spec-Driven Development** - Methodology foundation

---

## Support

For questions or issues:
- Create an issue in this repository
- Contact: [TO BE DETERMINED]

---

## Project Status

- [x] Constitution created (v1.0.0)
- [x] Phase 1 spec created
- [x] Agent skills defined (4 skills with REFERENCE.md)
- [x] Project structure initialized
- [x] Phase 1 plan created
- [x] Phase 1 tasks defined
- [x] Phase 1 Backend implementation
- [x] Phase 1 ChatGPT App implementation
- [x] Phase 1 Testing & validation
- [x] Phase 1 Deployment
- [x] Phase 2 Hybrid Intelligence implementation
- [x] Phase 2 Testing & validation
- [x] Phase 2 Deployment
- [x] Phase 3 plan created
- [x] Phase 3 tasks defined
- [x] Phase 3 Full Web App implementation
- [x] Phase 3 Testing & validation
- [x] Phase 3 Deployment

**Current Phase**: Project Complete
