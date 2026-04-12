# ─────────────────────────────────────────────────────────────
# STEP 1: Install and import
# pip install anthropic
# ─────────────────────────────────────────────────────────────
import anthropic
import json
import os

# ─────────────────────────────────────────────────────────────
# STEP 2: Create the client
# Reads ANTHROPIC_API_KEY from environment automatically.
# Never hardcode the key here.
# ─────────────────────────────────────────────────────────────
client = anthropic.Anthropic()


# ─────────────────────────────────────────────────────────────
# STEP 3: Define your tools
#
# Each tool has three required fields:
#   name        — what Claude calls it in tool_use blocks
#   description — how Claude decides WHEN to use this tool
#                 (more on this in Episode 05)
#   input_schema — JSON Schema defining the tool's parameters
# ─────────────────────────────────────────────────────────────
tools = [
    {
        "name": "lookup_order",
        "description": (
            "Look up an order by its order ID. "
            "Returns current status, estimated delivery date, and carrier name. "
            "Use this when the customer asks where their order is or when it will arrive."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The numeric order ID (e.g. '4821')"
                }
            },
            "required": ["order_id"]
        }
    }
]


# ─────────────────────────────────────────────────────────────
# STEP 4: Implement your tool functions
#
# Claude CANNOT call these functions directly.
# Claude REQUESTS a tool call → your code runs it → you return the result.
# This is a mock implementation. In production, this would query a database.
# ─────────────────────────────────────────────────────────────
def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Run a tool and return its result as a JSON string."""
    if tool_name == "lookup_order":
        order_id = tool_input.get("order_id", "")
        # Mock database lookup
        mock_orders = {
            "4821": {"status": "shipped",    "eta": "March 30", "carrier": "FedEx"},
            "9910": {"status": "processing", "eta": "April 2",  "carrier": "UPS"},
            "0042": {"status": "delivered",  "eta": "March 25", "carrier": "DHL"},
        }
        if order_id in mock_orders:
            return json.dumps(mock_orders[order_id])
        else:
            return json.dumps({"error": f"Order {order_id} not found"})

    # Unknown tool — return an error result (never raise an exception here)
    return json.dumps({"error": f"Unknown tool: {tool_name}"})


# ─────────────────────────────────────────────────────────────
# STEP 5: The agentic loop
# ─────────────────────────────────────────────────────────────
def run_agent(user_message: str) -> str:
    """
    Run the agentic loop until Claude produces a final answer.
    Returns the final text response.
    """

    # Start with just the user's message.
    # The messages array will grow on every loop iteration.
    messages = [
        {"role": "user", "content": user_message}
    ]

    # Safety valve — not the primary stop condition.
    MAX_ITERATIONS = 50
    iteration = 0

    while iteration < MAX_ITERATIONS:
        iteration += 1

        # ── API CALL ──────────────────────────────────────────
        # Send the current messages + available tools to Claude.
        # Claude returns a response with a stop_reason.
        # ─────────────────────────────────────────────────────
        response = client.messages.create(
            model="claude-haiku-4-5",   # Fast and cheap — good for learning
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # ── EXIT CONDITION ────────────────────────────────────
        # stop_reason == "end_turn" means Claude is done.
        # Extract the text and return it to the caller.
        # This is the ONLY valid primary loop exit.
        # ─────────────────────────────────────────────────────
        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return ""  # end_turn with no text (rare but possible)

        # ── TOOL USE ──────────────────────────────────────────
        # stop_reason == "tool_use" means Claude wants to call tools.
        # We must: execute the tools, then append both messages to history.
        # ─────────────────────────────────────────────────────
        if response.stop_reason == "tool_use":

            # APPEND 1: The assistant's message (role: "assistant")
            # This saves Claude's tool request(s) into conversation history.
            # You MUST append this before the tool results.
            messages.append({
                "role": "assistant",
                "content": response.content   # contains the tool_use blocks
            })

            # Execute each tool Claude requested
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  → Calling tool: {block.name}({block.input})")
                    result = execute_tool(block.name, block.input)
                    print(f"  ← Result: {result}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,  # ← MUST match the id in the assistant msg
                        "content": result
                    })

            # APPEND 2: The tool results (role: "user")
            # "user" role because this is data COMING INTO Claude from your code.
            # Even though no human typed this, it uses the user role.
            messages.append({
                "role": "user",
                "content": tool_results
            })

            # Loop continues — goes back to the top of the while loop.
            # Claude will now see the tool results and decide what to do next.

    # Safety valve triggered — this should never happen in normal operation
    return "Error: agent did not complete within the iteration limit"


# ─────────────────────────────────────────────────────────────
# STEP 6: Run it
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Running agent...")
    answer = run_agent("Where is my order #4821?")
    print(f"\nFinal answer: {answer}")