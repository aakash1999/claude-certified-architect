# Creating an Agent with Claude

This guide provides step-by-step directions for creating robust agents using the Anthropic Python SDK. It covers the core single-agent loop, handling built-in and custom tools, and orchestrating multi-agent systems.

## 1. Single Agent Setup (The Core Loop)

An agent is essentially a while-loop around the `client.messages.create` method, dynamically appending tool calls and results to the conversation history until Claude provides a final text answer.

### Step 1: Setup and Initialization
```python
import anthropic
import json

# The client automatically picks up ANTHROPIC_API_KEY from the environment
client = anthropic.Anthropic()
```

### Step 2: Define Tools
Define the tools Claude can use. Each tool needs a name, description, and an input schema based on JSON Schema.
```python
tools = [
    {
        "name": "lookup_order",
        "description": "Look up an order by its ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },
            "required": ["order_id"]
        }
    }
]
```

### Step 3: Tool Execution and Error Handling
Your application needs to intercept tool calls requested by Claude, run the actual code, and return the result. Use structured error categories to help Claude decide how to recover:
- **Transient**: Infrastructure issue (e.g., timeout). Claude can retry.
- **Permission**: Access denied. Escalate, do not retry.
- **Validation**: Bad input parameters. Claude should self-correct before retrying.
- **Internal**: Unexpected error. Surface to user/coordinator.

```python
def handle_tool_call(tool_name: str, tool_id: str, tool_input: dict) -> dict:
    try:
        # Run your logic here
        content = execute_tool(tool_name, tool_input)
        return {
            "type": "tool_result",
            "tool_use_id": tool_id,
            "content": content,
        }
    except ValueError as e:
        # Validation error example
        return {
            "type": "tool_result",
            "tool_use_id": tool_id,
            "is_error": True,
            "content": json.dumps({
                "errorCategory": "validation",
                "isRetryable": False,
                "description": str(e),
            }),
        }
```

### Step 4: The Agentic Loop
The heart of the agent. Maintain a conversation history and append messages continuously.
```python
def run_agent(user_message: str):
    messages = [{"role": "user", "content": user_message}]
    MAX_ITERATIONS = 50
    
    for _ in range(MAX_ITERATIONS):
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )
        
        # 1. Exit condition
        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return ""
            
        # 2. Tool usage condition
        if response.stop_reason == "tool_use":
            # Append Claude's request (role: assistant)
            messages.append({"role": "assistant", "content": response.content})
            
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_results.append(handle_tool_call(block.name, block.id, block.input))
                    
            # Append Tool Results (role: user)
            messages.append({"role": "user", "content": tool_results})

    return "Error: Agent limit reached"
```

## 2. Incorporating Inbuilt Tools

When interacting with a filesystem or coding environment, it's a common pattern to expose file operations as tools to Claude:
- **`grep`**: Search for patterns within files. (Inputs: `pattern`, `path`, `include`).
- **`glob`**: Search for file paths. (Inputs: `pattern`, `path`).
- **`read`**: Read a file's entire content. (Inputs: `file_path`).
- **`write`**: Create or overwrite a file. (Inputs: `file_path`, `content`).
- **`edit`**: Targeted string replacement. (Inputs: `file_path`, `old_string`, `new_string`).

*Fallback Pattern*: If `edit` fails (e.g., the `old_string` is not unique in the file), Claude should gracefully fallback to using `read` to load the whole file into context and then `write` to overwrite it with the updated content.

## 3. Multi-Agent Systems (Coordinator Pattern)

For complex tasks, define a Coordinator Agent that delegates to Specialized Subagents. 
The Coordinator uses a built-in `Task` tool to spawn subagents.

### The Task Tool Schema
The Task tool must be explicitly permitted. The coordinator passes an `AgentDefinition` to it.
```python
coordinator_config = {
    "model": "claude-haiku-4-5",
    "system": "You are a research coordinator. Decompose tasks and delegate to subagents.",
    "tools": [{"type": "task", "name": "Task"}],
    "allowedTools": ["Task", "compile_report"]
}

# Example Claude tool_use response emitting a Task
task_tool_call = {
    "type": "tool_use",
    "name": "Task",
    "input": {
        "description": "Environmental Researcher", 
        "prompt": "Find recent papers on wind energy...",
        "allowed_tools": ["web_search", "read_url"],
        "model": "claude-haiku-4-5"
    }
}
```

### Parallel Execution
A coordinator can drastically reduce overall execution time by dispatching tasks simultaneously. Claude can emit multiple `tool_use` blocks within the same response content array, launching multiple specialized subagents in parallel.

```python
# Coordinator firing multiple tasks in parallel
"content": [
    {"type": "tool_use", "name": "Task", "input": {"description": "Env Researcher", ...}},
    {"type": "tool_use", "name": "Task", "input": {"description": "Econ Researcher", ...}},
    {"type": "tool_use", "name": "Task", "input": {"description": "Policy Analyst", ...}}
]
```
