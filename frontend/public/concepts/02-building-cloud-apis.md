# Building Cloud-Ready APIs with Python

## From Theory to Practice 🛠️

In Chapter 1, you learned the **why** of cloud-native development. Now let's learn the **how**!

### What You'll Build
By the end of this chapter, you'll have built:
- A production-ready FastAPI application
- Health checks and monitoring endpoints
- Database integration (cloud-ready!)
- Error handling and logging
- Docker containerization

Let's build something real! 🚀

---

## Setting Up Your Cloud-Native Python Project

### Project Structure

```
my-cloud-app/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration management
│   ├── models.py        # Database models
│   └── routes/
│       ├── __init__.py
│       ├── health.py    # Health check endpoints
│       └── api.py       # API endpoints
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .env                 # Environment variables (don't commit!)
├── .env.example         # Example env file (commit this)
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container definition
└── README.md           # Documentation
```

---

## Step 1: Configuration Management (The Right Way!)

### config.py - Centralized Configuration

```python
"""
Configuration management using environment variables.
Follows 12-factor app methodology.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App Settings
    app_name: str = "My Cloud API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False

    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000

    # Database Settings
    database_url: str = "sqlite:///./app.db"

    # Security
    secret_key: str = "change-this-in-production"
    api_key: str = ""

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """
    Create and cache settings instance.
    Uses lru_cache so settings are loaded only once.
    """
    return Settings()

# Usage in other files:
# from app.config import get_settings
# settings = get_settings()
```

### .env.example - Template for Environment Variables

```bash
# Application
APP_NAME=My Cloud API
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Security (CHANGE THESE IN PRODUCTION!)
SECRET_KEY=your-secret-key-here
API_KEY=your-api-key-here

# Logging
LOG_LEVEL=INFO
```

**Why This Approach?**
- ✅ Type-safe configuration with Pydantic
- ✅ Environment-specific settings
- ✅ Easy to change without touching code
- ✅ Cached for performance

---

## Step 2: Building the Core Application

### main.py - FastAPI Application

```python
"""
Main FastAPI application.
Cloud-native design with proper logging, health checks, and error handling.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from app.config import get_settings
from app.routes import health, api

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle.
    Startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")

    yield  # Application runs here

    # Shutdown
    logger.info("Shutting down gracefully...")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Cloud-native Python API",
    lifespan=lifespan
)

# CORS middleware (for web frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(api.router, prefix="/api/v1", tags=["API"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs",
        "health": "/health"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected errors gracefully."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return {
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }
```

---

## Step 3: Health Checks (Critical for Cloud!)

### routes/health.py - Health Check Endpoints

```python
"""
Health check endpoints for Kubernetes and load balancers.
Essential for cloud-native applications!
"""

from fastapi import APIRouter, status
from pydantic import BaseModel
import time
import psutil
from datetime import datetime

router = APIRouter()

# Store startup time
startup_time = time.time()

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    uptime_seconds: float
    version: str

class DetailedHealthResponse(HealthResponse):
    """Detailed health check with system metrics."""
    cpu_percent: float
    memory_percent: float
    disk_percent: float

@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Basic health check endpoint.
    Returns 200 OK if service is running.

    Used by:
    - Kubernetes liveness probe
    - Load balancers
    - Monitoring systems
    """
    uptime = time.time() - startup_time

    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        uptime_seconds=round(uptime, 2),
        version="1.0.0"
    )

@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.
    Returns 200 OK if service can accept traffic.

    Used by:
    - Kubernetes readiness probe
    - Load balancers (before routing traffic)

    In production, check:
    - Database connectivity
    - External API availability
    - Cache connectivity
    """
    # TODO: Add actual readiness checks
    # Example: Check database connection
    # if not database.is_connected():
    #     raise HTTPException(status_code=503, detail="Database not ready")

    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/detailed", response_model=DetailedHealthResponse)
async def detailed_health():
    """
    Detailed health metrics.
    Includes system resource usage.

    Useful for:
    - Monitoring dashboards
    - Debugging performance issues
    - Capacity planning
    """
    uptime = time.time() - startup_time

    return DetailedHealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        uptime_seconds=round(uptime, 2),
        version="1.0.0",
        cpu_percent=psutil.cpu_percent(interval=1),
        memory_percent=psutil.virtual_memory().percent,
        disk_percent=psutil.disk_usage('/').percent
    )
```

**Why Health Checks Matter:**
- Kubernetes uses them to restart unhealthy pods
- Load balancers use them to route traffic
- Monitoring systems use them for alerts

---

## Step 4: Building API Endpoints

### routes/api.py - RESTful API Endpoints

```python
"""
API endpoints for your application.
Following RESTful best practices.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Data models
class Task(BaseModel):
    """Task model."""
    id: int
    title: str
    description: str = ""
    completed: bool = False

class TaskCreate(BaseModel):
    """Task creation model."""
    title: str
    description: str = ""

# In-memory storage (use database in production!)
tasks_db = {}
task_counter = 0

@router.get("/tasks", response_model=List[Task])
async def get_tasks():
    """
    Get all tasks.

    Cloud-native consideration:
    - Returns empty list if no tasks (not error)
    - Logs access for monitoring
    """
    logger.info(f"Fetching all tasks. Count: {len(tasks_db)}")
    return list(tasks_db.values())

@router.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """
    Create a new task.

    Cloud-native considerations:
    - Returns 201 Created with the new resource
    - Logs creation for audit trail
    - Validates input with Pydantic
    """
    global task_counter
    task_counter += 1

    new_task = Task(
        id=task_counter,
        title=task.title,
        description=task.description,
        completed=False
    )

    tasks_db[task_counter] = new_task
    logger.info(f"Created task {task_counter}: {task.title}")

    return new_task

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """
    Get a specific task.

    Cloud-native considerations:
    - Returns 404 if not found (proper HTTP semantics)
    - Logs access for monitoring
    """
    if task_id not in tasks_db:
        logger.warning(f"Task {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")

    logger.info(f"Fetching task {task_id}")
    return tasks_db[task_id]

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskCreate):
    """
    Update a task.

    Cloud-native considerations:
    - Returns updated resource
    - Logs modification for audit trail
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks_db[task_id].title = task.title
    tasks_db[task_id].description = task.description

    logger.info(f"Updated task {task_id}")
    return tasks_db[task_id]

@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """
    Delete a task.

    Cloud-native considerations:
    - Returns 204 No Content (successful deletion)
    - Logs deletion for audit trail
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks_db[task_id]
    logger.info(f"Deleted task {task_id}")
    return None
```

---

## Step 5: Containerization with Docker

### Dockerfile - Production-Ready Container

```dockerfile
# Multi-stage build for smaller images
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/app/.local

# Copy application code
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Add local bin to PATH
ENV PATH=/home/app/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### .dockerignore - Exclude Unnecessary Files

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.git
.gitignore
.env
.pytest_cache
.coverage
htmlcov/
dist/
build/
*.egg-info/
```

---

## Step 6: Dependencies Management

### requirements.txt

```
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Configuration
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0

# System Monitoring
psutil==5.9.6

# Development
pytest==7.4.3
httpx==0.25.2  # For testing
```

---

## Running Your Cloud-Native App

### Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file from example
cp .env.example .env

# 4. Run the app
uvicorn app.main:app --reload

# 5. Visit http://localhost:8000
# - API docs: http://localhost:8000/docs
# - Health check: http://localhost:8000/health
```

### With Docker

```bash
# Build image
docker build -t my-cloud-app .

# Run container
docker run -p 8000:8000 --env-file .env my-cloud-app

# Or with environment variables
docker run -p 8000:8000 \
    -e ENVIRONMENT=production \
    -e DATABASE_URL=postgresql://... \
    my-cloud-app
```

---

## Testing Your API

### Manual Testing with curl

```bash
# Check health
curl http://localhost:8000/health

# Get all tasks
curl http://localhost:8000/api/v1/tasks

# Create a task
curl -X POST http://localhost:8000/api/v1/tasks \
    -H "Content-Type: application/json" \
    -d '{"title": "Learn Cloud-Native", "description": "Master Python in the cloud"}'

# Get specific task
curl http://localhost:8000/api/v1/tasks/1

# Update task
curl -X PUT http://localhost:8000/api/v1/tasks/1 \
    -H "Content-Type: application/json" \
    -d '{"title": "Master Cloud-Native", "description": "Become an expert!"}'

# Delete task
curl -X DELETE http://localhost:8000/api/v1/tasks/1
```

### Automated Testing

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_task():
    """Test creating a task."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "description": "Testing"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] is False

def test_get_tasks():
    """Test getting all tasks."""
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

Run tests:
```bash
pytest tests/
```

---

## Cloud-Native Best Practices Checklist

### ✅ Configuration
- [x] Environment variables for all config
- [x] No hardcoded secrets
- [x] .env.example provided

### ✅ Logging
- [x] Structured logging to stdout
- [x] Log levels configurable
- [x] Request/response logging

### ✅ Health Checks
- [x] /health endpoint (liveness)
- [x] /health/ready endpoint (readiness)
- [x] /health/detailed for monitoring

### ✅ Error Handling
- [x] Global exception handler
- [x] Proper HTTP status codes
- [x] Meaningful error messages

### ✅ Containerization
- [x] Multi-stage Dockerfile
- [x] Non-root user
- [x] Health check in container
- [x] .dockerignore file

### ✅ Security
- [x] Non-root container user
- [x] No secrets in code
- [x] Input validation (Pydantic)

---

## What You've Learned

🎉 **Congratulations!** You've built a production-ready cloud-native Python API!

You now know how to:
- ✅ Structure a cloud-native Python project
- ✅ Manage configuration properly
- ✅ Build RESTful APIs with FastAPI
- ✅ Implement health checks
- ✅ Handle errors gracefully
- ✅ Log everything properly
- ✅ Containerize with Docker
- ✅ Test your API

---

## Next Steps

Ready to level up? Next chapter covers:
- **Database Integration** - PostgreSQL in the cloud
- **Kubernetes Deployment** - Running in production
- **Monitoring & Observability** - Prometheus, Grafana
- **CI/CD Pipelines** - Automated deployment

---

**Duration:** 40 minutes
**Difficulty:** Intermediate
**Prerequisites:** Chapter 1 - Introduction to Cloud-Native

*You're now ready to deploy real applications to the cloud! ☁️🚀*
