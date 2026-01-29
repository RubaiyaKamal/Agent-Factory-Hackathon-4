# Getting Started - Building Your First AI Agent

## Setting Up Your Environment

### What You'll Need

**Software Requirements:**
- ✅ Python 3.10 or higher
- ✅ Code editor (VS Code recommended)
- ✅ Terminal/Command line access
- ✅ Claude API key (we'll get this!)

**Don't worry if you're new to this - we'll walk through everything step by step!**

---

## Getting Your Claude API Key

### Step 1: Create an Anthropic Account
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Click "Sign Up"
3. Enter your email and create a password
4. Verify your email

### Step 2: Get Your API Key
1. Log in to the console
2. Click "API Keys" in the sidebar
3. Click "Create Key"
4. Copy your key (it looks like: `sk-ant-api03-...`)
5. **Keep it secret!** Never share it publicly

### Step 3: Store Your Key Safely
Create a file called `.env`:
```bash
ANTHROPIC_API_KEY=your_key_here
```

---

## Your First Agent - Hello World!

### Simple Example
Let's create the simplest possible AI agent:

```python
# hello_agent.py
import anthropic

# Initialize Claude
client = anthropic.Client(api_key="your_key_here")

# Send a message
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello! What can you do?"}
    ]
)

# Print the response
print(message.content[0].text)
```

**Run it:**
```bash
python hello_agent.py
```

**Expected Output:**
```
Hello! I'm Claude, an AI assistant. I can help you with many tasks like:
- Answering questions
- Writing and editing
- Problem solving
- And much more!
```

🎉 **Congratulations!** You just created your first AI agent!

---

## Understanding the Code

### Breaking It Down

```python
# 1. Import the library
import anthropic

# 2. Create a client (connects to Claude)
client = anthropic.Client(api_key="your_key_here")

# 3. Send a message
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",  # Which Claude version
    max_tokens=1024,                      # Max length of response
    messages=[                            # Your conversation
        {"role": "user", "content": "Hello!"}
    ]
)

# 4. Get the response
response_text = message.content[0].text
```

---

## Making It More Useful

### Adding Instructions (System Prompt)

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a friendly tutor who explains things simply.",  # ← New!
    messages=[
        {"role": "user", "content": "What is Python?"}
    ]
)
```

**Why this matters:**
The `system` prompt tells Claude HOW to behave. It's like giving your agent a personality and job description!

---

## Building a Conversational Agent

### Multi-Turn Conversation

```python
def chat_with_agent():
    client = anthropic.Client(api_key="your_key_here")
    conversation = []

    print("Chat with your agent (type 'quit' to exit)")

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        # Add to conversation
        conversation.append({"role": "user", "content": user_input})

        # Get agent response
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=conversation
        )

        agent_response = message.content[0].text
        print(f"Agent: {agent_response}")

        # Add agent response to conversation
        conversation.append({"role": "assistant", "content": agent_response})

# Run it!
chat_with_agent()
```

**Try it out:**
```
You: What's your name?
Agent: I'm Claude, an AI assistant.

You: What did I just ask you?
Agent: You asked me what my name is.
```

✨ **See how it remembers?** That's the power of conversation history!

---

## Common Patterns

### Pattern 1: Question Answering

```python
def ask_agent(question):
    client = anthropic.Client(api_key="your_key_here")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system="You are a helpful assistant that answers questions clearly.",
        messages=[{"role": "user", "content": question}]
    )

    return message.content[0].text

# Use it
answer = ask_agent("What is machine learning?")
print(answer)
```

### Pattern 2: Text Processing

```python
def improve_text(text):
    client = anthropic.Client(api_key="your_key_here")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system="You improve writing by fixing grammar and making it clearer.",
        messages=[{"role": "user", "content": f"Improve this text: {text}"}]
    )

    return message.content[0].text

# Use it
original = "me and my friend goed to store yesterday"
improved = improve_text(original)
print(f"Original: {original}")
print(f"Improved: {improved}")
```

---

## Error Handling

### Always Handle Errors!

```python
try:
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(message.content[0].text)

except anthropic.APIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

**Common Errors:**
- ❌ Invalid API key → Check your `.env` file
- ❌ Rate limit → You're sending too many requests
- ❌ Network error → Check your internet connection

---

## Best Practices

### 1. Keep Your API Key Secret

❌ **Bad:**
```python
api_key = "sk-ant-api03-1234..."  # In your code!
```

✅ **Good:**
```python
import os
api_key = os.getenv("ANTHROPIC_API_KEY")  # From .env file
```

### 2. Use Clear Instructions

❌ **Bad:**
```python
system = "help"
```

✅ **Good:**
```python
system = """You are a helpful coding tutor.
- Explain concepts simply
- Provide code examples
- Be patient and encouraging"""
```

### 3. Limit Token Usage

```python
max_tokens=1024  # For short responses
max_tokens=4096  # For longer responses
```

**Why?** Tokens cost money! Only use what you need.

### 4. Store Conversation History

```python
# Keep track of the conversation
conversation_history = []

# Add each exchange
conversation_history.append({"role": "user", "content": "..."})
conversation_history.append({"role": "assistant", "content": "..."})
```

---

## Practice Exercises

### Exercise 1: Greeting Agent
Create an agent that:
- Greets users by name
- Remembers their name throughout the conversation
- Says goodbye when they leave

### Exercise 2: Calculator Agent
Create an agent that:
- Solves math problems
- Explains how it solved them
- Handles errors gracefully

### Exercise 3: Story Generator
Create an agent that:
- Generates short stories based on prompts
- Continues stories based on user input
- Maintains consistent characters

---

## Troubleshooting

### Problem: "API key not found"
**Solution:** Make sure you set the environment variable correctly.

### Problem: "Rate limit exceeded"
**Solution:** Wait a minute between requests or upgrade your plan.

### Problem: "Connection error"
**Solution:** Check your internet connection and API endpoint.

### Problem: Agent gives wrong answers
**Solution:** Improve your system prompt with more specific instructions.

---

## Quick Summary

**What You Learned:**
- ✅ How to get and use a Claude API key
- ✅ Basic agent structure and code
- ✅ How to have conversations with agents
- ✅ Common patterns for different tasks
- ✅ Error handling and best practices

**Key Code Structure:**
```python
1. Import anthropic
2. Create client
3. Set system prompt (agent's instructions)
4. Send messages
5. Get and use responses
```

---

## What's Next?

Now that you can create basic agents, you're ready for:

✅ **Core Principles** (Next Section)
   - Advanced prompting techniques
   - Managing complex conversations
   - Performance optimization

✅ **Practical Applications** (Later)
   - Building real-world agents
   - Integrating with tools
   - Deploying your agents

---

## Checkpoint Questions

1. What are the 4 things you need to create an agent?
2. What is the `system` parameter used for?
3. Why do we keep conversation history?
4. How would you make an agent remember the user's name?

---

**Duration:** 25 minutes
**Difficulty:** Beginner
**Prerequisites:** Introduction to Concepts

---

*Ready to level up? Move on to "Core Principles" to learn advanced techniques!*
