# Chapter 3: Model Context Protocol (MCP) Servers

## What is MCP?

The Model Context Protocol (MCP) is an open standard that enables AI agents to connect with external data sources and tools. Think of it as a universal adapter that lets your AI agent interact with databases, APIs, file systems, and more.

## Why MCP Matters

Traditional AI agents are limited to text generation. MCP extends their capabilities to:
- Query databases
- Search the web
- Read and write files
- Perform calculations
- Access external APIs
- Run system commands

## MCP Architecture

```
┌──────────────┐
│   AI Agent   │
│   (Claude)   │
└──────┬───────┘
       │
       │ MCP Protocol
       │
┌──────▼───────┐         ┌─────────────┐
│ MCP Client   ├────────►│  Database   │
└──────┬───────┘         └─────────────┘
       │
       ├────────────────►┌─────────────┐
       │                 │  File System│
       │                 └─────────────┘
       │
       └────────────────►┌─────────────┐
                         │  Web API    │
                         └─────────────┘
```

## Core MCP Concepts

### 1. Resources

Resources are data sources that agents can read from:
- **Files**: Local or remote documents
- **Database Tables**: Structured data
- **API Endpoints**: External services
- **System Information**: OS details, environment variables

### 2. Tools

Tools are actions that agents can perform:
- **read_file**: Access file contents
- **execute_query**: Run database queries
- **web_search**: Search the internet
- **calculate**: Perform mathematical operations

### 3. Prompts

Reusable templates for common agent tasks:
- Code review workflows
- Data analysis patterns
- Report generation templates

## Installing MCP

```bash
# Python
pip install mcp anthropic-mcp

# Node.js
npm install @modelcontextprotocol/sdk
```

## Building Your First MCP Server

### Simple File System Server (Python)

```python
from mcp import Server, Tool
from pathlib import Path

# Create MCP server
server = Server("filesystem-server")

@server.tool()
async def read_file(path: str) -> str:
    """Read contents of a file"""
    try:
        content = Path(path).read_text()
        return content
    except FileNotFoundError:
        return f"Error: File '{path}' not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"

@server.tool()
async def list_directory(path: str = ".") -> list[str]:
    """List files in a directory"""
    try:
        files = [f.name for f in Path(path).iterdir()]
        return files
    except Exception as e:
        return [f"Error: {str(e)}"]

# Start server
if __name__ == "__main__":
    server.run()
```

### Using the MCP Server with Claude

```python
import anthropic
from anthropic_mcp import MCPClient

# Initialize MCP client
mcp_client = MCPClient("filesystem-server")

# Initialize Claude client with MCP
client = anthropic.Anthropic(api_key="your-key")

# Agent can now use file system tools
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=mcp_client.get_tools(),
    messages=[{
        "role": "user",
        "content": "What files are in my current directory?"
    }]
)

# Process tool calls
if response.stop_reason == "tool_use":
    tool_call = response.content[1]  # Get tool call block
    tool_name = tool_call.name
    tool_input = tool_call.input

    # Execute tool via MCP
    result = await mcp_client.call_tool(tool_name, tool_input)

    # Send result back to Claude
    final_response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "What files are in my current directory?"},
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": result
                }
            ]}
        ]
    )

    print(final_response.content[0].text)
```

## Common MCP Server Types

### 1. Database Server

```python
from mcp import Server
import sqlite3

server = Server("database-server")

@server.tool()
async def execute_query(query: str) -> dict:
    """Execute SQL query"""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return {
                "columns": columns,
                "rows": rows,
                "count": len(rows)
            }
        else:
            conn.commit()
            return {
                "affected_rows": cursor.rowcount,
                "message": "Query executed successfully"
            }
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
```

### 2. Web Search Server

```python
import httpx
from mcp import Server

server = Server("web-search-server")

@server.tool()
async def search_web(query: str, num_results: int = 5) -> list[dict]:
    """Search the web using DuckDuckGo"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json"}
        )
        data = response.json()

        results = []
        for item in data.get("RelatedTopics", [])[:num_results]:
            if "Text" in item:
                results.append({
                    "title": item.get("Text", ""),
                    "url": item.get("FirstURL", ""),
                    "snippet": item.get("Text", "")[:200]
                })

        return results
```

### 3. Calculator Server

```python
from mcp import Server
import math

server = Server("calculator-server")

@server.tool()
async def calculate(expression: str) -> float:
    """
    Evaluate mathematical expressions safely
    Supports: +, -, *, /, **, sqrt, sin, cos, etc.
    """
    # Create safe namespace with math functions
    safe_dict = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
    }

    try:
        # Evaluate expression in safe context
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return result
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")
```

## Tool Use Workflow

1. **User asks a question** that requires tool use
2. **Claude identifies** which tool to use
3. **Agent calls the tool** via MCP
4. **Tool returns results**
5. **Claude synthesizes** the answer

Example:

```
User: "What's the square root of the number of files in my home directory?"

Step 1: Claude decides to use list_directory tool
Step 2: MCP calls list_directory("/home/user")
Step 3: MCP returns: ["file1.txt", "file2.txt", "file3.txt"]
Step 4: Claude decides to use calculate tool
Step 5: MCP calls calculate("sqrt(3)")
Step 6: MCP returns: 1.732...
Step 7: Claude responds: "There are 3 files, and the square root is approximately 1.73."
```

## Best Practices

### 1. Tool Descriptions

Write clear, specific tool descriptions:

```python
@server.tool()
async def search_products(
    query: str,
    category: str = None,
    min_price: float = None,
    max_price: float = None
) -> list[dict]:
    """
    Search for products in the inventory.

    Args:
        query: Search term (searches name and description)
        category: Filter by category (e.g., 'electronics', 'clothing')
        min_price: Minimum price in USD
        max_price: Maximum price in USD

    Returns:
        List of matching products with id, name, price, and category
    """
    # Implementation...
```

### 2. Error Handling

Always handle errors gracefully:

```python
@server.tool()
async def safe_tool(param: str) -> dict:
    try:
        result = perform_operation(param)
        return {"success": True, "data": result}
    except ValueError as e:
        return {"success": False, "error": f"Invalid input: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
```

### 3. Security

Validate and sanitize inputs:

```python
@server.tool()
async def execute_query(query: str) -> dict:
    # Prevent SQL injection
    if any(keyword in query.upper() for keyword in ["DROP", "DELETE", "UPDATE"]):
        return {"error": "Modifying queries not allowed"}

    # Only allow SELECT
    if not query.strip().upper().startswith("SELECT"):
        return {"error": "Only SELECT queries allowed"}

    # Execute safely...
```

## Testing MCP Servers

```python
import pytest
from your_server import read_file

@pytest.mark.asyncio
async def test_read_file_success():
    result = await read_file("test.txt")
    assert "Error" not in result
    assert len(result) > 0

@pytest.mark.asyncio
async def test_read_file_not_found():
    result = await read_file("nonexistent.txt")
    assert "not found" in result.lower()
```

## MCP Configuration

Configure MCP servers in your agent:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["filesystem_server.py"]
    },
    "database": {
      "command": "python",
      "args": ["database_server.py"],
      "env": {
        "DB_PATH": "/path/to/database.db"
      }
    },
    "web-search": {
      "command": "node",
      "args": ["web-search-server.js"]
    }
  }
}
```

## Practical Exercise

Build a multi-tool agent that can:
1. Search for information
2. Perform calculations
3. Store results in a database

```python
# Agent with multiple MCP servers
mcp_filesystem = MCPClient("filesystem-server")
mcp_calculator = MCPClient("calculator-server")
mcp_database = MCPClient("database-server")

# Combine all tools
all_tools = (
    mcp_filesystem.get_tools() +
    mcp_calculator.get_tools() +
    mcp_database.get_tools()
)

# Now agent can use all capabilities
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    tools=all_tools,
    messages=[{
        "role": "user",
        "content": "Calculate the total size of all Python files and save it to the database"
    }]
)
```

## Next Steps

In Chapter 4 (Premium), we'll build reusable Agent Skills that combine MCP tools into higher-level capabilities. You'll learn:
- Skill composition patterns
- State management
- Multi-step workflows
- Error recovery strategies

---

**Estimated Reading Time**: 25 minutes
**Hands-On Exercise**: Build an MCP server that exposes your system's environment variables and create an agent that can query them.
