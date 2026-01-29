# Chapter 4: Building Agent Skills (Premium)

## What Are Agent Skills?

Agent skills are reusable, composable capabilities that extend your AI agent's functionality. Think of them as specialized modules that your agent can invoke to perform complex tasks.

## Why Build Skills?

Raw tool use is powerful but low-level. Skills provide:
- **Abstraction**: Hide complexity behind simple interfaces
- **Reusability**: Use the same skill across multiple agents
- **Composition**: Combine skills to build more sophisticated behaviors
- **Maintainability**: Update skills without changing agent code
- **Testing**: Unit test skills independently

## Skill Architecture

```
┌─────────────────────────────────────┐
│          AI Agent                   │
└───────────────┬─────────────────────┘
                │
┌───────────────▼─────────────────────┐
│         Skill Manager               │
│  (Discovery, Routing, Execution)    │
└───────────────┬─────────────────────┘
                │
        ┌───────┴────────┬──────────────┐
        │                │              │
┌───────▼──────┐  ┌──────▼─────┐  ┌────▼────────┐
│ Search Skill │  │ Code Skill │  │ Data Skill  │
└───────┬──────┘  └──────┬─────┘  └────┬────────┘
        │                │              │
┌───────▼──────────────────────────────▼─────────┐
│              MCP Servers & Tools               │
└────────────────────────────────────────────────┘
```

## Core Skill Components

### 1. Skill Manifest

Defines skill metadata and capabilities:

```yaml
name: document-analyzer
version: 1.0.0
description: Analyzes documents and extracts insights
author: Your Name
triggers:
  - "analyze document"
  - "summarize file"
  - "extract data from"
capabilities:
  - read_files
  - extract_text
  - generate_summaries
dependencies:
  - filesystem-mcp
  - nlp-tools
```

### 2. Skill Implementation

```python
from typing import Dict, Any
from skills import Skill, SkillResult

class DocumentAnalyzerSkill(Skill):
    """
    Analyzes documents and extracts key information
    """

    def __init__(self):
        self.name = "document-analyzer"
        self.description = "Analyze documents and extract insights"

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Execute the document analysis skill

        Args:
            params: Dictionary containing:
                - file_path: Path to document
                - analysis_type: Type of analysis (summary, entities, sentiment)

        Returns:
            SkillResult with analysis results
        """
        file_path = params.get("file_path")
        analysis_type = params.get("analysis_type", "summary")

        # Read document
        content = await self.read_file(file_path)

        # Perform analysis based on type
        if analysis_type == "summary":
            result = await self.generate_summary(content)
        elif analysis_type == "entities":
            result = await self.extract_entities(content)
        elif analysis_type == "sentiment":
            result = await self.analyze_sentiment(content)
        else:
            return SkillResult(
                success=False,
                error=f"Unknown analysis type: {analysis_type}"
            )

        return SkillResult(
            success=True,
            data=result,
            metadata={
                "file_path": file_path,
                "analysis_type": analysis_type,
                "word_count": len(content.split())
            }
        )

    async def read_file(self, path: str) -> str:
        """Read file using MCP filesystem server"""
        # Call MCP tool
        pass

    async def generate_summary(self, text: str) -> dict:
        """Generate document summary"""
        # Use Claude to summarize
        pass

    async def extract_entities(self, text: str) -> list:
        """Extract named entities"""
        # Use NLP tools
        pass

    async def analyze_sentiment(self, text: str) -> dict:
        """Analyze document sentiment"""
        # Sentiment analysis
        pass
```

### 3. Skill Registration

```python
from skills import SkillRegistry

# Create registry
registry = SkillRegistry()

# Register skills
registry.register(DocumentAnalyzerSkill())
registry.register(WebSearchSkill())
registry.register(CodeGeneratorSkill())

# Agent can now discover and use all registered skills
available_skills = registry.list_skills()
```

## Building Common Skills

### 1. Web Research Skill

```python
class WebResearchSkill(Skill):
    """
    Conducts comprehensive web research on a topic
    """

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        topic = params.get("topic")
        depth = params.get("depth", "basic")  # basic, detailed, comprehensive

        # Step 1: Search for information
        search_results = await self.search_web(topic, num_results=10)

        # Step 2: Extract relevant information
        relevant_data = []
        for result in search_results:
            content = await self.fetch_url(result["url"])
            extracted = await self.extract_key_points(content, topic)
            relevant_data.append(extracted)

        # Step 3: Synthesize findings
        if depth == "basic":
            synthesis = await self.create_summary(relevant_data)
        elif depth == "detailed":
            synthesis = await self.create_detailed_report(relevant_data)
        else:
            synthesis = await self.create_comprehensive_analysis(relevant_data)

        return SkillResult(
            success=True,
            data={
                "topic": topic,
                "sources": len(search_results),
                "synthesis": synthesis,
                "references": [r["url"] for r in search_results]
            }
        )
```

### 2. Code Review Skill

```python
class CodeReviewSkill(Skill):
    """
    Reviews code for quality, security, and best practices
    """

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        code_path = params.get("code_path")
        review_type = params.get("type", "full")  # full, security, style

        # Read code files
        code_files = await self.read_directory(code_path)

        reviews = []
        for file in code_files:
            content = await self.read_file(file)

            # Perform different checks
            if review_type in ["full", "security"]:
                security_issues = await self.check_security(content)
                reviews.append({
                    "file": file,
                    "type": "security",
                    "issues": security_issues
                })

            if review_type in ["full", "style"]:
                style_issues = await self.check_style(content)
                reviews.append({
                    "file": file,
                    "type": "style",
                    "issues": style_issues
                })

            if review_type == "full":
                logic_issues = await self.check_logic(content)
                reviews.append({
                    "file": file,
                    "type": "logic",
                    "issues": logic_issues
                })

        # Generate review report
        report = await self.generate_review_report(reviews)

        return SkillResult(
            success=True,
            data={
                "files_reviewed": len(code_files),
                "total_issues": sum(len(r["issues"]) for r in reviews),
                "report": report,
                "reviews": reviews
            }
        )
```

### 3. Data Analysis Skill

```python
class DataAnalysisSkill(Skill):
    """
    Analyzes datasets and generates insights
    """

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        data_path = params.get("data_path")
        analysis_goals = params.get("goals", ["summary"])

        # Load data
        data = await self.load_dataset(data_path)

        # Perform analyses
        results = {}

        if "summary" in analysis_goals:
            results["summary"] = await self.generate_summary_statistics(data)

        if "trends" in analysis_goals:
            results["trends"] = await self.identify_trends(data)

        if "anomalies" in analysis_goals:
            results["anomalies"] = await self.detect_anomalies(data)

        if "correlations" in analysis_goals:
            results["correlations"] = await self.find_correlations(data)

        if "predictions" in analysis_goals:
            results["predictions"] = await self.generate_predictions(data)

        # Create visualization recommendations
        viz_recommendations = await self.recommend_visualizations(data, results)

        return SkillResult(
            success=True,
            data={
                "dataset": data_path,
                "rows": len(data),
                "analyses": results,
                "visualizations": viz_recommendations
            }
        )
```

## Skill Composition

Combine skills to create more powerful capabilities:

```python
class ResearchAndReportSkill(Skill):
    """
    Combines web research and document generation
    """

    def __init__(self, skill_registry: SkillRegistry):
        self.registry = skill_registry
        self.web_research = skill_registry.get("web-research")
        self.document_writer = skill_registry.get("document-writer")

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        topic = params.get("topic")
        report_format = params.get("format", "markdown")

        # Step 1: Research the topic
        research_result = await self.web_research.execute({
            "topic": topic,
            "depth": "comprehensive"
        })

        if not research_result.success:
            return research_result

        # Step 2: Generate report
        report_result = await self.document_writer.execute({
            "content": research_result.data["synthesis"],
            "format": report_format,
            "title": f"Research Report: {topic}",
            "include_references": True,
            "references": research_result.data["references"]
        })

        return report_result
```

## Skill State Management

Handle multi-step workflows with state:

```python
class MultiStepSkill(Skill):
    """
    Skill that maintains state across multiple steps
    """

    def __init__(self):
        self.state = {}

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        session_id = params.get("session_id")
        step = params.get("step", 1)

        # Load state for this session
        session_state = self.state.get(session_id, {})

        # Execute current step
        if step == 1:
            result = await self.step_1(params)
            session_state["step_1_result"] = result

        elif step == 2:
            # Use results from step 1
            step_1_data = session_state.get("step_1_result")
            result = await self.step_2(params, step_1_data)
            session_state["step_2_result"] = result

        elif step == 3:
            # Combine all previous results
            result = await self.step_3(
                params,
                session_state["step_1_result"],
                session_state["step_2_result"]
            )

        # Save state
        self.state[session_id] = session_state

        return SkillResult(
            success=True,
            data=result,
            metadata={"step": step, "session_id": session_id}
        )
```

## Error Handling in Skills

Robust error handling:

```python
class RobustSkill(Skill):
    """
    Skill with comprehensive error handling
    """

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        try:
            # Validate parameters
            self.validate_params(params)

            # Execute main logic
            result = await self.perform_task(params)

            return SkillResult(success=True, data=result)

        except ValidationError as e:
            return SkillResult(
                success=False,
                error=f"Invalid parameters: {str(e)}",
                error_type="validation"
            )

        except ToolError as e:
            # Tool execution failed, try recovery
            recovery_result = await self.attempt_recovery(e)
            if recovery_result:
                return SkillResult(
                    success=True,
                    data=recovery_result,
                    metadata={"recovered": True}
                )
            return SkillResult(
                success=False,
                error=f"Tool execution failed: {str(e)}",
                error_type="tool_error"
            )

        except Exception as e:
            # Unexpected error
            return SkillResult(
                success=False,
                error=f"Unexpected error: {str(e)}",
                error_type="unknown"
            )

    def validate_params(self, params: Dict[str, Any]):
        """Validate required parameters"""
        required = ["param1", "param2"]
        for param in required:
            if param not in params:
                raise ValidationError(f"Missing required parameter: {param}")
```

## Testing Skills

```python
import pytest
from skills import DocumentAnalyzerSkill

@pytest.mark.asyncio
async def test_document_analyzer_summary():
    skill = DocumentAnalyzerSkill()

    result = await skill.execute({
        "file_path": "test_document.txt",
        "analysis_type": "summary"
    })

    assert result.success
    assert "summary" in result.data
    assert result.metadata["word_count"] > 0

@pytest.mark.asyncio
async def test_document_analyzer_invalid_type():
    skill = DocumentAnalyzerSkill()

    result = await skill.execute({
        "file_path": "test_document.txt",
        "analysis_type": "invalid"
    })

    assert not result.success
    assert "Unknown analysis type" in result.error
```

## Skill Best Practices

1. **Single Responsibility**: Each skill should do one thing well
2. **Clear Interfaces**: Document parameters and return values
3. **Error Recovery**: Implement graceful degradation
4. **Idempotency**: Skills should be safe to retry
5. **Logging**: Track skill execution for debugging
6. **Versioning**: Version skills for backward compatibility

## Practical Exercise

Build a "Smart Inbox" skill that:
1. Reads emails from a folder
2. Categorizes them by importance
3. Generates summaries of urgent emails
4. Suggests responses for common inquiries

```python
class SmartInboxSkill(Skill):
    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        # 1. Read emails
        emails = await self.read_emails(params.get("folder", "inbox"))

        # 2. Categorize
        categorized = await self.categorize_emails(emails)

        # 3. Summarize urgent
        urgent = [e for e in categorized if e["category"] == "urgent"]
        summaries = await self.generate_summaries(urgent)

        # 4. Suggest responses
        responses = await self.suggest_responses(emails)

        return SkillResult(
            success=True,
            data={
                "total_emails": len(emails),
                "urgent": len(urgent),
                "summaries": summaries,
                "suggested_responses": responses
            }
        )
```

## Next Steps

In Chapter 5, we'll explore advanced agent patterns including:
- Multi-agent systems
- Agent orchestration
- Memory and context management
- Production deployment strategies

---

**Estimated Reading Time**: 30 minutes (Premium Content)
**Hands-On Exercise**: Build a skill that combines web search, data extraction, and report generation for competitive analysis.
