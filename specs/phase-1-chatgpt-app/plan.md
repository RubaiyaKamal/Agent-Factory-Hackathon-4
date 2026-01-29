# Implementation Plan: Phase 1 ChatGPT App (Zero-Backend-LLM)

**Branch**: `phase-1-chatgpt-app` | **Date**: 2026-01-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/phase-1-chatgpt-app/spec.md`

---

## Summary

Build Course Companion FTE Phase 1 with strict Zero-Backend-LLM architecture: a ChatGPT App frontend paired with a deterministic FastAPI backend implementing all 6 required features (Content Delivery, Navigation, Grounded Q&A, Rule-Based Quizzes, Progress Tracking, Freemium Gate) with NO backend LLM inference, serving 10,000 users at $0.002-$0.004 per user cost target.

**Technical Approach**:
- ChatGPT App handles ALL intelligent reasoning via OpenAI Apps SDK
- Backend serves as pure data/computation layer (content retrieval, rule-based grading, calculations)
- Cloudflare R2 for content storage with signed URLs
- Neon PostgreSQL for relational data (users, progress, quizzes)
- Pre-computed embeddings for semantic search (no runtime LLM)

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.109, Pydantic 2.5, SQLModel 0.0.14, Boto3 (R2), OpenAI Apps SDK (frontend)
**Storage**: Cloudflare R2 (content), Neon PostgreSQL (user data)
**Testing**: pytest, pytest-asyncio, httpx-mock, faker
**Target Platform**: Linux server (Fly.io/Railway), ChatGPT App platform
**Project Type**: Web (backend API + ChatGPT App frontend)
**Performance Goals**: <500ms p95 API response, 100 concurrent users per instance, 99.9% uptime
**Constraints**: ZERO backend LLM calls (constitutional), <$50/month for 10K users, <200ms p95 for content delivery
**Scale/Scope**: 10,000 users (Phase 1), 20 chapters per course, 100 quiz questions, 4 agent skills

---

## Constitution Check

### ✅ Compliance Verification

**I. Zero-Backend-LLM Architecture (Default)** - PASS
- ✅ Backend contains NO LLM API calls (verified in `backend/main.py` startup check)
- ✅ Backend is purely deterministic (content retrieval, rule-based grading, calculations)
- ✅ ChatGPT handles ALL explanation, tutoring, adaptation
- ✅ Runtime enforcement enabled (`ENFORCE_ZERO_BACKEND_LLM=true`)

**II. Phase-Based Development Progression** - PASS
- ✅ Phase 1 requirements only (no Phase 2/3 features)
- ✅ All 6 required features specified
- ✅ Clear validation criteria (code audit for zero LLM calls)

**III. Agent Factory 8-Layer Architecture** - PASS
- ✅ L3 (FastAPI) - HTTP interface implemented
- ✅ L6 (Skills + MCP) - 4 agent skills defined
- ⚠️ L0-L2, L4-L5, L7 deferred to Phase 2 (as per constitution)

**IV. Spec-Driven Development (SDD)** - PASS
- ✅ Spec created (spec.md)
- ✅ Plan in progress (this file)
- ⏳ Tasks pending (tasks.md - next step)
- ✅ PHR routing configured

**V. Cost Efficiency & Scalability** - PASS
- ✅ Cost target: $0.002-$0.004 per user (infrastructure only)
- ✅ Sub-linear scaling via deterministic backend
- ✅ Cloudflare R2 for cost-effective storage

**VI. Educational Quality Standards** - PASS
- ✅ 6 required features specified
- ✅ 4 agent skills defined (concept-explainer, quiz-master, socratic-tutor, progress-motivator)
- ✅ 99%+ consistency via deterministic backend

**VII. Security & Compliance** - PASS
- ✅ JWT authentication specified
- ✅ User data isolation in database schema
- ✅ No hardcoded secrets (.env.example provided)
- ✅ HTTPS required (R2 signed URLs)

### Complexity Tracking

No constitutional violations. All architectural decisions align with Zero-Backend-LLM mandate.

---

## Project Structure

### Documentation (this feature)

```text
specs/phase-1-chatgpt-app/
├── spec.md                  # ✅ Requirements and user stories
├── plan.md                  # ✅ This file - architecture and design
└── tasks.md                 # ⏳ Implementation tasks (next step)
```

### Source Code (repository root)

```text
backend/                          # FastAPI backend (deterministic only)
├── api/
│   ├── routes/
│   │   ├── auth.py              # JWT authentication endpoints
│   │   ├── content.py           # Content delivery from R2
│   │   ├── navigation.py        # Chapter sequencing logic
│   │   ├── quizzes.py           # Rule-based quiz grading
│   │   ├── progress.py          # Progress tracking and streaks
│   │   └── search.py            # Keyword + semantic search
│   ├── models/                  # SQLModel database models
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── chapter.py
│   │   ├── quiz.py
│   │   ├── progress.py
│   │   └── achievement.py
│   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── auth.py
│   │   ├── content.py
│   │   ├── quiz.py
│   │   └── progress.py
│   └── middleware/
│       ├── auth.py              # JWT verification middleware
│       ├── rate_limit.py        # Tier-based rate limiting
│       └── cors.py              # CORS configuration
├── core/
│   ├── config.py                # ✅ Settings management (Pydantic)
│   ├── constants.py             # ✅ Application constants
│   ├── security.py              # Password hashing, JWT utils
│   └── exceptions.py            # Custom exception classes
├── db/
│   ├── session.py               # Database connection management
│   ├── base.py                  # SQLModel base classes
│   └── migrations/              # Alembic migrations
│       └── versions/
├── services/
│   ├── r2.py                    # Cloudflare R2 client
│   ├── search.py                # Search service (keyword + semantic)
│   ├── quiz_grader.py           # Rule-based grading logic
│   ├── progress_calculator.py  # Streak and completion calculations
│   └── embeddings.py            # Offline embedding generation
├── tests/
│   ├── unit/                    # Unit tests (>80% coverage)
│   │   ├── test_quiz_grader.py
│   │   ├── test_progress.py
│   │   └── test_search.py
│   ├── integration/             # Integration tests
│   │   ├── test_api_content.py
│   │   ├── test_api_quizzes.py
│   │   └── test_api_progress.py
│   └── conftest.py              # Pytest fixtures
└── main.py                      # ✅ FastAPI app entry point

chatgpt-app/                     # ChatGPT App frontend
├── src/
│   ├── app.yaml                 # OpenAI Apps SDK manifest
│   ├── skills/                  # Agent skill references
│   │   ├── concept-explainer.md
│   │   ├── quiz-master.md
│   │   ├── socratic-tutor.md
│   │   └── progress-motivator.md
│   └── actions/                 # Custom actions (if needed)
├── config/
│   └── backend.json             # Backend API configuration
└── tests/
    └── test_integration.py      # End-to-end app tests

content/                         # Course content (uploaded to R2)
├── courses/
│   └── ai-agent-development/    # Example course (TBD: choose topic)
│       ├── chapter-01.md
│       ├── chapter-02.md
│       └── ...
├── quizzes/
│   └── ai-agent-development/
│       ├── quiz-01.json
│       ├── quiz-02.json
│       └── ...
└── assets/
    └── images/

.claude/skills/                  # ✅ Agent runtime skills
├── concept-explainer/
│   ├── SKILL.md
│   └── REFERENCE.md
├── quiz-master/
│   ├── SKILL.md
│   └── REFERENCE.md
├── socratic-tutor/
│   ├── SKILL.md
│   └── REFERENCE.md
└── progress-motivator/
    ├── SKILL.md
    └── REFERENCE.md
```

**Structure Decision**: Web application architecture with clear backend/frontend separation. Backend follows layered architecture (routes → services → database). ChatGPT App references backend via REST API. All agent intelligence resides in ChatGPT (via skills), ensuring constitutional compliance.

---

## Architecture Decisions

### AD-001: Zero-Backend-LLM Enforcement Strategy

**Decision**: Implement multi-layer enforcement to prevent accidental LLM usage in Phase 1.

**Layers:**
1. **Startup Check** (`backend/main.py:_verify_zero_llm_compliance()`):
   - Scans `sys.modules` for forbidden imports (`anthropic`, `openai`, `langchain`)
   - Raises `RuntimeError` if violations detected
   - Logs compliance verification result

2. **Configuration Validation** (`backend/core/config.py:_validate_phase_1_compliance()`):
   - Checks for LLM API keys in environment
   - Blocks if `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` are set (when `ENFORCE_ZERO_BACKEND_LLM=true`)
   - Prevents accidental Phase 2 configuration

3. **Dependency Management** (`requirements.txt`):
   - LLM libraries commented out with warnings
   - Documentation explains Phase 2-only usage

4. **Code Review Checklist**:
   - Manual verification before merge
   - Automated grep for forbidden patterns in CI/CD (future)

**Rationale**: Multiple enforcement layers prevent both intentional and accidental violations. Startup check catches runtime issues. Config validation prevents environment mistakes.

**Tradeoff**: Slight startup overhead (~10ms) for module scanning. Acceptable given criticality of compliance.

---

### AD-002: Semantic Search Without LLM

**Decision**: Use pre-computed embeddings with offline model for semantic search, avoiding runtime LLM calls.

**Implementation**:
```python
# backend/services/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once at startup (cached)
model = SentenceTransformer('all-MiniLM-L6-v2')  # 80MB, offline

# Pre-compute embeddings for all course content
def generate_content_embeddings(content: str) -> np.ndarray:
    """Generate embeddings locally (no API call)."""
    return model.encode(content)

# Runtime search (no LLM)
def semantic_search(query: str, content_embeddings: List[np.ndarray]) -> List[int]:
    """Find similar content using cosine similarity."""
    query_embedding = model.encode(query)
    similarities = cosine_similarity(query_embedding, content_embeddings)
    return np.argsort(similarities)[::-1][:5]  # Top 5 results
```

**Storage**:
- Pre-computed embeddings stored in PostgreSQL (`chapter_embeddings` table)
- Generated during content upload (one-time cost)
- Updated only when content changes

**Performance**:
- Query encoding: ~20ms (CPU)
- Cosine similarity: ~5ms for 1000 chapters
- Total: <50ms for semantic search

**Rationale**: `sentence-transformers` runs locally without API calls. Embeddings are deterministic and cached. Meets constitutional requirement while providing intelligent search.

**Alternative Rejected**: Cloud embedding APIs (OpenAI, Cohere) - violates Zero-Backend-LLM.

---

### AD-003: Rule-Based Quiz Grading Strategy

**Decision**: Implement deterministic grading using exact matching and regex patterns, no LLM evaluation.

**Grading Rules** (`backend/services/quiz_grader.py`):

```python
from typing import List, Pattern
import re

class QuizGrader:
    """Deterministic quiz grading (Zero-LLM compliant)."""

    def grade_multiple_choice(
        self, user_answer: str, correct_answer: str
    ) -> bool:
        """Exact match (case-insensitive)."""
        return user_answer.strip().upper() == correct_answer.strip().upper()

    def grade_true_false(
        self, user_answer: str, correct_answer: str
    ) -> bool:
        """Normalize and match boolean values."""
        true_values = ['true', 't', 'yes', 'y', '1']
        false_values = ['false', 'f', 'no', 'n', '0']

        user = user_answer.strip().lower()
        correct = correct_answer.strip().lower()

        if correct == 'true':
            return user in true_values
        else:
            return user in false_values

    def grade_fill_in_blank(
        self, user_answer: str, correct_answers: List[str], pattern: Pattern = None
    ) -> bool:
        """
        Accept multiple correct answers or regex pattern.

        Examples:
        - correct_answers: ["GET", "get"] → case variations
        - pattern: r"^(GET|POST|PUT|DELETE)$" → any HTTP method
        """
        user = user_answer.strip()

        # Try exact matches first (case-insensitive)
        for correct in correct_answers:
            if user.lower() == correct.lower():
                return True

        # Try regex pattern if provided
        if pattern and re.match(pattern, user, re.IGNORECASE):
            return True

        return False
```

**Question Schema** (database):
```python
class Question(SQLModel, table=True):
    id: int = Field(primary_key=True)
    question_text: str
    question_type: str  # "multiple_choice" | "true_false" | "fill_in_blank"
    correct_answer: str  # Single answer for MC/TF
    correct_answers: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))  # Multiple for fill-in
    answer_pattern: Optional[str] = None  # Regex pattern (optional)
    options: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))  # For MC
```

**Rationale**: Rule-based grading is deterministic, testable, and fast (<1ms per question). Covers 99% of quiz use cases without LLM. Regex patterns handle flexibility (e.g., accepting "Python 3.11" or "3.11" or "Python 3").

**Limitation**: Cannot grade free-form essay questions. Deferred to Phase 2 (LLM-graded assessments as premium feature).

---

### AD-004: Content Delivery via Cloudflare R2

**Decision**: Store all course content in Cloudflare R2, serve via signed URLs with client-side caching.

**Architecture**:
```
User → ChatGPT App → Backend API → R2 (signed URL) → User
                                  ↓
                              Database (metadata)
```

**Flow**:
1. ChatGPT asks backend: `GET /api/content/chapters/3`
2. Backend queries database for chapter metadata (title, R2 key)
3. Backend generates signed URL (1-hour expiration): `https://<bucket>.r2.cloudflarestorage.com/chapters/3.md?signature=...`
4. Backend returns: `{ "id": 3, "title": "...", "content_url": "...", "expires_at": "..." }`
5. ChatGPT fetches content from signed URL
6. ChatGPT explains content to user

**R2 Client** (`backend/services/r2.py`):
```python
import boto3
from botocore.config import Config
from backend.core.config import settings

class R2Client:
    """Cloudflare R2 client (S3-compatible)."""

    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4', region_name=settings.R2_REGION)
        )
        self.bucket = settings.R2_BUCKET_NAME

    def generate_signed_url(self, key: str, expiry: int = 3600) -> str:
        """Generate pre-signed URL for reading object."""
        return self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': key},
            ExpiresIn=expiry
        )

    async def upload_content(self, key: str, content: bytes, content_type: str) -> None:
        """Upload content to R2 (admin function)."""
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ContentType=content_type
        )
```

**Cost Analysis**:
- Storage: $0.015/GB/month (20 chapters × 50KB = 1MB ~ $0.000015/month)
- Class A operations (upload): $4.50/million (20 chapters = $0.00009)
- Class B operations (read): $0.36/million (10K users × 20 chapters = 200K reads = $0.072/month)
- Bandwidth (egress): $0 (first 10GB free, then $0.09/GB)

**Total R2 Cost (10K users)**: ~$0.10/month

**Rationale**: R2 is 10x cheaper than AWS S3 for storage + egress. Signed URLs prevent unauthorized access. Client-side caching reduces API calls.

**Alternative Rejected**: Database BLOB storage - expensive, slow, not scalable.

---

### AD-005: Progress Tracking and Streak Calculation

**Decision**: Calculate streaks server-side using UTC timestamps with user timezone for display.

**Database Schema**:
```python
class Progress(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    chapter_id: int = Field(foreign_key="chapters.id")
    completed: bool = Field(default=False)
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserActivity(SQLModel, table=True):
    """Track daily activity for streak calculation."""
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    activity_date: date  # User's local date
    activity_count: int = Field(default=1)  # Number of activities that day
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        indexes = [("user_id", "activity_date")]  # Composite index for fast lookup
```

**Streak Calculation** (`backend/services/progress_calculator.py`):
```python
from datetime import date, timedelta
from typing import List

def calculate_streak(user_id: int, activity_dates: List[date]) -> int:
    """
    Calculate consecutive day streak.

    Algorithm:
    1. Sort dates descending (most recent first)
    2. Start from today (or most recent activity)
    3. Count consecutive days going backward
    4. Break on first gap > grace period (24 hours)
    """
    if not activity_dates:
        return 0

    sorted_dates = sorted(activity_dates, reverse=True)
    today = sorted_dates[0]
    streak = 1

    for i in range(1, len(sorted_dates)):
        expected_date = today - timedelta(days=i)
        if sorted_dates[i] == expected_date:
            streak += 1
        else:
            break  # Gap detected

    return streak

def update_user_activity(user_id: int, user_timezone: str = "UTC") -> None:
    """
    Record activity for today (user's timezone).
    Upserts into UserActivity table.
    """
    from zoneinfo import ZoneInfo

    user_tz = ZoneInfo(user_timezone)
    user_today = datetime.now(user_tz).date()

    # Upsert activity
    db.execute(
        """
        INSERT INTO user_activity (user_id, activity_date, activity_count)
        VALUES (:user_id, :date, 1)
        ON CONFLICT (user_id, activity_date) DO UPDATE
        SET activity_count = user_activity.activity_count + 1
        """,
        {"user_id": user_id, "date": user_today}
    )
```

**Grace Period**:
- User has 24 hours (in their timezone) to maintain streak
- Example: If user studied at 11 PM on Monday, they have until 11:59 PM Tuesday to maintain streak

**Performance**:
- Query user activities: ~5ms (indexed on user_id + date)
- Calculate streak: O(n) where n = streak length (typically <100 days)
- Total: <10ms

**Rationale**: Server-side calculation ensures consistency. Timezone handling prevents unfair streak breaks due to UTC midnight. Efficient with proper indexing.

---

### AD-006: Freemium Access Control

**Decision**: Implement tier-based access control using middleware and database flags.

**User Tier Schema**:
```python
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    tier: str = Field(default="free")  # "free" | "premium" | "pro" | "team"
    tier_expires_at: Optional[datetime] = None  # For subscription tracking
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AccessRule(SQLModel, table=True):
    """Define what each tier can access."""
    id: int = Field(primary_key=True)
    resource_type: str  # "chapter" | "quiz" | "feature"
    resource_id: Optional[int] = None  # Specific chapter/quiz ID (null = all)
    min_tier: str  # Minimum tier required ("free", "premium", "pro", "team")
```

**Access Check Middleware** (`backend/api/middleware/access.py`):
```python
from fastapi import HTTPException, status, Depends
from backend.api.models.user import User
from backend.core.constants import UserTier, ErrorMessages

async def check_chapter_access(
    chapter_id: int,
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Verify user has access to requested chapter.

    Free tier: Chapters 1-3 only
    Premium+: All chapters
    """
    if current_user.tier == UserTier.FREE and chapter_id > 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status": "error",
                "message": ErrorMessages.TIER_LIMIT_REACHED,
                "upgrade_url": "/api/upgrade",
                "upgrade_tiers": ["premium", "pro", "team"]
            }
        )

async def check_quiz_access(
    quiz_id: int,
    current_user: User = Depends(get_current_user)
) -> None:
    """Verify user has access to quiz."""
    # Free tier: 3 quizzes only
    if current_user.tier == UserTier.FREE:
        completed_quizzes = await get_user_quiz_count(current_user.id)
        if completed_quizzes >= 3:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "status": "error",
                    "message": ErrorMessages.TIER_LIMIT_REACHED,
                    "upgrade_url": "/api/upgrade"
                }
            )
```

**Route Integration**:
```python
@router.get("/chapters/{chapter_id}")
async def get_chapter(
    chapter_id: int,
    current_user: User = Depends(get_current_user),
    _: None = Depends(check_chapter_access)  # Access check
):
    """Get chapter content (tier-gated)."""
    # Access verified, proceed with logic
    ...
```

**ChatGPT Response Handling**:
- Backend returns 403 with upgrade messaging
- ChatGPT receives error and gracefully explains:
  ```
  "I'd love to help you with Chapter 4, but it's part of our premium content!

  Here's what premium unlocks:
  - All 20 chapters (you've completed the 3 free chapters!)
  - Unlimited quizzes
  - Full progress tracking

  Premium is just $9.99/month. Want to learn more about upgrading?"
  ```

**Rationale**: Middleware keeps access logic centralized and testable. Database-driven rules allow dynamic tier configuration. Graceful error responses maintain user experience.

---

## API Design

### API Architecture

**Base URL**: `https://api.course-companion.app` (production)
**Protocol**: HTTPS only
**Format**: JSON (request and response)
**Authentication**: JWT Bearer tokens
**Versioning**: URI versioning (`/api/v1/...`) - currently v1

### Authentication Flow

```
1. Registration:  POST /api/auth/register → { access_token, refresh_token }
2. Login:         POST /api/auth/login → { access_token, refresh_token }
3. Refresh:       POST /api/auth/refresh → { access_token }
4. Authenticated: Headers: { "Authorization": "Bearer <access_token>" }
```

**Token Expiration**:
- Access token: 60 minutes
- Refresh token: 30 days

### API Endpoints

#### 1. Authentication (`/api/auth`)

**POST /api/auth/register**
```yaml
Summary: Register new user
Request:
  email: string (email format)
  password: string (min 8 chars)
  timezone: string (optional, default UTC)
Response: 201
  access_token: string (JWT)
  refresh_token: string (JWT)
  user: { id, email, tier, created_at }
Errors:
  400: Invalid email/password
  409: Email already registered
```

**POST /api/auth/login**
```yaml
Summary: Authenticate user
Request:
  email: string
  password: string
Response: 200
  access_token: string
  refresh_token: string
  user: { id, email, tier }
Errors:
  401: Invalid credentials
  429: Too many login attempts
```

---

#### 2. Content Delivery (`/api/content`)

**GET /api/content/courses**
```yaml
Summary: List available courses
Auth: Required
Response: 200
  courses: [
    { id, title, description, total_chapters, difficulty }
  ]
```

**GET /api/content/chapters/{chapter_id}**
```yaml
Summary: Get chapter content
Auth: Required
Tier Gate: Free (chapters 1-3), Premium+ (all)
Response: 200
  id: integer
  chapter_number: integer
  title: string
  course_id: integer
  content_url: string (R2 signed URL, 1hr expiry)
  estimated_duration: integer (minutes)
  next_chapter_id: integer | null
  previous_chapter_id: integer | null
  expires_at: string (ISO datetime)
Errors:
  403: Tier limit reached
  404: Chapter not found
```

**GET /api/content/chapters/{chapter_id}/content**
```yaml
Summary: Get chapter content directly (alternative to signed URL)
Auth: Required
Tier Gate: Same as above
Response: 200
  content: string (markdown)
  format: "markdown"
Errors: Same as above
```

---

#### 3. Navigation (`/api/navigation`)

**GET /api/navigation/courses/{course_id}/structure**
```yaml
Summary: Get complete course structure
Auth: Required
Response: 200
  course: { id, title, total_chapters }
  chapters: [
    {
      id, chapter_number, title,
      completed: boolean,
      locked: boolean (based on user tier)
    }
  ]
  completion_percentage: integer
  current_chapter: integer | null
```

**GET /api/navigation/chapters/{chapter_id}/next**
```yaml
Summary: Get next chapter in sequence
Auth: Required
Response: 200
  next_chapter: { id, title, chapter_number } | null
  is_locked: boolean
  unlock_tier: string | null
```

---

#### 4. Search (`/api/search`)

**GET /api/search?q={query}&type={type}&limit={limit}**
```yaml
Summary: Search course content
Auth: Required
Parameters:
  q: string (min 3 chars)
  type: "keyword" | "semantic" (default: "keyword")
  limit: integer (default: 20, max: 50)
Response: 200
  results: [
    {
      chapter_id: integer,
      chapter_title: string,
      excerpt: string,
      relevance_score: float,
      match_type: "title" | "content"
    }
  ]
  total: integer
  query: string
Errors:
  400: Query too short
  429: Rate limit exceeded
```

---

#### 5. Quizzes (`/api/quizzes`)

**GET /api/quizzes/chapters/{chapter_id}/quiz**
```yaml
Summary: Get quiz for chapter
Auth: Required
Tier Gate: Free (3 quizzes max), Premium+ (unlimited)
Response: 200
  quiz_id: integer
  chapter_id: integer
  questions: [
    {
      question_id: integer,
      question_text: string,
      question_type: "multiple_choice" | "true_false" | "fill_in_blank",
      options: string[] | null (for multiple_choice),
      difficulty: "easy" | "medium" | "hard"
    }
  ]
  total_questions: integer
  passing_score: integer (percentage)
Errors:
  403: Quiz limit reached (free tier)
  404: Quiz not found
```

**POST /api/quizzes/{quiz_id}/submit**
```yaml
Summary: Submit quiz answers (rule-based grading)
Auth: Required
Request:
  answers: [
    { question_id: integer, user_answer: string }
  ]
Response: 200
  quiz_id: integer
  score: integer (percentage)
  total_questions: integer
  correct_answers: integer
  passed: boolean
  results: [
    {
      question_id: integer,
      correct: boolean,
      user_answer: string,
      correct_answer: string,
      explanation: string (from database)
    }
  ]
  attempt_number: integer
Errors:
  400: Invalid answers format
  404: Quiz not found
  422: Max attempts exceeded
```

**GET /api/quizzes/{quiz_id}/attempts**
```yaml
Summary: Get user's quiz attempt history
Auth: Required
Response: 200
  attempts: [
    {
      attempt_id: integer,
      score: integer,
      passed: boolean,
      attempted_at: string (ISO datetime)
    }
  ]
  total_attempts: integer
  best_score: integer
  average_score: float
```

---

#### 6. Progress Tracking (`/api/progress`)

**GET /api/progress/me**
```yaml
Summary: Get current user's progress summary
Auth: Required
Response: 200
  user_id: integer
  course_completion_percentage: integer
  chapters_completed: integer
  total_chapters: integer
  current_chapter: integer | null
  streak_days: integer
  last_activity: string (ISO datetime)
  quizzes_taken: integer
  quizzes_passed: integer
  average_quiz_score: integer
  total_study_time_minutes: integer (estimated)
  achievements: string[] (achievement IDs)
```

**POST /api/progress/chapters/{chapter_id}/complete**
```yaml
Summary: Mark chapter as completed
Auth: Required
Response: 200
  chapter_id: integer
  completed: boolean
  completed_at: string (ISO datetime)
  new_completion_percentage: integer
  streak_updated: boolean
  new_streak: integer
  achievements_earned: string[] (newly unlocked achievements)
```

**GET /api/progress/streak**
```yaml
Summary: Get detailed streak information
Auth: Required
Response: 200
  current_streak: integer
  longest_streak: integer
  last_activity_date: string (ISO date)
  streak_status: "active" | "broken"
  next_deadline: string (ISO datetime, for maintaining streak)
```

---

#### 7. Health & Monitoring (`/health`)

**GET /health**
```yaml
Summary: Health check (no auth required)
Response: 200
  status: "healthy" | "degraded" | "unhealthy"
  checks: {
    database: "ok" | "error",
    storage: "ok" | "error",
    cache: "ok" | "error"
  }
  version: string
  uptime: string
```

---

### Error Response Format (Standard)

```json
{
  "status": "error",
  "message": "Human-readable error message",
  "detail": {
    "field": "Specific field error (if applicable)"
  },
  "code": "ERROR_CODE",
  "request_id": "uuid"
}
```

**HTTP Status Codes Used**:
- 200: Success
- 201: Created
- 204: No Content (e.g., DELETE operations)
- 400: Bad Request (validation errors)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (tier limit, permissions)
- 404: Not Found
- 409: Conflict (e.g., duplicate email)
- 422: Unprocessable Entity (business logic errors)
- 429: Too Many Requests (rate limit)
- 500: Internal Server Error

---

## Database Schema

### Entity-Relationship Diagram (ERD)

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    User      │────────<│   Progress   │>────────│   Chapter    │
│──────────────│         │──────────────│         │──────────────│
│ id (PK)      │         │ id (PK)      │         │ id (PK)      │
│ email (UQ)   │         │ user_id (FK) │         │ course_id(FK)│
│ hashed_pwd   │         │ chapter_id(FK│         │ chapter_num  │
│ tier         │         │ completed    │         │ title        │
│ tier_expires │         │ completed_at │         │ content_key  │
│ timezone     │         │ created_at   │         │ duration_est │
│ created_at   │         │ updated_at   │         │ created_at   │
└──────────────┘         └──────────────┘         └──────────────┘
       │                                                  │
       │                                                  │
       │                 ┌──────────────┐                │
       │                 │   Course     │<───────────────┘
       │                 │──────────────│
       │                 │ id (PK)      │
       │                 │ title        │
       │                 │ description  │
       │                 │ difficulty   │
       │                 │ total_chapts │
       │                 │ created_at   │
       │                 └──────────────┘
       │                        │
       │                        │
       │                 ┌──────────────┐
       └───────────────><│  Quiz        │
                         │──────────────│
                         │ id (PK)      │
                         │ chapter_id(FK│
                         │ passing_score│
                         │ created_at   │
                         └──────────────┘
                                │
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
       ┌──────────────┐  ┌──────────────┐ ┌──────────────┐
       │  Question    │  │ QuizAttempt  │ │UserActivity  │
       │──────────────│  │──────────────│ │──────────────│
       │ id (PK)      │  │ id (PK)      │ │ id (PK)      │
       │ quiz_id (FK) │  │ user_id (FK) │ │ user_id (FK) │
       │ question_text│  │ quiz_id (FK) │ │ activity_date│
       │ type         │  │ score        │ │ activity_cnt │
       │ correct_ans  │  │ answers(JSON)│ │ created_at   │
       │ options(JSON)│  │ attempted_at │ └──────────────┘
       │ explanation  │  │ passed       │
       │ difficulty   │  └──────────────┘
       └──────────────┘
```

### Table Definitions (SQLModel)

#### **users**
```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    tier: str = Field(default="free", max_length=20)  # free|premium|pro|team
    tier_expires_at: datetime | None = None
    timezone: str = Field(default="UTC", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships (using SQLModel)
    progress: list["Progress"] = Relationship(back_populates="user")
    quiz_attempts: list["QuizAttempt"] = Relationship(back_populates="user")
    activities: list["UserActivity"] = Relationship(back_populates="user")
```

#### **courses**
```python
class Course(SQLModel, table=True):
    __tablename__ = "courses"

    id: int = Field(primary_key=True)
    title: str = Field(max_length=255)
    description: str = Field(max_length=1000)
    difficulty: str = Field(max_length=20)  # beginner|intermediate|advanced
    total_chapters: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    chapters: list["Chapter"] = Relationship(back_populates="course")
```

#### **chapters**
```python
class Chapter(SQLModel, table=True):
    __tablename__ = "chapters"

    id: int = Field(primary_key=True)
    course_id: int = Field(foreign_key="courses.id", index=True)
    chapter_number: int
    title: str = Field(max_length=255)
    content_key: str = Field(max_length=500)  # R2 object key
    estimated_duration: int  # Minutes
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    course: Course = Relationship(back_populates="chapters")
    progress: list["Progress"] = Relationship(back_populates="chapter")
    quiz: "Quiz | None" = Relationship(back_populates="chapter")

    # Composite index for fast lookup
    class Config:
        indexes = [("course_id", "chapter_number")]
```

#### **progress**
```python
class Progress(SQLModel, table=True):
    __tablename__ = "progress"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    chapter_id: int = Field(foreign_key="chapters.id", index=True)
    completed: bool = Field(default=False)
    completed_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="progress")
    chapter: Chapter = Relationship(back_populates="progress")

    # Unique constraint: one progress record per user per chapter
    class Config:
        indexes = [("user_id", "chapter_id")]
        # Unique constraint in Alembic migration
```

#### **quizzes**
```python
class Quiz(SQLModel, table=True):
    __tablename__ = "quizzes"

    id: int = Field(primary_key=True)
    chapter_id: int = Field(foreign_key="chapters.id", unique=True, index=True)
    passing_score: int = Field(default=70)  # Percentage
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    chapter: Chapter = Relationship(back_populates="quiz")
    questions: list["Question"] = Relationship(back_populates="quiz")
    attempts: list["QuizAttempt"] = Relationship(back_populates="quiz")
```

#### **questions**
```python
from sqlalchemy import Column, JSON

class Question(SQLModel, table=True):
    __tablename__ = "questions"

    id: int = Field(primary_key=True)
    quiz_id: int = Field(foreign_key="quizzes.id", index=True)
    question_text: str = Field(max_length=1000)
    question_type: str = Field(max_length=50)  # multiple_choice|true_false|fill_in_blank
    correct_answer: str = Field(max_length=500)  # Single answer (MC, TF)
    correct_answers: list[str] | None = Field(default=None, sa_column=Column(JSON))  # Multiple (fill-in)
    answer_pattern: str | None = Field(default=None, max_length=500)  # Regex pattern
    options: list[str] | None = Field(default=None, sa_column=Column(JSON))  # For MC
    explanation: str = Field(max_length=1000)  # Why answer is correct
    difficulty: str = Field(max_length=20)  # easy|medium|hard
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    quiz: Quiz = Relationship(back_populates="questions")
```

#### **quiz_attempts**
```python
class QuizAttempt(SQLModel, table=True):
    __tablename__ = "quiz_attempts"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    quiz_id: int = Field(foreign_key="quizzes.id", index=True)
    score: int  # Percentage
    answers: dict = Field(sa_column=Column(JSON))  # { question_id: user_answer }
    passed: bool
    attempted_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="quiz_attempts")
    quiz: Quiz = Relationship(back_populates="attempts")

    # Index for user's quiz history
    class Config:
        indexes = [("user_id", "quiz_id", "attempted_at")]
```

#### **user_activity** (for streak calculation)
```python
from datetime import date

class UserActivity(SQLModel, table=True):
    __tablename__ = "user_activity"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    activity_date: date  # User's local date (converted from timezone)
    activity_count: int = Field(default=1)  # Number of activities that day
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="activities")

    # Composite unique constraint + index
    class Config:
        indexes = [("user_id", "activity_date")]
        # UNIQUE constraint in Alembic migration
```

#### **chapter_embeddings** (for semantic search)
```python
from sqlalchemy import Column, ARRAY, Float

class ChapterEmbedding(SQLModel, table=True):
    __tablename__ = "chapter_embeddings"

    id: int = Field(primary_key=True)
    chapter_id: int = Field(foreign_key="chapters.id", unique=True, index=True)
    embedding: list[float] = Field(sa_column=Column(ARRAY(Float)))  # 384-dim vector
    model_version: str = Field(max_length=100)  # "all-MiniLM-L6-v2"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Note: PostgreSQL supports vector operations via pgvector extension (optional)
```

### Database Migrations (Alembic)

**Initial Migration** (`alembic/versions/001_initial_schema.py`):
```python
"""Initial schema

Revision ID: 001
Create Date: 2026-01-21
"""

def upgrade():
    # Create tables in dependency order
    op.create_table('users', ...)
    op.create_table('courses', ...)
    op.create_table('chapters', ...)
    op.create_table('progress', ...)
    op.create_table('quizzes', ...)
    op.create_table('questions', ...)
    op.create_table('quiz_attempts', ...)
    op.create_table('user_activity', ...)
    op.create_table('chapter_embeddings', ...)

    # Create indexes
    op.create_index('idx_progress_user_chapter', 'progress', ['user_id', 'chapter_id'], unique=True)
    op.create_index('idx_activity_user_date', 'user_activity', ['user_id', 'activity_date'], unique=True)

def downgrade():
    # Drop in reverse order
    op.drop_table('chapter_embeddings')
    op.drop_table('user_activity')
    op.drop_table('quiz_attempts')
    op.drop_table('questions')
    op.drop_table('quizzes')
    op.drop_table('progress')
    op.drop_table('chapters')
    op.drop_table('courses')
    op.drop_table('users')
```

---

## Testing Strategy

### Test Coverage Requirements

- **Unit Tests**: >80% code coverage
- **Integration Tests**: All API endpoints
- **End-to-End**: Critical user journeys (ChatGPT App → Backend → Database)

### Test Structure

```
backend/tests/
├── unit/                           # Unit tests (fast, isolated)
│   ├── test_quiz_grader.py         # Rule-based grading logic
│   ├── test_progress_calculator.py # Streak calculation
│   ├── test_search.py              # Search algorithms
│   ├── test_security.py            # JWT, password hashing
│   └── test_r2_client.py           # R2 client (mocked)
│
├── integration/                    # Integration tests (database)
│   ├── test_api_auth.py            # Auth endpoints
│   ├── test_api_content.py         # Content delivery
│   ├── test_api_quizzes.py         # Quiz endpoints
│   ├── test_api_progress.py        # Progress tracking
│   └── test_api_search.py          # Search endpoints
│
├── e2e/                            # End-to-end (full flow)
│   ├── test_student_journey.py     # Complete learning session
│   └── test_chatgpt_integration.py # ChatGPT App → Backend
│
└── conftest.py                     # Pytest fixtures
```

### Key Test Fixtures (`conftest.py`)

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from backend.main import app
from backend.core.config import settings

@pytest.fixture
def test_db():
    """Create test database session."""
    engine = create_engine(settings.TEST_DATABASE_URL)
    with Session(engine) as session:
        yield session
        session.rollback()  # Rollback after each test

@pytest.fixture
def client(test_db):
    """FastAPI test client."""
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    """Authenticated user headers (JWT)."""
    # Register test user
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_course(test_db):
    """Create sample course with chapters."""
    course = Course(title="Test Course", total_chapters=5)
    test_db.add(course)
    test_db.commit()
    return course
```

### Example Unit Test

```python
# backend/tests/unit/test_quiz_grader.py
import pytest
from backend.services.quiz_grader import QuizGrader

def test_grade_multiple_choice_correct():
    grader = QuizGrader()
    assert grader.grade_multiple_choice("B", "B") == True

def test_grade_multiple_choice_case_insensitive():
    grader = QuizGrader()
    assert grader.grade_multiple_choice("b", "B") == True

def test_grade_multiple_choice_incorrect():
    grader = QuizGrader()
    assert grader.grade_multiple_choice("A", "B") == False

def test_grade_fill_in_blank_multiple_answers():
    grader = QuizGrader()
    assert grader.grade_fill_in_blank("GET", ["GET", "get", "Get"]) == True
    assert grader.grade_fill_in_blank("get", ["GET", "get", "Get"]) == True
    assert grader.grade_fill_in_blank("POST", ["GET", "get", "Get"]) == False
```

### Example Integration Test

```python
# backend/tests/integration/test_api_quizzes.py
def test_submit_quiz_success(client, auth_headers, test_db):
    # Arrange: Create quiz
    quiz = create_test_quiz(test_db)

    # Act: Submit quiz
    response = client.post(
        f"/api/quizzes/{quiz.id}/submit",
        headers=auth_headers,
        json={
            "answers": [
                {"question_id": 1, "user_answer": "B"},
                {"question_id": 2, "user_answer": "true"}
            ]
        }
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 100  # Both correct
    assert data["passed"] == True
    assert len(data["results"]) == 2
```

### Constitutional Compliance Tests

```python
# backend/tests/unit/test_constitutional_compliance.py
import sys
import pytest

def test_no_llm_imports():
    """Verify no forbidden LLM libraries are imported."""
    forbidden = ["anthropic", "openai", "langchain", "llama_index"]
    for module in forbidden:
        assert module not in sys.modules, f"Forbidden module '{module}' is imported!"

def test_zero_llm_enforcement_enabled():
    """Verify constitutional enforcement is enabled."""
    from backend.core.config import settings
    assert settings.ENFORCE_ZERO_BACKEND_LLM == True

def test_no_llm_api_keys_in_config():
    """Verify no LLM API keys are configured in Phase 1."""
    from backend.core.config import settings
    assert not hasattr(settings, "ANTHROPIC_API_KEY")
    assert not hasattr(settings, "OPENAI_API_KEY")
```

---

## Security Implementation

### Authentication & Authorization

**JWT Token Structure**:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "tier": "premium",
  "exp": 1234567890,
  "iat": 1234564290,
  "type": "access"
}
```

**Security Utilities** (`backend/core/security.py`):
```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from backend.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

# JWT tokens
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> dict:
    """Decode and verify JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            raise JWTError("Invalid token type")
        return payload
    except JWTError:
        return None
```

### Rate Limiting

**Implementation** (`backend/api/middleware/rate_limit.py`):
```python
from fastapi import HTTPException, Request, status
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """In-memory rate limiter (use Redis in production)."""

    def __init__(self):
        self.requests = defaultdict(list)  # {user_id: [timestamp, ...]}

    async def check_rate_limit(self, request: Request, user_id: int, tier: str):
        """Check if user has exceeded rate limit."""
        from backend.core.constants import RATE_LIMITS

        limit = RATE_LIMITS.get(tier, 50)
        window = timedelta(minutes=1)

        # Get user's recent requests
        now = datetime.utcnow()
        cutoff = now - window

        # Filter requests within window
        self.requests[user_id] = [
            ts for ts in self.requests[user_id] if ts > cutoff
        ]

        # Check limit
        if len(self.requests[user_id]) >= limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Limit: {limit} requests per minute."
            )

        # Record this request
        self.requests[user_id].append(now)

rate_limiter = RateLimiter()
```

### Data Protection

**User Data Isolation**:
- All queries filtered by `user_id`
- Row-level security via SQLModel relationships
- No cross-user data access

**Sensitive Data**:
- Passwords: Bcrypt hashed (12 rounds)
- JWT secret: Environment variable, rotated regularly
- R2 credentials: Environment variables, never logged

---

## Deployment Strategy

### Phase 1 Deployment Architecture

```
                    ┌──────────────┐
                    │  CloudFlare  │
                    │  DNS + CDN   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   ChatGPT    │
                    │     App      │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Fly.io     │
                    │  (FastAPI)   │
                    └──┬───────┬───┘
                       │       │
              ┌────────▼───┐   └────────▼──────┐
              │   Neon     │   │  Cloudflare  │
              │ PostgreSQL │   │      R2      │
              └────────────┘   └──────────────┘
```

### Deployment Steps

1. **Database Setup (Neon)**
   ```bash
   # Create Neon project
   # Copy DATABASE_URL to .env
   # Run migrations
   alembic upgrade head
   ```

2. **R2 Bucket Setup**
   ```bash
   # Create R2 bucket via Cloudflare dashboard
   # Generate API credentials
   # Configure CORS policies
   # Upload initial course content
   ```

3. **Backend Deployment (Fly.io)**
   ```bash
   # Install Fly CLI
   fly auth login

   # Initialize app
   fly launch --name course-companion-api

   # Set secrets
   fly secrets set SECRET_KEY=<random-string>
   fly secrets set DATABASE_URL=<neon-url>
   fly secrets set R2_ACCESS_KEY_ID=<key>
   fly secrets set R2_SECRET_ACCESS_KEY=<secret>

   # Deploy
   fly deploy
   ```

4. **ChatGPT App Deployment**
   - Follow OpenAI Apps deployment guide
   - Configure backend URL
   - Link agent skills
   - Test in ChatGPT

### Environment Configuration

**Production `.env`**:
```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

SECRET_KEY=<generated-secure-random-string>
DATABASE_URL=<neon-postgresql-url>

R2_ENDPOINT_URL=<cloudflare-r2-endpoint>
R2_ACCESS_KEY_ID=<r2-access-key>
R2_SECRET_ACCESS_KEY=<r2-secret-key>

ENFORCE_ZERO_BACKEND_LLM=true
```

---

## Cost Projection (10,000 Users)

| Component | Monthly Cost | Notes |
|-----------|-------------|-------|
| Fly.io (1 instance, 256MB RAM) | $5-10 | Scales with usage |
| Neon PostgreSQL (Free tier) | $0 | <1GB storage, <100h compute |
| Cloudflare R2 | $0.10 | 1MB content, 200K reads |
| Domain (example.com) | $1 | Annual / 12 |
| **TOTAL** | **$6-11** | **$0.0006-$0.0011 per user** |

**Under budget**: $16-41 target → $6-11 actual 🎉

---

## Next Steps

1. **Create tasks.md** (`/sp.tasks`) - Break plan into testable implementation tasks
2. **Choose course content** - Select from 4 options (AI Agent Dev, Cloud-Native Python, GenAI, Modern Python)
3. **Implement Phase 1** - Follow TDD (Red-Green-Refactor)
4. **Deploy & Validate** - Code audit for Zero-Backend-LLM compliance
5. **Create PHR** - Document completion
6. **Suggest ADR** - If architecturally significant decisions made

---

## Appendix: Architectural Decision Log

| ID | Decision | Rationale | Alternatives Considered |
|----|----------|-----------|------------------------|
| AD-001 | Zero-Backend-LLM enforcement | Constitutional requirement, cost efficiency | Trust-based (rejected - too risky) |
| AD-002 | Semantic search via offline embeddings | Avoid LLM API calls while enabling intelligent search | Cloud embedding APIs (rejected - violates constitution) |
| AD-003 | Rule-based quiz grading | Deterministic, testable, fast | LLM grading (rejected - Phase 2 only) |
| AD-004 | Cloudflare R2 for content | 10x cheaper than S3, S3-compatible API | AWS S3 (rejected - cost), Database BLOBs (rejected - performance) |
| AD-005 | Server-side streak calculation | Consistency, timezone handling | Client-side (rejected - trust issues) |
| AD-006 | Middleware-based access control | Centralized, testable, reusable | Route-level checks (rejected - duplication) |

---

**Plan Status**: ✅ Complete
**Next Action**: Create `tasks.md` via `/sp.tasks` command
**Approval Required**: Yes (constitutional compliance verified, awaiting user approval to proceed with implementation)
