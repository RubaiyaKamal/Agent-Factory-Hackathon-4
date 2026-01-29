# Tasks: Phase 1 ChatGPT App (Zero-Backend-LLM)

**Input**: Design documents from `/specs/phase-1-chatgpt-app/`
**Prerequisites**: plan.md (✅), spec.md (✅)

**Tests**: Tests are integrated throughout based on TDD approach per constitution

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

## Path Conventions

This is a **Web App** project:
- Backend: `backend/` (FastAPI)
- Frontend: `chatgpt-app/` (OpenAI Apps SDK)
- Tests: `backend/tests/` (unit, integration)
- Content: `content/` (courses, quizzes)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Verify project structure matches plan.md (backend/, chatgpt-app/, content/, docs/, scripts/)
- [ ] T002 [P] Install Python dependencies from requirements.txt in virtual environment
- [ ] T003 [P] Configure pre-commit hooks (black, ruff, mypy) in .pre-commit-config.yaml
- [ ] T004 [P] Create .env file from .env.example and fill required values (SECRET_KEY, DATABASE_URL, R2 credentials)
- [ ] T005 [P] Verify constitutional compliance: run backend/main.py startup check to ensure no LLM imports

**Checkpoint**: Environment configured, dependencies installed, constitutional compliance verified

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Core Infrastructure

- [ ] T006 Create database session management in backend/db/session.py (async SQLModel engine, session factory)
- [ ] T007 Create base SQLModel classes in backend/db/base.py (imports for all models, Alembic base)
- [ ] T008 Initialize Alembic in backend/db/ (alembic init, configure alembic.ini and env.py for async)
- [ ] T009 [P] Create User model in backend/api/models/user.py (id, email, hashed_password, tier, timezone, timestamps)
- [ ] T010 [P] Create Course model in backend/api/models/course.py (id, title, description, difficulty, total_chapters)
- [ ] T011 [P] Create Chapter model in backend/api/models/chapter.py (id, course_id, chapter_number, title, content_key, duration)
- [ ] T012 Create initial Alembic migration (001_initial_schema.py) for users, courses, chapters tables
- [ ] T013 Run Alembic migration to create tables in Neon PostgreSQL (alembic upgrade head)

### Authentication Infrastructure

- [ ] T014 Implement password hashing utilities in backend/core/security.py (hash_password, verify_password using bcrypt)
- [ ] T015 Implement JWT token utilities in backend/core/security.py (create_access_token, create_refresh_token, decode_token)
- [ ] T016 Create authentication middleware in backend/api/middleware/auth.py (get_current_user, verify JWT)
- [ ] T017 Implement authentication routes in backend/api/routes/auth.py (register, login, refresh endpoints)
- [ ] T018 Create Pydantic schemas for auth in backend/api/schemas/auth.py (RegisterRequest, LoginRequest, TokenResponse)

### Storage & Utilities

- [ ] T019 Implement Cloudflare R2 client in backend/services/r2.py (init_client, generate_signed_url, upload_content)
- [ ] T020 Create custom exception classes in backend/core/exceptions.py (AuthenticationError, NotFoundError, ForbiddenError, ValidationError)
- [ ] T021 [P] Implement rate limiting middleware in backend/api/middleware/rate_limit.py (tier-based limits per constants.py)
- [ ] T022 [P] Configure CORS middleware in backend/main.py (already present, verify settings from .env)

### Testing Infrastructure

- [ ] T023 Create pytest conftest.py with fixtures (test_db, client, auth_headers, sample_course)
- [ ] T024 [P] Write unit tests for security utils in backend/tests/unit/test_security.py (password hashing, JWT creation/validation)
- [ ] T025 [P] Write integration tests for auth endpoints in backend/tests/integration/test_api_auth.py (register, login, refresh, invalid credentials)

**Checkpoint**: Foundation ready - database connected, auth working, R2 configured, user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Content Delivery (Priority: P1) 🎯 MVP

**Goal**: Enable students to access course content through ChatGPT with backend serving verbatim content from R2

**Independent Test**: Request Chapter 1 via API, verify signed R2 URL returned, fetch content, confirm ChatGPT can explain it

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T026 [P] [US1] Unit test for R2 signed URL generation in backend/tests/unit/test_r2_client.py
- [ ] T027 [P] [US1] Integration test for GET /api/content/chapters/{id} in backend/tests/integration/test_api_content.py
- [ ] T028 [P] [US1] Integration test for content delivery error cases (404, 403) in backend/tests/integration/test_api_content.py

### Implementation for User Story 1

- [ ] T029 [P] [US1] Create ChapterEmbedding model in backend/api/models/chapter.py (for future semantic search, empty for now)
- [ ] T030 [US1] Create Pydantic schemas in backend/api/schemas/content.py (ChapterResponse, CourseListResponse, ContentResponse)
- [ ] T031 [US1] Implement content service in backend/services/content_service.py (get_chapter_by_id, generate_content_url, list_courses)
- [ ] T032 [US1] Implement content delivery routes in backend/api/routes/content.py (GET /courses, GET /chapters/{id})
- [ ] T033 [US1] Add R2 health check to /health endpoint in backend/main.py (verify R2 connectivity)
- [ ] T034 [US1] Add validation for content access in backend/api/routes/content.py (verify chapter exists, belongs to course)
- [ ] T035 [US1] Add error handling for R2 failures in backend/services/content_service.py (retry logic, graceful degradation)

### Content Setup

- [ ] T036 [US1] Create sample course structure in content/courses/ai-agent-development/ (choose course topic from 4 options)
- [ ] T037 [US1] Write 3 sample chapters as markdown in content/courses/ai-agent-development/ (chapter-01.md, chapter-02.md, chapter-03.md)
- [ ] T038 [US1] Create upload script in scripts/data/upload_content_to_r2.py (reads markdown, uploads to R2, inserts metadata into database)
- [ ] T039 [US1] Run upload script to populate R2 and database with sample content

**Checkpoint**: User Story 1 complete - backend serves content via signed URLs, ChatGPT can retrieve and explain content

---

## Phase 4: User Story 2 - Navigation (Priority: P1)

**Goal**: Enable students to navigate through course chapters sequentially (next/previous/structure)

**Independent Test**: Request next chapter from Chapter 2, verify Chapter 3 returned; request course structure, verify chapter list with completion status

### Tests for User Story 2

- [ ] T040 [P] [US2] Integration test for GET /api/navigation/chapters/{id}/next in backend/tests/integration/test_api_navigation.py
- [ ] T041 [P] [US2] Integration test for GET /api/navigation/courses/{id}/structure in backend/tests/integration/test_api_navigation.py
- [ ] T042 [P] [US2] Integration test for navigation edge cases (first/last chapter) in backend/tests/integration/test_api_navigation.py

### Implementation for User Story 2

- [ ] T043 [P] [US2] Create Progress model in backend/api/models/progress.py (id, user_id, chapter_id, completed, completed_at)
- [ ] T044 [US2] Create Alembic migration (002_add_progress.py) for progress table with indexes on (user_id, chapter_id)
- [ ] T045 [US2] Run migration (alembic upgrade head)
- [ ] T046 [US2] Create Pydantic schemas in backend/api/schemas/navigation.py (CourseStructureResponse, ChapterNavigation, NextChapterResponse)
- [ ] T047 [US2] Implement navigation service in backend/services/navigation_service.py (get_next_chapter, get_previous_chapter, get_course_structure)
- [ ] T048 [US2] Implement navigation routes in backend/api/routes/navigation.py (GET /chapters/{id}/next, GET /chapters/{id}/previous, GET /courses/{id}/structure)
- [ ] T049 [US2] Add completion status calculation in backend/services/navigation_service.py (query user progress, mark completed chapters)
- [ ] T050 [US2] Add boundary handling (first chapter has no previous, last chapter has no next) in backend/services/navigation_service.py

**Checkpoint**: User Story 2 complete - students can navigate chapters sequentially, see course structure with progress

---

## Phase 5: User Story 3 - Grounded Q&A (Priority: P2)

**Goal**: Enable students to ask questions and receive answers grounded in course content via search

**Independent Test**: Search for "MCP benefits", verify relevant chapter sections returned; ask question, verify ChatGPT uses only retrieved content

### Tests for User Story 3

- [ ] T051 [P] [US3] Unit test for keyword search in backend/tests/unit/test_search.py (query matching, relevance scoring)
- [ ] T052 [P] [US3] Unit test for semantic search (when implemented) in backend/tests/unit/test_search.py (embedding similarity, threshold)
- [ ] T053 [P] [US3] Integration test for GET /api/search in backend/tests/integration/test_api_search.py (keyword, semantic, pagination)

### Implementation for User Story 3

- [ ] T054 [US3] Create Pydantic schemas in backend/api/schemas/search.py (SearchRequest, SearchResult, SearchResponse)
- [ ] T055 [US3] Implement keyword search service in backend/services/search.py (search_content_keyword using PostgreSQL LIKE/ILIKE)
- [ ] T056 [US3] Implement semantic search service in backend/services/search.py (load sentence-transformers model, search_content_semantic using cosine similarity)
- [ ] T057 [US3] Implement embedding generation in backend/services/embeddings.py (generate_content_embeddings for all chapters, store in database)
- [ ] T058 [US3] Create script to pre-compute embeddings in scripts/data/generate_embeddings.py (reads chapters, generates embeddings, updates chapter_embeddings table)
- [ ] T059 [US3] Run embedding generation script for existing content
- [ ] T060 [US3] Implement search routes in backend/api/routes/search.py (GET /search with query, type, limit parameters)
- [ ] T061 [US3] Add search result ranking logic in backend/services/search.py (combine keyword + semantic scores if both enabled)
- [ ] T062 [US3] Add query validation in backend/api/routes/search.py (min length, sanitization)

**Checkpoint**: User Story 3 complete - students can search content, ChatGPT can answer questions using retrieved sections

---

## Phase 6: User Story 4 - Rule-Based Quizzes (Priority: P2)

**Goal**: Enable students to take quizzes with rule-based grading and immediate feedback

**Independent Test**: Request quiz for Chapter 2, submit answers, verify rule-based grading returns correct score and explanations

### Tests for User Story 4

- [ ] T063 [P] [US4] Unit test for quiz grader in backend/tests/unit/test_quiz_grader.py (multiple-choice, true/false, fill-in-blank grading)
- [ ] T064 [P] [US4] Integration test for GET /api/quizzes/chapters/{id}/quiz in backend/tests/integration/test_api_quizzes.py
- [ ] T065 [P] [US4] Integration test for POST /api/quizzes/{id}/submit in backend/tests/integration/test_api_quizzes.py (correct/incorrect answers, score calculation)

### Implementation for User Story 4

- [ ] T066 [P] [US4] Create Quiz model in backend/api/models/quiz.py (id, chapter_id, passing_score)
- [ ] T067 [P] [US4] Create Question model in backend/api/models/quiz.py (id, quiz_id, question_text, type, correct_answer, options, explanation, difficulty)
- [ ] T068 [P] [US4] Create QuizAttempt model in backend/api/models/quiz.py (id, user_id, quiz_id, score, answers JSON, passed, attempted_at)
- [ ] T069 [US4] Create Alembic migration (003_add_quizzes.py) for quizzes, questions, quiz_attempts tables
- [ ] T070 [US4] Run migration (alembic upgrade head)
- [ ] T071 [US4] Create Pydantic schemas in backend/api/schemas/quiz.py (QuizResponse, QuestionResponse, SubmitQuizRequest, QuizResultResponse)
- [ ] T072 [US4] Implement QuizGrader service in backend/services/quiz_grader.py (grade_multiple_choice, grade_true_false, grade_fill_in_blank)
- [ ] T073 [US4] Implement quiz service in backend/services/quiz_service.py (get_quiz_by_chapter, submit_quiz, calculate_score, get_attempt_history)
- [ ] T074 [US4] Implement quiz routes in backend/api/routes/quizzes.py (GET /chapters/{id}/quiz, POST /{id}/submit, GET /{id}/attempts)
- [ ] T075 [US4] Add max attempts validation in backend/services/quiz_service.py (check QUIZ_MAX_ATTEMPTS from settings)
- [ ] T076 [US4] Add quiz result formatting in backend/services/quiz_service.py (per-question feedback with explanations)

### Quiz Content Creation

- [ ] T077 [US4] Create sample quiz JSON files in content/quizzes/ai-agent-development/ (quiz-01.json, quiz-02.json, quiz-03.json)
- [ ] T078 [US4] Create quiz upload script in scripts/data/upload_quizzes.py (reads JSON, inserts into database)
- [ ] T079 [US4] Run quiz upload script to populate database with sample quizzes

**Checkpoint**: User Story 4 complete - students can take quizzes, receive rule-based grades and feedback

---

## Phase 7: User Story 5 - Progress Tracking (Priority: P3)

**Goal**: Enable students to track learning progress, streaks, and completion statistics

**Independent Test**: Complete Chapter 3, verify progress updated; check streak after consecutive days, verify calculation correct

### Tests for User Story 5

- [ ] T080 [P] [US5] Unit test for streak calculation in backend/tests/unit/test_progress_calculator.py (consecutive days, gap handling, timezone)
- [ ] T081 [P] [US5] Unit test for completion percentage in backend/tests/unit/test_progress_calculator.py
- [ ] T082 [P] [US5] Integration test for GET /api/progress/me in backend/tests/integration/test_api_progress.py
- [ ] T083 [P] [US5] Integration test for POST /api/progress/chapters/{id}/complete in backend/tests/integration/test_api_progress.py

### Implementation for User Story 5

- [ ] T084 [P] [US5] Create UserActivity model in backend/api/models/progress.py (id, user_id, activity_date, activity_count)
- [ ] T085 [US5] Create Alembic migration (004_add_user_activity.py) for user_activity table with composite unique index on (user_id, activity_date)
- [ ] T086 [US5] Run migration (alembic upgrade head)
- [ ] T087 [US5] Create Pydantic schemas in backend/api/schemas/progress.py (ProgressSummaryResponse, StreakResponse, CompleteChapterRequest)
- [ ] T088 [US5] Implement progress calculator service in backend/services/progress_calculator.py (calculate_streak, calculate_completion_percentage, update_user_activity)
- [ ] T089 [US5] Implement progress service in backend/services/progress_service.py (get_user_progress, mark_chapter_complete, get_streak_details)
- [ ] T090 [US5] Implement progress routes in backend/api/routes/progress.py (GET /me, POST /chapters/{id}/complete, GET /streak)
- [ ] T091 [US5] Add timezone handling in backend/services/progress_calculator.py (convert UTC to user timezone for streak calculation)
- [ ] T092 [US5] Add achievement detection logic in backend/services/progress_service.py (check milestones: 25%, 50%, 75%, 100%, streaks)
- [ ] T093 [US5] Store total study time estimation in backend/services/progress_service.py (sum chapter durations for completed chapters)

**Checkpoint**: User Story 5 complete - students can track progress, streaks, and see achievement milestones

---

## Phase 8: User Story 6 - Freemium Gate (Priority: P3)

**Goal**: Enforce tier-based access control (free: 3 chapters, premium: all chapters)

**Independent Test**: As free user, request Chapter 4, verify 403 with upgrade message; as premium user, verify access granted

### Tests for User Story 6

- [ ] T094 [P] [US6] Integration test for free tier limits in backend/tests/integration/test_api_access_control.py (chapter 4 denied for free user)
- [ ] T095 [P] [US6] Integration test for premium tier access in backend/tests/integration/test_api_access_control.py (all chapters allowed)
- [ ] T096 [P] [US6] Integration test for quiz limits in backend/tests/integration/test_api_access_control.py (3 quiz max for free tier)

### Implementation for User Story 6

- [ ] T097 [US6] Implement access control middleware in backend/api/middleware/access.py (check_chapter_access, check_quiz_access functions)
- [ ] T098 [US6] Add tier checking logic in backend/api/middleware/access.py (query user tier, apply FREE_TIER_CHAPTER_LIMIT and FREE_TIER_QUIZ_LIMIT from settings)
- [ ] T099 [US6] Apply access middleware to content routes in backend/api/routes/content.py (Depends(check_chapter_access))
- [ ] T100 [US6] Apply access middleware to quiz routes in backend/api/routes/quizzes.py (Depends(check_quiz_access))
- [ ] T101 [US6] Create upgrade endpoint in backend/api/routes/auth.py (GET /upgrade returns tier options and pricing)
- [ ] T102 [US6] Add 403 error response formatting in backend/api/middleware/access.py (include upgrade_url, tier options in response)
- [ ] T103 [US6] Add tier expiration checking in backend/api/middleware/auth.py (verify tier_expires_at for premium users)

**Checkpoint**: User Story 6 complete - freemium access control enforced, free users can sample content, premium features gated

---

## Phase 9: ChatGPT App Frontend

**Purpose**: Build ChatGPT App frontend that integrates with backend API and uses agent skills

### ChatGPT App Setup

- [ ] T104 Create ChatGPT App manifest in chatgpt-app/src/app.yaml (OpenAI Apps SDK format, define actions and backend URL)
- [ ] T105 [P] Copy agent skill references to chatgpt-app/src/skills/ (concept-explainer.md, quiz-master.md, socratic-tutor.md, progress-motivator.md)
- [ ] T106 Configure backend API connection in chatgpt-app/config/backend.json (API base URL, auth method)
- [ ] T107 Define custom actions in chatgpt-app/src/actions/ (if needed beyond standard API calls)

### ChatGPT App Integration

- [ ] T108 Implement content delivery action (calls GET /api/content/chapters/{id}, presents to user)
- [ ] T109 Implement navigation action (calls GET /api/navigation/courses/{id}/structure, helps user navigate)
- [ ] T110 Implement search action (calls GET /api/search, retrieves relevant sections for Q&A)
- [ ] T111 Implement quiz action (calls GET /api/quizzes/chapters/{id}/quiz, POST /api/quizzes/{id}/submit, presents results)
- [ ] T112 Implement progress action (calls GET /api/progress/me, presents stats with motivation)
- [ ] T113 Add error handling for API failures in ChatGPT App (graceful degradation, user-friendly messages)

### End-to-End Testing

- [ ] T114 [P] Write E2E test for complete learning session in backend/tests/e2e/test_student_journey.py (register → login → view chapter → quiz → check progress)
- [ ] T115 [P] Write E2E test for ChatGPT integration in backend/tests/e2e/test_chatgpt_integration.py (mock ChatGPT → backend API calls)
- [ ] T116 Manual testing: Deploy to staging, test full user journey in actual ChatGPT interface

**Checkpoint**: ChatGPT App complete - frontend communicates with backend, all 6 features accessible via conversational UI

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Documentation

- [ ] T117 [P] Update API documentation with complete OpenAPI spec in docs/api/ (generate from FastAPI /openapi.json)
- [ ] T118 [P] Create deployment guide in docs/guides/deployment.md (Fly.io setup, environment config, R2 setup)
- [ ] T119 [P] Create developer quickstart in docs/guides/quickstart.md (local setup, running tests, sample requests)

### Performance & Optimization

- [ ] T120 [P] Add database query optimization (indexes on frequently queried columns per plan.md)
- [ ] T121 [P] Add API response caching for static content in backend/api/middleware/cache.py (content, course structure)
- [ ] T122 [P] Add database connection pooling configuration in backend/db/session.py (set pool_size, max_overflow from settings)

### Security Hardening

- [ ] T123 [P] Run security audit (check for hardcoded secrets, SQL injection vulnerabilities, XSS)
- [ ] T124 [P] Add request validation for all endpoints (validate input lengths, formats, SQL injection prevention)
- [ ] T125 [P] Add HTTPS enforcement in production (Fly.io configuration, redirect HTTP to HTTPS)

### Monitoring & Observability

- [ ] T126 [P] Add Prometheus metrics endpoints in backend/main.py (request latency, error rates, database queries)
- [ ] T127 [P] Add structured logging throughout backend (use python-json-logger per requirements.txt)
- [ ] T128 [P] Add health check for all dependencies in /health endpoint (database, R2, cache)

### Code Quality

- [ ] T129 [P] Run full test suite and achieve >80% coverage (pytest --cov=backend --cov-report=html)
- [ ] T130 [P] Run linting and formatting (black, ruff, mypy) and fix all issues
- [ ] T131 [P] Code review checklist: verify no LLM imports, all secrets in .env, error handling complete

### Final Validation

- [ ] T132 Run constitutional compliance audit (verify zero backend LLM calls, check startup logs)
- [ ] T133 Run cost analysis (calculate actual costs for 10K users, verify under $16-41 target)
- [ ] T134 Validate all 6 user stories independently (test each feature in isolation)
- [ ] T135 Create demo video showing all 6 features (ChatGPT App → Backend → Database flow)

**Checkpoint**: Phase 1 complete - ready for production deployment, all features tested, documented, and optimized

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-8)**: All depend on Foundational phase completion
  - US1 (Content Delivery): Can start after Foundational - No dependencies on other stories
  - US2 (Navigation): Can start after Foundational - Minimal dependency on US1 (needs Progress model, but can mock initially)
  - US3 (Grounded Q&A): Can start after Foundational - Depends on US1 (needs content in database)
  - US4 (Rule-Based Quizzes): Can start after Foundational - Independent of other stories (needs separate quiz tables)
  - US5 (Progress Tracking): Can start after Foundational - Depends on US1, US2 (needs chapters and completion tracking)
  - US6 (Freemium Gate): Can start after Foundational - Applies to US1, US4 (modifies access control)
- **ChatGPT App (Phase 9)**: Depends on all desired user stories being implemented (backend APIs must exist)
- **Polish (Phase 10)**: Depends on ChatGPT App completion

### Recommended Execution Order

**Sequential (Single Developer)**:
1. Setup → Foundational → US1 → US2 → US3 → US4 → US5 → US6 → ChatGPT App → Polish

**Parallel (Multiple Developers)**:
1. Setup → Foundational (team completes together)
2. Once Foundational done, split:
   - Developer A: US1 (Content Delivery) → US3 (Grounded Q&A, depends on US1)
   - Developer B: US2 (Navigation) → US5 (Progress Tracking, depends on US2)
   - Developer C: US4 (Rule-Based Quizzes) → US6 (Freemium Gate, modifies US1 & US4)
3. Once all user stories done: ChatGPT App (single developer)
4. Final: Polish (can be parallelized)

### MVP Path (Fastest to Demo)

**Minimum Viable Product** (User Story 1 only):
1. Phase 1: Setup (T001-T005)
2. Phase 2: Foundational (T006-T025) - Critical foundation
3. Phase 3: User Story 1 (T026-T039) - Content Delivery only
4. Phase 9 (partial): ChatGPT App Setup (T104-T108) - Just content delivery action
5. **STOP and DEMO**: Students can view course content via ChatGPT

This gives you a working demo in ~30-40 tasks instead of all 135 tasks.

### Parallel Opportunities (Within Each Phase)

**Setup Phase**: T002, T003, T004, T005 can run in parallel

**Foundational Phase**:
- Models (T009, T010, T011) can run in parallel
- Services (T021, T024, T025) can run in parallel after models complete

**User Story 1**:
- Tests (T026, T027, T028) can run in parallel (write all tests first)
- Model (T029) and Schemas (T030) can run in parallel

**User Story 2**:
- Tests (T040, T041, T042) can run in parallel
- Model (T043) and Schemas (T046) can run in parallel

**User Story 3**:
- Tests (T051, T052, T053) can run in parallel

**User Story 4**:
- Models (T066, T067, T068) can run in parallel
- Tests (T063, T064, T065) can run in parallel

**User Story 5**:
- Tests (T080, T081, T082, T083) can run in parallel
- Model (T084) and Schemas (T087) can run in parallel

**User Story 6**:
- Tests (T094, T095, T096) can run in parallel

**Polish Phase**:
- All documentation tasks (T117, T118, T119) can run in parallel
- All optimization tasks (T120, T121, T122) can run in parallel
- All security tasks (T123, T124, T125) can run in parallel
- All monitoring tasks (T126, T127, T128) can run in parallel
- All quality tasks (T129, T130, T131) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (write tests first, ensure they fail):
Task T026: "Unit test for R2 signed URL generation in backend/tests/unit/test_r2_client.py"
Task T027: "Integration test for GET /api/content/chapters/{id} in backend/tests/integration/test_api_content.py"
Task T028: "Integration test for content delivery error cases in backend/tests/integration/test_api_content.py"

# Then implement in parallel:
Task T029: "Create ChapterEmbedding model in backend/api/models/chapter.py"
Task T030: "Create Pydantic schemas in backend/api/schemas/content.py"

# Sequential after above:
Task T031: "Implement content service in backend/services/content_service.py" (uses T029, T030)
Task T032: "Implement content delivery routes in backend/api/routes/content.py" (uses T031)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Goal**: Fastest path to working demo

1. Complete Phase 1: Setup (5 tasks)
2. Complete Phase 2: Foundational (20 tasks) - **CRITICAL**
3. Complete Phase 3: User Story 1 (14 tasks)
4. Complete Phase 9 (partial): ChatGPT App Setup for Content Delivery (5 tasks)
5. **STOP and VALIDATE**: Demo content delivery feature
6. **Total**: 44 tasks for MVP

**Deliverable**: Students can view course chapters via ChatGPT with explanations

### Incremental Delivery (Add Features One by One)

**Goal**: Build confidence, validate each feature independently

1. Foundation (Phases 1-2) → Test database, auth, R2 working
2. Add US1 (Content Delivery) → Test independently → Demo
3. Add US2 (Navigation) → Test independently → Demo
4. Add US3 (Grounded Q&A) → Test independently → Demo
5. Add US4 (Quizzes) → Test independently → Demo
6. Add US5 (Progress) → Test independently → Demo
7. Add US6 (Freemium) → Test independently → Demo
8. Add ChatGPT App → Test E2E → Final demo
9. Polish → Production ready

Each increment adds value without breaking previous features.

### Parallel Team Strategy (3 Developers)

**Week 1**: Foundation (all together)
- Setup + Foundational phases
- Checkpoint: Auth working, database schema created, R2 configured

**Week 2**: Core Features (parallel)
- Dev A: US1 (Content Delivery) + US3 (Grounded Q&A)
- Dev B: US2 (Navigation) + US5 (Progress Tracking)
- Dev C: US4 (Rule-Based Quizzes) + US6 (Freemium Gate)

**Week 3**: Integration (all together)
- ChatGPT App frontend
- E2E testing
- Polish & optimization

---

## Task Summary

**Total Tasks**: 135

**Breakdown by Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 20 tasks
- Phase 3 (US1 - Content Delivery): 14 tasks
- Phase 4 (US2 - Navigation): 11 tasks
- Phase 5 (US3 - Grounded Q&A): 12 tasks
- Phase 6 (US4 - Rule-Based Quizzes): 17 tasks
- Phase 7 (US5 - Progress Tracking): 14 tasks
- Phase 8 (US6 - Freemium Gate): 7 tasks
- Phase 9 (ChatGPT App Frontend): 13 tasks
- Phase 10 (Polish): 22 tasks

**Parallel Opportunities**: 58 tasks marked [P] (43% of total)

**Independent Test Criteria**:
- US1: Request chapter, verify signed URL, fetch content
- US2: Navigate chapters, verify sequencing and structure
- US3: Search content, verify relevant results returned
- US4: Take quiz, verify rule-based grading accurate
- US5: Complete activities, verify streak and progress calculated correctly
- US6: Test tier limits, verify free users gated at Chapter 4, premium users granted access

**MVP Scope**: Phases 1-3 + partial Phase 9 = 44 tasks (Content Delivery only)

---

## Notes

- **[P] tasks**: Different files, no dependencies - can be parallelized
- **[Story] labels**: Map tasks to user stories for traceability
- **Test-First Approach**: All test tasks should be written and verified to FAIL before implementation tasks
- **Constitutional Compliance**: T005 and T132 verify zero backend LLM calls
- **Cost Target**: T133 validates actual costs under $16-41 budget
- **Independent Stories**: Each user story (US1-US6) can be tested independently per acceptance scenarios in spec.md
- **Checkpoint Validation**: After each phase, stop and verify that phase's deliverable works before proceeding
- **Avoid**: Tasks that modify the same files simultaneously (not marked [P])
- **Commit Strategy**: Commit after completing each task or logical task group (e.g., all models for a user story)
