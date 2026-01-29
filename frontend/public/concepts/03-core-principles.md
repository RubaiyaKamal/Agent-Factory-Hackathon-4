# Core Principles - Building Effective AI Agents

## The Foundation of Great Agents

### What Makes an Agent "Good"?

A great AI agent is:
- **Reliable** - Does what it's supposed to do
- **Clear** - Easy to understand and use
- **Helpful** - Actually solves problems
- **Safe** - Doesn't cause harm or confusion

Let's learn the principles that make this possible!

---

## Principle 1: Clear Instructions (The System Prompt)

### What is a System Prompt?

Think of it as your agent's job description + personality + rulebook all in one.

**Basic Example:**
```python
system = "You are a helpful assistant."
```

**Better Example:**
```python
system = """You are a patient coding tutor who:
- Explains concepts step-by-step
- Uses simple language and examples
- Encourages students when they struggle
- Never gives complete solutions, only hints
- Always asks if the student understands"""
```

### The 3 Parts of a Great System Prompt

**1. Identity (WHO)**
```
"You are a [role]..."
```

**2. Behavior (HOW)**
```
"You should:
- Always...
- Never...
- When X happens, do Y..."
```

**3. Constraints (BOUNDARIES)**
```
"You must not:
- Provide medical advice
- Share personal information
- Make decisions for the user"
```

---

## Principle 2: Context Management

### What is Context?

Context is everything the agent remembers during a conversation.

**Simple Analogy:**
Imagine talking to a friend who forgets everything you said 5 seconds ago. Frustrating, right? That's why context matters!

### The Context Window

**Visual Representation:**
```
[────────── Context Window (100k tokens) ──────────]
│ System │ Message 1 │ Message 2 │ ... │ Message N │
└─────────────────────────────────────────────────┘
                                            ↑
                                      Most Recent
```

### Context Management Strategies

**Strategy 1: Summarization**
```python
def summarize_if_needed(conversation):
    # If conversation is getting long...
    if len(conversation) > 20:
        # Summarize older messages
        summary = create_summary(conversation[:10])
        # Keep recent messages
        return [summary] + conversation[10:]
    return conversation
```

**Strategy 2: Selective Memory**
```python
# Keep only important information
important_context = {
    "user_name": "John",
    "user_goal": "Learn Python",
    "current_topic": "Functions",
    "key_facts": ["prefers examples", "beginner level"]
}
```

**Strategy 3: External Memory**
```python
# Store information outside the conversation
save_to_database("user_id", "preferences", preferences)

# Retrieve when needed
preferences = load_from_database("user_id", "preferences")
```

---

## Principle 3: Prompt Engineering

### What is Prompt Engineering?

The art of crafting inputs to get the best outputs from your agent.

### Technique 1: Be Specific

❌ **Vague:**
```python
"Write something about Python"
```

✅ **Specific:**
```python
"Write a 3-paragraph introduction to Python for complete beginners.
Include: what Python is, why it's popular, and one simple example."
```

### Technique 2: Provide Examples

**Few-Shot Learning:**
```python
system = """You are a sentiment analyzer.

Examples:
Input: "I love this product!"
Output: POSITIVE

Input: "This is terrible."
Output: NEGATIVE

Input: "It's okay, I guess."
Output: NEUTRAL

Now analyze the sentiment of user messages."""
```

### Technique 3: Chain of Thought

Ask the agent to think step-by-step:

```python
message = """Solve this problem step by step:

Problem: A store has 50 apples. They sell 15 in the morning
and 20 in the afternoon. How many are left?

Show your work:
Step 1: ...
Step 2: ...
Final Answer: ..."""
```

### Technique 4: Role Playing

```python
system = """You are Socrates, the ancient Greek philosopher.
When answering questions:
- Ask probing questions back
- Guide students to find answers themselves
- Use the Socratic method
- Be wise and patient"""
```

---

## Principle 4: Error Handling and Validation

### Input Validation

Always check user input before processing:

```python
def validate_input(user_input):
    # Check if empty
    if not user_input.strip():
        return False, "Please enter something!"

    # Check length
    if len(user_input) > 5000:
        return False, "Input too long! Keep it under 5000 characters."

    # Check for inappropriate content
    if contains_inappropriate_content(user_input):
        return False, "Please keep the conversation appropriate."

    return True, "Valid input"

# Use it
is_valid, message = validate_input(user_input)
if not is_valid:
    print(message)
    return
```

### Output Validation

Make sure the agent's response is appropriate:

```python
def validate_output(agent_response):
    # Check for harmful content
    if contains_harmful_content(agent_response):
        return "I apologize, but I can't provide that information."

    # Check if response makes sense
    if is_nonsense(agent_response):
        return "Let me try that again..."

    return agent_response
```

### Graceful Degradation

When things go wrong, fail gracefully:

```python
try:
    response = agent.generate_response(user_input)
except APIError:
    response = "I'm having trouble connecting. Please try again."
except RateLimitError:
    response = "Too many requests. Please wait a moment."
except Exception as e:
    response = "Something went wrong. Let me try a different approach."
    log_error(e)
```

---

## Principle 5: Agent Loops and Workflows

### The Basic Agent Loop

```python
def agent_loop():
    while True:
        # 1. Get input
        user_input = get_user_input()
        if user_input == "quit":
            break

        # 2. Process
        agent_response = process_with_agent(user_input)

        # 3. Output
        display_response(agent_response)

        # 4. Update state
        update_conversation_history(user_input, agent_response)
```

### Advanced: Multi-Step Workflows

```python
def research_workflow(topic):
    """Example: Research assistant workflow"""

    # Step 1: Understand the topic
    understanding = agent.analyze(f"What are key aspects of {topic}?")

    # Step 2: Break down research tasks
    tasks = agent.create_tasks(understanding)

    # Step 3: Execute each task
    results = []
    for task in tasks:
        result = agent.execute(task)
        results.append(result)

    # Step 4: Synthesize findings
    final_report = agent.synthesize(results)

    return final_report
```

### ReAct Pattern (Reason + Act)

```python
def react_agent(question):
    """
    Reason about what to do, then act on it
    """
    max_iterations = 5

    for i in range(max_iterations):
        # Thought: What should I do?
        thought = agent.think(question, context)

        # Action: Do it
        if "search" in thought:
            result = search_tool(thought.query)
        elif "calculate" in thought:
            result = calculator_tool(thought.expression)
        elif "done" in thought:
            return thought.answer

        # Observation: What happened?
        context.add(f"Observation: {result}")
```

---

## Principle 6: Testing and Evaluation

### Test Your Agent Thoroughly

**Create Test Cases:**
```python
test_cases = [
    {
        "input": "What is 2+2?",
        "expected": "4",
        "category": "simple_math"
    },
    {
        "input": "Explain quantum physics to a 5-year-old",
        "expected_contains": ["simple", "example"],
        "category": "explanation"
    },
    {
        "input": "Tell me a joke",
        "expected_type": "humorous",
        "category": "entertainment"
    }
]

def run_tests(agent, test_cases):
    results = []
    for test in test_cases:
        response = agent.respond(test["input"])
        passed = evaluate_response(response, test)
        results.append({"test": test, "passed": passed})
    return results
```

### Evaluation Metrics

**1. Accuracy**
- Does it give correct answers?

**2. Consistency**
- Does it give the same answer to the same question?

**3. Latency**
- How fast does it respond?

**4. Safety**
- Does it avoid harmful outputs?

**5. User Satisfaction**
- Do users find it helpful?

---

## Principle 7: Continuous Improvement

### The Improvement Cycle

```
┌─────────────────────────────────────┐
│  1. Collect Feedback                │
│     ↓                                │
│  2. Analyze Problems                │
│     ↓                                │
│  3. Update Instructions/Logic       │
│     ↓                                │
│  4. Test Changes                    │
│     ↓                                │
│  5. Deploy Improvements             │
│     ↓                                │
└────→ Back to Step 1                 │
```

### Logging for Improvement

```python
def log_interaction(user_input, agent_response, feedback):
    log_entry = {
        "timestamp": datetime.now(),
        "input": user_input,
        "output": agent_response,
        "user_feedback": feedback,
        "conversation_id": session_id
    }
    save_to_log(log_entry)

# Later, analyze logs
def analyze_problems():
    logs = load_logs()

    # Find common issues
    negative_feedback = [l for l in logs if l["user_feedback"] == "bad"]

    # Identify patterns
    common_problems = find_patterns(negative_feedback)

    return common_problems
```

---

## Best Practices Checklist

### Before Deploying Your Agent:

- [ ] Clear system prompt with identity, behavior, and constraints
- [ ] Input validation for all user inputs
- [ ] Output validation for all agent responses
- [ ] Error handling for common failure cases
- [ ] Conversation context management
- [ ] Test cases covering typical scenarios
- [ ] Test cases covering edge cases
- [ ] Logging for monitoring and improvement
- [ ] Rate limiting to prevent abuse
- [ ] Cost monitoring (API usage)

---

## Common Anti-Patterns (AVOID!)

### ❌ Anti-Pattern 1: Vague Instructions
```python
system = "Be helpful"  # Too vague!
```

### ❌ Anti-Pattern 2: No Error Handling
```python
response = agent.respond(input)  # What if it fails?
print(response)
```

### ❌ Anti-Pattern 3: Infinite Context
```python
# Keeping entire conversation forever
conversation.append(message)  # Memory leak!
```

### ❌ Anti-Pattern 4: No Testing
```python
# Just hoping it works... 🤞
```

### ❌ Anti-Pattern 5: Hardcoded Logic
```python
if input == "hello":
    return "hi"
elif input == "goodbye":
    return "bye"
# ... (listing every possibility)
```

---

## Practice Exercises

### Exercise 1: Improve a System Prompt
Take this basic prompt and make it better:
```
"You help with homework"
```

### Exercise 2: Build Context Management
Create a function that keeps context under a token limit.

### Exercise 3: Create Test Suite
Write 10 test cases for a math tutor agent.

### Exercise 4: Implement Error Handling
Add proper error handling to this code:
```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": input}]
)
print(response.content[0].text)
```

---

## Real-World Example: Customer Support Agent

```python
class CustomerSupportAgent:
    def __init__(self):
        self.client = anthropic.Client()
        self.system_prompt = """You are a customer support agent for TechCo.

        Guidelines:
        - Be friendly and empathetic
        - Ask clarifying questions before suggesting solutions
        - Provide step-by-step instructions
        - If you can't solve it, escalate to human support
        - Never make promises about refunds or policies

        Knowledge:
        - Product warranty: 1 year
        - Return policy: 30 days
        - Support hours: 9 AM - 5 PM EST"""

    def respond(self, user_message, context):
        # Validate input
        if not self.validate_input(user_message):
            return "Please provide more details about your issue."

        # Build conversation
        messages = self.build_messages(context, user_message)

        try:
            # Get response
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=self.system_prompt,
                messages=messages
            )

            # Validate output
            return self.validate_output(response.content[0].text)

        except Exception as e:
            return "I'm experiencing technical difficulties. A human agent will assist you shortly."
```

---

## Quick Summary

**7 Core Principles:**
1. **Clear Instructions** - Define agent behavior precisely
2. **Context Management** - Remember what matters, forget what doesn't
3. **Prompt Engineering** - Craft inputs for best outputs
4. **Error Handling** - Fail gracefully
5. **Agent Loops** - Structure workflows effectively
6. **Testing** - Verify everything works
7. **Improvement** - Learn from feedback

---

## What's Next?

You're now ready for:

✅ **Practical Applications** (Next Section)
   - Building real-world agents
   - Integrating with tools and APIs
   - Deploying to production

---

**Duration:** 30 minutes
**Difficulty:** Intermediate
**Prerequisites:** Introduction to Concepts, Getting Started

*Master these principles, and you'll build agents that actually work!*
