# Feature Specification: Phase 1 ChatGPT App (Zero-Backend-LLM)

**Feature Branch**: `phase-1-chatgpt-app`
**Created**: 2026-01-21
**Status**: Draft
**Input**: Build Course Companion FTE Phase 1 with ChatGPT App frontend and deterministic backend implementing all 6 required features with strict Zero-Backend-LLM architecture

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Content Delivery (Priority: P1)

As a student, I want to access course content through ChatGPT so I can learn course material with explanations tailored to my understanding level.

**Why this priority**: Core functionality - without content delivery, there's no educational value. This is the foundation for all other features.

**Independent Test**: Can be fully tested by requesting a chapter and verifying backend serves verbatim content while ChatGPT explains it adaptively. Delivers immediate learning value.

**Acceptance Scenarios**:

1. **Given** I'm a student enrolled in "AI Agent Development", **When** I ask "Show me Chapter 1", **Then** ChatGPT retrieves content from backend and explains it at my level
2. **Given** I'm viewing Chapter 3, **When** I ask "Explain this in simpler terms", **Then** ChatGPT re-explains using the same content with simpler language and analogies
3. **Given** I request a non-existent chapter, **When** I ask "Show me Chapter 99", **Then** backend returns 404 and ChatGPT gracefully explains chapter doesn't exist
4. **Given** course content includes code examples, **When** I view the chapter, **Then** ChatGPT presents code with explanations and can answer questions about it

---

### User Story 2 - Navigation (Priority: P1)

As a student, I want to navigate through course chapters sequentially so I can follow the learning path and progress through the material systematically.

**Why this priority**: Essential for structured learning - students need clear progression through material. Ties directly with Content Delivery as P1.

**Independent Test**: Can be fully tested by requesting next/previous chapter and verifying correct sequencing. Delivers organized learning experience.

**Acceptance Scenarios**:

1. **Given** I'm viewing Chapter 2, **When** I say "Next chapter", **Then** backend returns Chapter 3 data and ChatGPT presents it
2. **Given** I'm viewing Chapter 5, **When** I say "Previous chapter", **Then** backend returns Chapter 4 data and ChatGPT presents it
3. **Given** I'm on the first chapter, **When** I say "Previous chapter", **Then** ChatGPT informs me I'm at the beginning
4. **Given** I'm on the last chapter, **When** I say "Next chapter", **Then** ChatGPT informs me I've completed the course and suggests review or quizzes
5. **Given** I ask "What's the course structure?", **When** ChatGPT queries backend, **Then** I receive a chapter list with current progress indicated

---

### User Story 3 - Grounded Q&A (Priority: P2)

As a student, I want to ask questions about course content and receive answers grounded in the actual material so I can clarify concepts without misinformation.

**Why this priority**: High value for comprehension but depends on Content Delivery (P1). Enhances learning effectiveness significantly.

**Independent Test**: Can be fully tested by asking questions and verifying ChatGPT answers only using content retrieved from backend. Delivers deep comprehension support.

**Acceptance Scenarios**:

1. **Given** I've read Chapter 4 on "MCP Servers", **When** I ask "What are the benefits of MCP?", **Then** backend searches content and ChatGPT answers using only retrieved sections
2. **Given** I ask a question outside course scope, **When** I ask "How do I cook pasta?", **Then** ChatGPT politely redirects to course topics
3. **Given** I ask an ambiguous question, **When** I ask "What is that?", **Then** ChatGPT asks for clarification or suggests related course topics
4. **Given** my question relates to multiple chapters, **When** I ask "How does Agent Factory relate to MCP?", **Then** backend retrieves relevant sections from multiple chapters and ChatGPT synthesizes the answer

---

### User Story 4 - Rule-Based Quizzes (Priority: P2)

As a student, I want to test my understanding with quizzes so I can validate my learning and identify knowledge gaps.

**Why this priority**: Critical for learning validation but requires Content Delivery foundation. Assessment drives retention.

**Independent Test**: Can be fully tested by taking a quiz and verifying rule-based grading works correctly. Delivers immediate feedback on comprehension.

**Acceptance Scenarios**:

1. **Given** I've completed Chapter 2, **When** I say "Quiz me on Chapter 2", **Then** backend retrieves quiz and ChatGPT presents questions one at a time
2. **Given** I'm taking a quiz, **When** I answer a multiple-choice question correctly, **Then** backend grades it as correct and ChatGPT celebrates and explains why
3. **Given** I answer incorrectly, **When** I submit a wrong answer, **Then** backend grades it as incorrect and ChatGPT encourages me and explains the correct answer using course content
4. **Given** I complete a quiz, **When** all questions are answered, **Then** backend calculates score and ChatGPT presents results with encouraging feedback
5. **Given** quiz has different question types, **When** I take the quiz, **Then** I encounter multiple-choice, true/false, and fill-in-the-blank questions (all rule-graded)

---

### User Story 5 - Progress Tracking (Priority: P3)

As a student, I want to track my learning progress and streaks so I stay motivated and see my advancement through the course.

**Why this priority**: Enhances motivation but isn't blocking for core learning. Builds on completed chapters and quizzes.

**Independent Test**: Can be fully tested by completing chapters/quizzes and verifying progress is persisted and retrieved correctly. Delivers gamification and motivation.

**Acceptance Scenarios**:

1. **Given** I complete Chapter 3, **When** I finish reading it, **Then** backend marks it complete and updates my progress percentage
2. **Given** I have a learning streak, **When** I complete a chapter today after doing so yesterday, **Then** backend increments streak and ChatGPT celebrates
3. **Given** I ask about my progress, **When** I say "How am I doing?", **Then** ChatGPT retrieves stats from backend and presents completion %, streak, quizzes passed
4. **Given** I haven't studied in 2 days, **When** I return and complete something, **Then** backend resets streak to 1 and ChatGPT encourages me to rebuild it
5. **Given** I want to see detailed progress, **When** I ask "Show my course progress", **Then** ChatGPT displays chapters completed, quiz scores, and overall course completion

---

### User Story 6 - Freemium Gate (Priority: P3)

As a platform operator, I want to enforce freemium access control so free users can sample content while premium features are monetized.

**Why this priority**: Business requirement but not blocking for MVP learning experience. Should be implemented last.

**Independent Test**: Can be fully tested by attempting to access restricted content with free vs premium accounts. Delivers monetization capability.

**Acceptance Scenarios**:

1. **Given** I'm a free user, **When** I request Chapter 1-3, **Then** backend allows access and ChatGPT delivers content normally
2. **Given** I'm a free user, **When** I request Chapter 4, **Then** backend denies access and ChatGPT gracefully explains premium upgrade benefits
3. **Given** I'm a premium user ($9.99/mo), **When** I request any chapter, **Then** backend allows access to all chapters
4. **Given** I'm a free user viewing progress, **When** I ask "How am I doing?", **Then** ChatGPT shows my progress but hints at premium features (full analytics)
5. **Given** I'm a free user, **When** I complete the free chapters, **Then** ChatGPT congratulates me and presents upgrade options with clear value proposition

---

### Edge Cases

- **What happens when backend is unreachable?** ChatGPT should gracefully inform user of temporary unavailability and suggest trying again
- **What happens when a chapter is partially loaded?** Backend should return complete chapter or error, never partial content
- **What happens when user asks for quiz on incomplete chapter?** ChatGPT should check if chapter is read first, encourage completion before quizzing
- **What happens when two users have same username?** Backend enforces unique user IDs (email or UUID), usernames are display-only
- **What happens when free user exhausts free content in 10 minutes?** System should handle this gracefully - it's a feature, not a bug - and present upgrade path
- **What happens when course content is updated?** Backend serves latest version; user progress persists but refers to new content
- **What happens when user streak calculation crosses timezones?** Backend uses UTC timestamps and user's timezone for display, 24-hour window for streak maintenance

## Requirements *(mandatory)*

### Functional Requirements

**Zero-Backend-LLM Architecture (Constitutional Compliance)**

- **FR-001**: Backend MUST NOT contain any LLM API calls (ChatGPT, Claude, or any inference service)
- **FR-002**: Backend MUST NOT implement RAG summarization, semantic reasoning, or dynamic content generation
- **FR-003**: Backend MUST NOT perform prompt orchestration or agent loops
- **FR-004**: All intelligent reasoning, explanation, and adaptation MUST occur in ChatGPT App frontend
- **FR-005**: Backend MUST be purely deterministic (content retrieval, rule-based grading, calculations)

**Content Delivery**

- **FR-006**: Backend MUST serve course content verbatim from Cloudflare R2 storage
- **FR-007**: Content MUST be served via signed URLs with expiration (max 1 hour)
- **FR-008**: Backend MUST support content types: markdown, code blocks, images, embedded media
- **FR-009**: Backend MUST return 404 for non-existent chapters with clear error message
- **FR-010**: ChatGPT MUST explain content at learner's level without backend assistance

**Navigation**

- **FR-011**: Backend MUST provide next/previous chapter APIs based on course structure
- **FR-012**: Backend MUST return chapter metadata (title, number, duration estimate)
- **FR-013**: Backend MUST provide course structure API (all chapters with completion status)
- **FR-014**: ChatGPT MUST suggest optimal learning path based on user's progress data from backend

**Grounded Q&A**

- **FR-015**: Backend MUST provide keyword search API over course content
- **FR-016**: Backend MUST provide semantic search API using pre-computed embeddings (no runtime LLM)
- **FR-017**: Search results MUST include chapter reference and relevant text excerpts
- **FR-018**: ChatGPT MUST answer questions using ONLY content retrieved from backend
- **FR-019**: ChatGPT MUST cite chapter/section when answering questions

**Rule-Based Quizzes**

- **FR-020**: Backend MUST store quiz questions with predefined answer keys in database
- **FR-021**: Backend MUST support question types: multiple-choice, true/false, fill-in-blank
- **FR-022**: Backend MUST grade answers using exact string matching or regex patterns (rule-based only)
- **FR-023**: Backend MUST calculate quiz scores as percentage (correct/total)
- **FR-024**: Backend MUST persist quiz attempts with score and timestamp
- **FR-025**: ChatGPT MUST present questions one at a time and provide encouragement

**Progress Tracking**

- **FR-026**: Backend MUST track chapter completion per user (boolean: complete/incomplete)
- **FR-027**: Backend MUST calculate learning streaks (consecutive days with activity)
- **FR-028**: Backend MUST calculate course completion percentage
- **FR-029**: Backend MUST persist quiz scores per attempt
- **FR-030**: Backend MUST provide progress summary API (completion %, streak, quiz avg)
- **FR-031**: ChatGPT MUST motivate users and celebrate milestones using progress data

**Freemium Gate**

- **FR-032**: Backend MUST enforce access control based on user tier (free/premium/pro/team)
- **FR-033**: Free users MUST have access to first 3 chapters only
- **FR-034**: Premium users ($9.99/mo) MUST have access to all chapters and quizzes
- **FR-035**: Backend MUST return 403 with upgrade messaging when free user accesses restricted content
- **FR-036**: ChatGPT MUST gracefully explain premium benefits when access denied

**Data & Storage**

- **FR-037**: All course content MUST be stored in Cloudflare R2
- **FR-038**: User data (progress, quiz scores, streaks) MUST be stored in Neon or Supabase PostgreSQL
- **FR-039**: User authentication MUST use JWT tokens or session-based auth
- **FR-040**: Backend MUST enforce user data isolation (users can only access their own data)

**API Design**

- **FR-041**: All APIs MUST use FastAPI framework (Python 3.11+)
- **FR-042**: All request/response schemas MUST use Pydantic validation
- **FR-043**: All API responses MUST follow consistent error format (status, message, details)
- **FR-044**: All endpoints MUST require authentication except health check
- **FR-045**: All endpoints MUST return appropriate HTTP status codes (200, 404, 403, 500)

### Key Entities

- **Course**: Represents a complete course (e.g., "AI Agent Development")
  - Attributes: course_id, title, description, total_chapters, created_at
  - Stored in: PostgreSQL

- **Chapter**: Represents a single course chapter with content
  - Attributes: chapter_id, course_id, chapter_number, title, content_url (R2), estimated_duration
  - Stored in: PostgreSQL (metadata), Cloudflare R2 (content)

- **User**: Represents a student or learner
  - Attributes: user_id (UUID), email, tier (free/premium/pro/team), created_at
  - Stored in: PostgreSQL

- **Progress**: Tracks user's course progression
  - Attributes: user_id, chapter_id, completed (boolean), completed_at, streak_count
  - Stored in: PostgreSQL

- **Quiz**: Represents a quiz for a chapter
  - Attributes: quiz_id, chapter_id, questions (JSON array)
  - Stored in: PostgreSQL

- **QuizAttempt**: Records user's quiz attempts
  - Attributes: attempt_id, user_id, quiz_id, score (percentage), answers (JSON), attempted_at
  - Stored in: PostgreSQL

- **Question**: Individual quiz question (embedded in Quiz)
  - Attributes: question_id, question_text, question_type (multiple_choice/true_false/fill_in), correct_answer, options (for multiple choice)
  - Stored in: PostgreSQL (JSON within Quiz)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: ChatGPT App successfully delivers course content with zero backend LLM calls (verified via code audit)
- **SC-002**: Students can complete a full learning session (read chapter, take quiz, check progress) in under 10 minutes
- **SC-003**: System serves 100 concurrent students with <500ms average API response time
- **SC-004**: Backend infrastructure costs remain under $50/month for 10,000 users ($0.005 per user)
- **SC-005**: Quiz grading accuracy is 100% for rule-based questions (exact match or regex)
- **SC-006**: 90% of student questions are answered correctly using grounded Q&A (verified via user feedback)
- **SC-007**: Free-to-premium conversion funnel is clear with <3 clicks to upgrade
- **SC-008**: Progress tracking shows 99%+ data consistency (no lost progress due to race conditions)
- **SC-009**: Content delivery has 99.9% uptime (Cloudflare R2 SLA)
- **SC-010**: Students report 4.5+ satisfaction rating (out of 5) for ChatGPT explanation quality

### Cost Validation (Per Constitution)

- **SC-011**: Total monthly cost for 10,000 users: $16-41 as budgeted
  - Cloudflare R2: ~$5
  - Database (Neon/Supabase): $0-25
  - Compute (Fly.io/Railway): ~$10
  - Domain + SSL: ~$1
- **SC-012**: Cost per user: $0.002-$0.004 (meets constitutional target)
- **SC-013**: ChatGPT usage cost to developer: $0 (users access via their ChatGPT subscription)

### Architecture Validation (Constitutional Compliance)

- **SC-014**: Code audit confirms zero backend LLM calls in Phase 1 (disqualification test)
- **SC-015**: All backend logic is deterministic and testable without LLM dependencies
- **SC-016**: ChatGPT App handles all explanation, tutoring, and adaptation without backend AI
- **SC-017**: Clear separation between deterministic backend (APIs) and intelligent frontend (ChatGPT)

### Technical Quality Gates

- **SC-018**: All APIs have OpenAPI/Swagger documentation
- **SC-019**: Backend has >80% unit test coverage
- **SC-020**: Integration tests cover all 6 required features
- **SC-021**: No secrets hardcoded; all config via environment variables
- **SC-022**: Database queries use parameterized statements (SQL injection safe)
- **SC-023**: HTTPS enforced for all API endpoints
- **SC-024**: User data isolation verified via security testing

## Constitutional Compliance Checklist

- ✅ Zero-Backend-LLM: Backend contains NO LLM API calls, RAG, or agent loops
- ✅ All 6 Required Features: Content Delivery, Navigation, Grounded Q&A, Rule-Based Quizzes, Progress Tracking, Freemium Gate
- ✅ Cost Target: <$50/month for 10,000 users ($0.002-$0.004 per user)
- ✅ Tech Stack: FastAPI (Backend), OpenAI Apps SDK (Frontend), Cloudflare R2 (Storage), Neon/Supabase (Database)
- ✅ Quality Standards: 99%+ consistency, 24/7 availability, source-grounded responses
- ✅ Security: JWT auth, user isolation, HTTPS, no hardcoded secrets

## Out of Scope (Phase 1)

- ❌ Hybrid intelligence features (Phase 2 only)
- ❌ Backend LLM calls for any purpose
- ❌ Adaptive learning paths (requires backend AI)
- ❌ LLM-graded assessments (free-form answers)
- ❌ Web frontend (Phase 3 only)
- ❌ Admin dashboard (Phase 3 only)
- ❌ Analytics platform (Phase 3 only)
- ❌ Multi-language support (future)
- ❌ Real-time collaboration (future)
- ❌ Video content (future)

## Next Steps

1. **Architecture Planning**: Create `plan.md` with API design, database schema, and integration strategy
2. **Task Breakdown**: Create `tasks.md` with testable implementation tasks
3. **Agent Skills**: Define `concept-explainer.skill.md`, `quiz-master.skill.md`, `socratic-tutor.skill.md`, `progress-motivator.skill.md`
4. **Implementation**: Execute tasks following Red-Green-Refactor TDD cycle
5. **Validation**: Code audit to confirm zero backend LLM calls before Phase 1 completion

## Course Content Selection

Team must choose ONE course topic:
- **Option A**: AI Agent Development (Claude Agent SDK, MCP, Agent Skills)
- **Option B**: Cloud-Native Python (FastAPI, Containers, Kubernetes basics)
- **Option C**: Generative AI Fundamentals (LLMs, Prompting, RAG, Fine-tuning)
- **Option D**: Modern Python (Modern Python with Typing)

**Selected**: [TO BE DETERMINED - requires user input]
