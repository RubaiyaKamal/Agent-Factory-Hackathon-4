# Chapter 5: Advanced Agent Patterns (Premium)

## Introduction

As AI agents grow in complexity, you need robust patterns to manage state, orchestrate workflows, and ensure reliability. This chapter covers production-ready patterns for building sophisticated agent systems.

## Multi-Agent Systems

### When to Use Multiple Agents

Use multiple specialized agents when you need:
- **Separation of Concerns**: Different agents for different domains
- **Parallel Processing**: Handle multiple requests simultaneously
- **Specialization**: Expert agents for specific tasks
- **Scalability**: Distribute load across agents

### Agent Coordination Patterns

#### 1. Hierarchical Pattern

```python
class ManagerAgent:
    """
    Coordinates multiple specialist agents
    """

    def __init__(self):
        self.agents = {
            "research": ResearchAgent(),
            "coding": CodingAgent(),
            "testing": TestingAgent(),
            "documentation": DocumentationAgent()
        }

    async def handle_request(self, task: str) -> dict:
        # Analyze task and route to appropriate agent
        task_type = await self.classify_task(task)

        if task_type == "complex":
            # Break down and delegate to multiple agents
            return await self.delegate_complex_task(task)
        else:
            # Route to single specialist agent
            agent = self.agents[task_type]
            return await agent.execute(task)

    async def delegate_complex_task(self, task: str) -> dict:
        """
        Example: Building a feature requires multiple agents
        """
        # 1. Research agent gathers requirements
        research = await self.agents["research"].execute(
            f"Research best practices for: {task}"
        )

        # 2. Coding agent implements
        code = await self.agents["coding"].execute(
            f"Implement based on research: {research}"
        )

        # 3. Testing agent validates
        tests = await self.agents["testing"].execute(
            f"Test the implementation: {code}"
        )

        # 4. Documentation agent documents
        docs = await self.agents["documentation"].execute(
            f"Document the feature: {code}"
        )

        return {
            "research": research,
            "code": code,
            "tests": tests,
            "documentation": docs
        }
```

#### 2. Peer-to-Peer Pattern

```python
class AgentNetwork:
    """
    Agents collaborate as peers
    """

    def __init__(self):
        self.agents = []
        self.message_bus = MessageBus()

    def add_agent(self, agent):
        self.agents.append(agent)
        agent.set_message_bus(self.message_bus)

    async def broadcast_task(self, task: str):
        """
        All agents receive task and decide if they can help
        """
        responses = []
        for agent in self.agents:
            can_handle = await agent.can_handle(task)
            if can_handle:
                response = await agent.execute(task)
                responses.append(response)

        # Combine responses
        return await self.synthesize_responses(responses)
```

#### 3. Pipeline Pattern

```python
class AgentPipeline:
    """
    Agents process data in sequence
    """

    def __init__(self):
        self.stages = []

    def add_stage(self, agent):
        self.stages.append(agent)

    async def process(self, input_data: Any) -> Any:
        """
        Pass data through each agent in sequence
        """
        current_data = input_data

        for agent in self.stages:
            result = await agent.execute(current_data)

            if not result.success:
                # Pipeline breaks on failure
                raise PipelineError(
                    f"Stage {agent.name} failed: {result.error}"
                )

            current_data = result.data

        return current_data

# Usage
pipeline = AgentPipeline()
pipeline.add_stage(DataValidationAgent())
pipeline.add_stage(DataTransformationAgent())
pipeline.add_stage(DataEnrichmentAgent())
pipeline.add_stage(DataStorageAgent())

result = await pipeline.process(raw_data)
```

## Advanced Memory Management

### Short-Term Memory (Context Window)

```python
class ContextManager:
    """
    Manages conversation context within token limits
    """

    def __init__(self, max_tokens: int = 100000):
        self.max_tokens = max_tokens
        self.messages = []
        self.system_prompt = ""

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self.trim_if_needed()

    def trim_if_needed(self):
        """
        Remove oldest messages if over token limit
        """
        total_tokens = self.estimate_tokens()

        while total_tokens > self.max_tokens and len(self.messages) > 2:
            # Keep at least 2 messages (1 user, 1 assistant)
            removed = self.messages.pop(0)
            total_tokens = self.estimate_tokens()

    def estimate_tokens(self) -> int:
        """
        Rough token estimation: 4 characters ≈ 1 token
        """
        total_chars = len(self.system_prompt)
        for msg in self.messages:
            total_chars += len(msg["content"])
        return total_chars // 4

    def get_messages(self) -> list:
        """
        Return messages for API call
        """
        return self.messages
```

### Long-Term Memory (Vector Store)

```python
from typing import List
import chromadb

class LongTermMemory:
    """
    Stores and retrieves information using embeddings
    """

    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("agent_memory")

    async def store(self, key: str, content: str, metadata: dict = None):
        """
        Store information with semantic embeddings
        """
        self.collection.add(
            documents=[content],
            ids=[key],
            metadatas=[metadata or {}]
        )

    async def retrieve(self, query: str, n_results: int = 5) -> List[dict]:
        """
        Retrieve relevant information based on semantic similarity
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        return [
            {
                "content": doc,
                "metadata": meta,
                "similarity": dist
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]

    async def update(self, key: str, content: str):
        """
        Update existing memory
        """
        self.collection.update(
            ids=[key],
            documents=[content]
        )

    async def delete(self, key: str):
        """
        Remove from memory
        """
        self.collection.delete(ids=[key])
```

### Hybrid Memory System

```python
class HybridMemory:
    """
    Combines short-term and long-term memory
    """

    def __init__(self):
        self.short_term = ContextManager()
        self.long_term = LongTermMemory()

    async def add_interaction(self, user_msg: str, assistant_msg: str):
        """
        Add to short-term memory and optionally store important info long-term
        """
        # Add to context
        self.short_term.add_message("user", user_msg)
        self.short_term.add_message("assistant", assistant_msg)

        # Determine if worth storing long-term
        if await self.is_important(user_msg, assistant_msg):
            await self.long_term.store(
                key=f"interaction_{timestamp()}",
                content=f"User: {user_msg}\nAssistant: {assistant_msg}",
                metadata={"timestamp": timestamp()}
            )

    async def get_relevant_context(self, query: str) -> str:
        """
        Retrieve relevant information from long-term memory
        """
        relevant = await self.long_term.retrieve(query, n_results=3)

        context = "Relevant past interactions:\n"
        for item in relevant:
            context += f"- {item['content']}\n"

        return context

    async def is_important(self, user_msg: str, assistant_msg: str) -> bool:
        """
        Determine if interaction should be stored long-term
        """
        # Store if:
        # - User provides preferences
        # - Complex problem solved
        # - Important information shared
        keywords = ["remember", "always", "never", "prefer", "important"]
        return any(kw in user_msg.lower() for kw in keywords)
```

## State Machines for Agent Workflows

```python
from enum import Enum

class AgentState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    ACTING = "acting"
    WAITING = "waiting"
    ERROR = "error"

class StatefulAgent:
    """
    Agent that maintains state through workflows
    """

    def __init__(self):
        self.state = AgentState.IDLE
        self.workflow_data = {}

    async def handle_input(self, user_input: str):
        """
        Process input based on current state
        """
        if self.state == AgentState.IDLE:
            self.state = AgentState.LISTENING
            return await self.start_workflow(user_input)

        elif self.state == AgentState.WAITING:
            # Agent was waiting for user response
            return await self.continue_workflow(user_input)

        elif self.state == AgentState.PROCESSING:
            return "I'm currently processing your previous request. Please wait."

        else:
            return await self.handle_unexpected_state(user_input)

    async def start_workflow(self, input: str):
        """
        Begin multi-step workflow
        """
        self.state = AgentState.PROCESSING

        # Step 1: Understand intent
        intent = await self.classify_intent(input)

        if intent == "complex_task":
            # Need more information
            self.state = AgentState.WAITING
            self.workflow_data["step"] = 1
            return "I need some more details. What is your preferred approach?"

        elif intent == "simple_task":
            # Can handle immediately
            result = await self.execute_simple_task(input)
            self.state = AgentState.IDLE
            return result

    async def continue_workflow(self, input: str):
        """
        Continue multi-step workflow
        """
        self.state = AgentState.PROCESSING
        current_step = self.workflow_data.get("step", 1)

        if current_step == 1:
            # Process user's approach preference
            self.workflow_data["approach"] = input
            self.workflow_data["step"] = 2
            self.state = AgentState.WAITING
            return "Great! Now, what's your timeline?"

        elif current_step == 2:
            # Have all information, execute
            result = await self.execute_complex_task(
                approach=self.workflow_data["approach"],
                timeline=input
            )
            self.state = AgentState.IDLE
            self.workflow_data = {}
            return result
```

## Circuit Breaker Pattern

Prevent cascading failures:

```python
class CircuitBreaker:
    """
    Protects against repeated failures
    """

    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = None

    async def call(self, func, *args, **kwargs):
        """
        Execute function with circuit breaker protection
        """
        if self.state == "OPEN":
            # Check if timeout has passed
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpen("Too many failures, circuit is open")

        try:
            result = await func(*args, **kwargs)

            # Success - reset if in HALF_OPEN
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0

            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

            raise e
```

## Retry Strategies

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

class RobustAgent:
    """
    Agent with intelligent retry mechanisms
    """

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(TemporaryError)
    )
    async def call_api_with_retry(self, prompt: str):
        """
        Retry API calls with exponential backoff
        """
        return await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

    async def adaptive_retry(self, func, max_attempts: int = 3):
        """
        Retry with adaptive strategy based on error type
        """
        for attempt in range(max_attempts):
            try:
                return await func()

            except RateLimitError:
                # Exponential backoff for rate limits
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)

            except NetworkError:
                # Quick retry for network errors
                await asyncio.sleep(1)

            except InvalidRequestError:
                # Don't retry invalid requests
                raise

        raise MaxRetriesExceeded(f"Failed after {max_attempts} attempts")
```

## Production Deployment Patterns

### Health Checks

```python
class AgentHealthCheck:
    """
    Monitor agent health
    """

    async def check_health(self) -> dict:
        """
        Comprehensive health check
        """
        checks = {
            "api_connectivity": await self.check_api(),
            "database": await self.check_database(),
            "memory_usage": await self.check_memory(),
            "response_time": await self.check_performance()
        }

        overall_status = "healthy" if all(
            check["status"] == "ok" for check in checks.values()
        ) else "unhealthy"

        return {
            "status": overall_status,
            "checks": checks,
            "timestamp": time.time()
        }

    async def check_api(self) -> dict:
        """Check API connectivity"""
        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return {"status": "ok", "latency_ms": 50}
        except Exception as e:
            return {"status": "error", "error": str(e)}
```

### Logging and Monitoring

```python
import structlog

class MonitoredAgent:
    """
    Agent with comprehensive logging
    """

    def __init__(self):
        self.logger = structlog.get_logger()

    async def execute(self, task: str):
        """
        Execute with detailed logging
        """
        self.logger.info(
            "task_started",
            task=task,
            timestamp=time.time()
        )

        try:
            result = await self.process_task(task)

            self.logger.info(
                "task_completed",
                task=task,
                duration_ms=100,
                tokens_used=500
            )

            return result

        except Exception as e:
            self.logger.error(
                "task_failed",
                task=task,
                error=str(e),
                error_type=type(e).__name__
            )
            raise
```

## Practical Exercise

Build a production-ready agent system that:
1. Uses multiple specialized agents
2. Implements memory management
3. Has circuit breakers for API calls
4. Includes health checks and monitoring
5. Handles errors gracefully

```python
class ProductionAgentSystem:
    def __init__(self):
        # Multi-agent setup
        self.manager = ManagerAgent()

        # Memory
        self.memory = HybridMemory()

        # Circuit breaker for API calls
        self.circuit_breaker = CircuitBreaker()

        # Monitoring
        self.health_check = AgentHealthCheck()
        self.logger = structlog.get_logger()

    async def handle_request(self, user_input: str):
        """
        Main request handler with all patterns
        """
        try:
            # Add relevant context from memory
            context = await self.memory.get_relevant_context(user_input)

            # Execute with circuit breaker protection
            result = await self.circuit_breaker.call(
                self.manager.handle_request,
                user_input,
                context
            )

            # Store interaction
            await self.memory.add_interaction(user_input, result)

            return result

        except Exception as e:
            self.logger.error("request_failed", error=str(e))
            raise
```

## Key Takeaways

1. **Multi-Agent Systems**: Use specialized agents for complex workflows
2. **Memory Management**: Combine short-term and long-term memory
3. **State Machines**: Handle complex workflows with clear states
4. **Error Handling**: Circuit breakers and retry strategies
5. **Production Ready**: Health checks, logging, monitoring

## Congratulations!

You've completed the AI Agent Development course. You now have the knowledge to build production-ready AI agents using Claude, MCP, and advanced patterns.

Continue your learning:
- Build real-world agent projects
- Contribute to open-source agent frameworks
- Join the AI agent development community
- Stay updated on new LLM capabilities

---

**Estimated Reading Time**: 35 minutes (Premium Content)
**Final Project**: Build a complete production agent system that demonstrates all concepts from this course.
