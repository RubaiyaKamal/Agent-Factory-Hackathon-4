# Practical Applications - Real-World AI Agents

## Building Agents That Solve Real Problems

Now that you understand the principles, let's build agents that people actually use!

---

## Application 1: Study Buddy Agent

### The Problem
Students need help understanding difficult concepts, but tutors are expensive and not always available.

### The Solution
An AI agent that:
- Explains concepts at the student's level
- Answers questions patiently
- Provides practice problems
- Tracks learning progress

### Implementation

```python
class StudyBuddyAgent:
    def __init__(self):
        self.client = anthropic.Client()
        self.student_profile = {
            "level": "beginner",
            "learning_style": "visual",
            "topics_mastered": [],
            "current_topic": None
        }

    def get_system_prompt(self):
        return f"""You are a patient study buddy helping a {self.student_profile['level']} student.

        Teaching Style:
        - Use {self.student_profile['learning_style']} explanations
        - Break complex ideas into simple steps
        - Provide examples and analogies
        - Ask questions to check understanding
        - Celebrate progress and encourage effort

        Topics already mastered: {', '.join(self.student_profile['topics_mastered'])}
        Current topic: {self.student_profile['current_topic']}

        Never:
        - Give direct answers to homework
        - Use jargon without explaining it
        - Move too fast
        - Make the student feel bad for not understanding"""

    def explain_concept(self, concept):
        """Explain a concept at the student's level"""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=self.get_system_prompt(),
            messages=[{
                "role": "user",
                "content": f"Explain {concept} to me"
            }]
        )
        return response.content[0].text

    def generate_practice_problem(self, topic):
        """Create a practice problem"""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=self.get_system_prompt(),
            messages=[{
                "role": "user",
                "content": f"Generate a practice problem for {topic}"
            }]
        )
        return response.content[0].text

    def check_answer(self, problem, student_answer):
        """Provide feedback on an answer"""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=self.get_system_prompt(),
            messages=[{
                "role": "user",
                "content": f"""Problem: {problem}
                Student's answer: {student_answer}

                Provide encouraging feedback. If incorrect, guide them towards the right answer without giving it away."""
            }]
        )
        return response.content[0].text

# Usage
buddy = StudyBuddyAgent()
buddy.student_profile['current_topic'] = "Python functions"

explanation = buddy.explain_concept("Python functions")
print(explanation)

problem = buddy.generate_practice_problem("Python functions")
print(problem)

feedback = buddy.check_answer(problem, "def add(a, b): return a + b")
print(feedback)
```

---

## Application 2: Code Review Assistant

### The Problem
Developers need code reviewed, but reviewers are busy and reviews can be inconsistent.

### The Solution
An AI agent that reviews code for:
- Bugs and errors
- Performance issues
- Best practices
- Security vulnerabilities

### Implementation

```python
class CodeReviewAgent:
    def __init__(self):
        self.client = anthropic.Client()

    def review_code(self, code, language="python"):
        """Comprehensive code review"""
        system_prompt = """You are an experienced code reviewer.

        Review Guidelines:
        1. Identify bugs and errors
        2. Suggest performance improvements
        3. Check for security vulnerabilities
        4. Verify best practices
        5. Comment on code readability

        Format your review as:
        ## Summary
        [Overall assessment]

        ## Issues Found
        ### Critical
        - [Issue 1]

        ### Warnings
        - [Issue 2]

        ## Suggestions
        - [Improvement 1]

        ## Good Practices
        - [What they did well]"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=3000,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Review this {language} code:\n\n```{language}\n{code}\n```"
            }]
        )

        return response.content[0].text

    def suggest_refactoring(self, code):
        """Suggest how to refactor code"""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system="You are a code refactoring expert. Suggest improvements for cleaner, more maintainable code.",
            messages=[{
                "role": "user",
                "content": f"Suggest refactoring for:\n\n```python\n{code}\n```"
            }]
        )

        return response.content[0].text

# Usage
reviewer = CodeReviewAgent()

code_to_review = """
def calc(x, y, op):
    if op == '+':
        return x + y
    elif op == '-':
        return x - y
    elif op == '*':
        return x * y
    elif op == '/':
        return x / y
"""

review = reviewer.review_code(code_to_review)
print(review)

refactoring = reviewer.suggest_refactoring(code_to_review)
print(refactoring)
```

---

## Application 3: Content Writer Agent

### The Problem
Creating content is time-consuming and requires creativity and consistency.

### The Solution
An AI agent that generates content while maintaining brand voice and quality.

### Implementation

```python
class ContentWriterAgent:
    def __init__(self, brand_voice=None):
        self.client = anthropic.Client()
        self.brand_voice = brand_voice or {
            "tone": "professional yet friendly",
            "style": "clear and concise",
            "target_audience": "general public"
        }

    def write_blog_post(self, topic, length="medium"):
        """Generate a blog post"""
        word_count = {"short": 500, "medium": 1000, "long": 1500}

        system_prompt = f"""You are a content writer for our brand.

        Brand Voice:
        - Tone: {self.brand_voice['tone']}
        - Style: {self.brand_voice['style']}
        - Audience: {self.brand_voice['target_audience']}

        Writing Guidelines:
        - Use clear headings and subheadings
        - Include examples and analogies
        - End with a strong conclusion
        - Target length: {word_count[length]} words
        - Make it engaging and valuable"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Write a blog post about: {topic}"
            }]
        )

        return response.content[0].text

    def generate_social_posts(self, topic, platforms=["twitter", "linkedin"]):
        """Generate social media posts"""
        posts = {}

        for platform in platforms:
            if platform == "twitter":
                prompt = f"Write a Twitter thread (5-7 tweets) about {topic}"
                max_tokens = 1024
            elif platform == "linkedin":
                prompt = f"Write a LinkedIn post about {topic}"
                max_tokens = 1536

            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=max_tokens,
                system=f"You create engaging {platform} content in our brand voice: {self.brand_voice['tone']}",
                messages=[{"role": "user", "content": prompt}]
            )

            posts[platform] = response.content[0].text

        return posts

# Usage
writer = ContentWriterAgent(brand_voice={
    "tone": "friendly and informative",
    "style": "conversational with examples",
    "target_audience": "tech enthusiasts"
})

blog_post = writer.write_blog_post("AI Agents in 2024", length="medium")
print(blog_post)

social_posts = writer.generate_social_posts("AI Agents in 2024")
print(social_posts["twitter"])
```

---

## Application 4: Data Analysis Assistant

### The Problem
Analyzing data requires technical skills that not everyone has.

### The Solution
An agent that helps users understand and analyze their data.

### Implementation

```python
class DataAnalysisAgent:
    def __init__(self):
        self.client = anthropic.Client()

    def analyze_csv(self, csv_data, question):
        """Analyze CSV data and answer questions"""
        system_prompt = """You are a data analyst assistant.

        When analyzing data:
        1. Summarize what the data shows
        2. Identify trends and patterns
        3. Answer specific questions
        4. Suggest visualizations
        5. Flag any anomalies

        Be clear and use simple language."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"""Data:
```csv
{csv_data}
```

Question: {question}"""
            }]
        )

        return response.content[0].text

    def generate_insights(self, data_description):
        """Generate insights from data description"""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1536,
            system="You are a data insights expert. Provide actionable insights from data patterns.",
            messages=[{
                "role": "user",
                "content": f"Generate insights from this data: {data_description}"
            }]
        )

        return response.content[0].text

# Usage
analyst = DataAnalysisAgent()

csv_data = """
Date,Sales,Region
2024-01-01,1200,North
2024-01-02,1500,North
2024-01-03,900,South
"""

analysis = analyst.analyze_csv(csv_data, "What are the sales trends?")
print(analysis)
```

---

## Application 5: Meeting Assistant

### The Problem
Meetings generate lots of information that's hard to track and act on.

### The Solution
An agent that processes meeting notes and extracts actionable information.

### Implementation

```python
class MeetingAssistant:
    def __init__(self):
        self.client = anthropic.Client()

    def summarize_meeting(self, transcript):
        """Create meeting summary"""
        system_prompt = """You summarize meetings effectively.

        Extract:
        1. Key Discussion Points
        2. Decisions Made
        3. Action Items (with assignees if mentioned)
        4. Important Dates
        5. Next Steps

        Format for easy scanning."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Summarize this meeting:\n\n{transcript}"
            }]
        )

        return response.content[0].text

    def extract_action_items(self, transcript):
        """Extract just the action items"""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="Extract action items from meetings. Format as: - [Action] - Assigned to: [Person] - Due: [Date]",
            messages=[{
                "role": "user",
                "content": f"Extract action items from:\n\n{transcript}"
            }]
        )

        return response.content[0].text

# Usage
assistant = MeetingAssistant()

transcript = """
Team discussed the Q2 launch. Sarah will prepare the marketing plan by March 15.
John agreed to finalize the budget by March 10. We decided to use the blue design
for the website. Next meeting scheduled for March 20.
"""

summary = assistant.summarize_meeting(transcript)
print(summary)

actions = assistant.extract_action_items(transcript)
print(actions)
```

---

## Integration Patterns

### Pattern 1: Agent with External API

```python
import requests

class WeatherAgent:
    def __init__(self, api_key):
        self.client = anthropic.Client()
        self.weather_api_key = api_key

    def get_weather_report(self, location):
        # Step 1: Get real weather data
        weather_data = requests.get(
            f"https://api.weatherapi.com/v1/current.json?key={self.weather_api_key}&q={location}"
        ).json()

        # Step 2: Have agent interpret it
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="You are a friendly weather reporter. Make weather data easy to understand.",
            messages=[{
                "role": "user",
                "content": f"Create a weather report for {location} using this data: {weather_data}"
            }]
        )

        return response.content[0].text
```

### Pattern 2: Agent with Database

```python
import sqlite3

class CustomerAgent:
    def __init__(self, db_path):
        self.client = anthropic.Client()
        self.db = sqlite3.connect(db_path)

    def answer_customer_query(self, question, customer_id):
        # Step 1: Get relevant data
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
        orders = cursor.fetchall()

        # Step 2: Have agent answer using the data
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="You are a customer service agent. Use order data to answer questions helpfully.",
            messages=[{
                "role": "user",
                "content": f"Customer orders: {orders}\n\nCustomer question: {question}"
            }]
        )

        return response.content[0].text
```

---

## Deployment Considerations

### 1. Cost Management

```python
def estimate_cost(input_tokens, output_tokens):
    """Estimate API cost"""
    # Claude pricing (example rates)
    input_cost_per_million = 3.00
    output_cost_per_million = 15.00

    input_cost = (input_tokens / 1_000_000) * input_cost_per_million
    output_cost = (output_tokens / 1_000_000) * output_cost_per_million

    return input_cost + output_cost

# Track usage
total_input_tokens = 0
total_output_tokens = 0

# After each API call
total_input_tokens += response.usage.input_tokens
total_output_tokens += response.usage.output_tokens

print(f"Estimated cost: ${estimate_cost(total_input_tokens, total_output_tokens):.4f}")
```

### 2. Rate Limiting

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests_per_minute=50):
        self.max_requests = max_requests_per_minute
        self.requests = deque()

    def wait_if_needed(self):
        now = time.time()

        # Remove requests older than 1 minute
        while self.requests and now - self.requests[0] > 60:
            self.requests.popleft()

        # If at limit, wait
        if len(self.requests) >= self.max_requests:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)

        self.requests.append(time.time())

# Usage
rate_limiter = RateLimiter(max_requests_per_minute=50)

def call_agent(message):
    rate_limiter.wait_if_needed()
    return agent.respond(message)
```

### 3. Caching

```python
from functools import lru_cache
import hashlib

class CachedAgent:
    def __init__(self):
        self.client = anthropic.Client()
        self.cache = {}

    def get_cache_key(self, message):
        """Generate cache key from message"""
        return hashlib.md5(message.encode()).hexdigest()

    def respond(self, message, use_cache=True):
        # Check cache
        if use_cache:
            cache_key = self.get_cache_key(message)
            if cache_key in self.cache:
                print("Using cached response")
                return self.cache[cache_key]

        # Get fresh response
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": message}]
        )

        result = response.content[0].text

        # Cache it
        if use_cache:
            self.cache[cache_key] = result

        return result
```

---

## Practice Projects

### Project 1: Email Assistant
Build an agent that:
- Categorizes emails (urgent, spam, newsletter)
- Drafts replies
- Summarizes long email threads

### Project 2: Recipe Generator
Build an agent that:
- Generates recipes from ingredients
- Adjusts serving sizes
- Suggests substitutions

### Project 3: Study Guide Creator
Build an agent that:
- Converts text into study guides
- Generates flashcards
- Creates practice quizzes

---

## Quick Summary

**5 Real-World Applications:**
1. **Study Buddy** - Personalized tutoring
2. **Code Reviewer** - Automated code review
3. **Content Writer** - Brand-consistent content
4. **Data Analyst** - Data insights
5. **Meeting Assistant** - Meeting summaries

**Key Integration Patterns:**
- External APIs for real-time data
- Databases for persistent information
- Caching for performance
- Rate limiting for reliability

---

## What's Next?

Ready for advanced techniques?

✅ **Advanced Techniques** (Next Section)
   - Multi-agent systems
   - Advanced prompt engineering
   - Performance optimization

---

**Duration:** 40 minutes
**Difficulty:** Intermediate-Advanced
**Prerequisites:** Core Principles

*Build agents that people actually use!*
