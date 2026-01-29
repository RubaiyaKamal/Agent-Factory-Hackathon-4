# Chapter 2: Claude SDK Basics

## Introduction

The Claude SDK by Anthropic provides a powerful foundation for building AI agents. Claude excels at natural conversation, reasoning, and tool use - making it ideal for agent development.

## Why Claude for Agent Development?

### Strengths of Claude

1. **Extended Context Window**: Up to 200K tokens (roughly 150,000 words)
2. **Strong Reasoning**: Excellent at multi-step problems and planning
3. **Tool Use**: Native support for function calling and tool integration
4. **Safety**: Built-in safety guardrails and constitutional AI
5. **Coding Ability**: Excellent at code generation and debugging
6. **Document Understanding**: Handles complex documents with ease

### Claude vs Other LLMs

- **GPT-4**: Comparable intelligence, Claude has longer context
- **Llama**: Open source option, Claude has better instruction following
- **Gemini**: Strong multimodal, Claude excels at text and reasoning

## Setting Up Your Environment

### Install the SDK

```bash
# Python
pip install anthropic

# Node.js
npm install @anthropic-ai/sdk
```

### Get Your API Key

1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Create an account or sign in
3. Navigate to API Keys section
4. Generate a new API key
5. Store it securely (never commit to git!)

### Environment Configuration

```bash
# Create .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# Load environment variables
export ANTHROPIC_API_KEY=your_key_here
```

## Your First Claude Agent

### Basic Message Example (Python)

```python
import anthropic

client = anthropic.Anthropic(
    api_key="your-api-key"
)

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Understanding the Response

```python
{
    "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": "Hello! How can I help you today?"
        }
    ],
    "model": "claude-3-5-sonnet-20241022",
    "stop_reason": "end_turn",
    "usage": {
        "input_tokens": 10,
        "output_tokens": 15
    }
}
```

## Key Claude SDK Concepts

### 1. Messages

Claude uses a message-based API where conversations consist of alternating user and assistant messages:

```python
messages = [
    {"role": "user", "content": "What is 2+2?"},
    {"role": "assistant", "content": "2+2 equals 4."},
    {"role": "user", "content": "What about 3+3?"}
]
```

### 2. System Prompts

System prompts set the agent's behavior and context:

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful math tutor. Explain concepts clearly and show your work.",
    messages=[
        {"role": "user", "content": "How do I solve quadratic equations?"}
    ]
)
```

### 3. Temperature and Sampling

Control randomness and creativity:

```python
# More deterministic (good for factual tasks)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    temperature=0.2,
    messages=[...]
)

# More creative (good for brainstorming)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    temperature=0.9,
    messages=[...]
)
```

### 4. Max Tokens

Control response length:

```python
# Short response
max_tokens=256  # ~200 words

# Medium response
max_tokens=1024  # ~750 words

# Long response
max_tokens=4096  # ~3000 words
```

## Building a Conversational Agent

### Maintaining Conversation History

```python
class ConversationAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.messages = []

    def send_message(self, user_message: str) -> str:
        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # Get Claude's response
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=self.messages
        )

        # Extract assistant's reply
        assistant_message = response.content[0].text

        # Add to history
        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

# Usage
agent = ConversationAgent(api_key="your-key")
print(agent.send_message("Hi, what's your name?"))
print(agent.send_message("Can you help me with Python?"))
```

## Error Handling

### Common Error Types

```python
from anthropic import APIError, RateLimitError, APIConnectionError

try:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[...]
    )
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    # Implement exponential backoff
except APIConnectionError as e:
    print(f"Connection failed: {e}")
    # Retry with different endpoint
except APIError as e:
    print(f"API error: {e}")
    # Log and handle gracefully
```

### Retry Logic with Exponential Backoff

```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def send_message_with_retry(client, messages):
    return client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=messages
    )
```

## Streaming Responses

For real-time user experience:

```python
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Best Practices

### 1. API Key Management

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment")
```

### 2. Token Usage Tracking

```python
def track_usage(response):
    usage = response.usage
    print(f"Input tokens: {usage.input_tokens}")
    print(f"Output tokens: {usage.output_tokens}")

    # Estimate cost (example rates)
    input_cost = usage.input_tokens * 0.003 / 1000
    output_cost = usage.output_tokens * 0.015 / 1000
    total_cost = input_cost + output_cost

    print(f"Estimated cost: ${total_cost:.6f}")
```

### 3. Context Window Management

```python
def trim_conversation_history(messages, max_tokens=150000):
    """Keep conversation within context window"""
    # Estimate tokens (rough: 4 chars per token)
    total_chars = sum(len(m["content"]) for m in messages)
    estimated_tokens = total_chars // 4

    if estimated_tokens > max_tokens:
        # Remove oldest messages (keep system prompt)
        return messages[:1] + messages[-(max_tokens // 100):]

    return messages
```

## Practical Exercise

Build a simple Q&A agent:

```python
def qa_agent(question: str, context: str) -> str:
    """
    Answer questions based on provided context
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    system_prompt = (
        "You are a helpful assistant that answers questions "
        "based on the provided context. If the answer isn't "
        "in the context, say so."
    )

    user_message = f"""
    Context: {context}

    Question: {question}

    Please answer based only on the context above.
    """

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )

    return response.content[0].text

# Test it
context = "Python is a high-level programming language. It was created by Guido van Rossum and released in 1991."
answer = qa_agent("When was Python released?", context)
print(answer)  # "Python was released in 1991."
```

## Next Steps

In Chapter 3, we'll explore the Model Context Protocol (MCP), which allows agents to use external tools and data sources. You'll learn how to:
- Connect agents to databases
- Enable web searching
- Perform calculations
- Access external APIs
- Build custom tool servers

---

**Estimated Reading Time**: 20 minutes
**Hands-On Exercise**: Build a simple agent that maintains conversation history and responds appropriately to follow-up questions.
