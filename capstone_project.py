"""
multi_agent_demo.py
====================
Claude Certified Architect — Episodes 01 to 05 Connector Demo

What this covers (exam-relevant):
  Ep 01 → Agentic loop: stop_reason, tool_use, messages array
  Ep 02 → Coordinator pattern: task decomposition, subagent invocation
  Ep 03 → Structured context passing: findings as objects, not prose

Cost: ~5–10 API calls total, all using claude-haiku-4-5
      Expect < $0.01 USD to run the whole demo.

Setup:
  pip install anthropic
  export ANTHROPIC_API_KEY="sk-ant-..."
  python multi_agent_demo.py
"""

import anthropic
import json
from datetime import datetime

client = anthropic.Anthropic()
MODEL  = "claude-haiku-4-5"

# ─────────────────────────────────────────────
# FAKE TOOLS  (no real API calls needed)
# These simulate what real tools would return.
# ─────────────────────────────────────────────

FAKE_DB = {
    "C001": {"name": "Alice", "email": "alice@example.com", "plan": "pro"},
    "C002": {"name": "Bob",   "email": "bob@example.com",   "plan": "free"},
}

# Raw DB-style records: status codes, Unix timestamps, cents.
# These are intentionally "unfriendly" so our PostToolUse hook has work to do.
FAKE_ORDERS = {
    "O100": {
        "customer_id":  "C001",
        "items":        ["Annual Plan"],
        "amount_cents": 9900,
        "status":       3,            # 3 = Delivered
        "ordered_at":   1740009600,   # Unix ts → Feb 20, 2025
    },
    "O101": {
        "customer_id":  "C002",
        "items":        ["Monthly Plan"],
        "amount_cents": 900,
        "status":       5,            # 5 = Refunded
        "ordered_at":   1738886400,   # Unix ts → Feb 07, 2025
    },
    "O102": {
        "customer_id":  "C001",
        "items":        ["Enterprise Plan (annual)"],
        "amount_cents": 75000,        # $750 → triggers PreToolUse block
        "status":       3,            # 3 = Delivered
        "ordered_at":   1740614400,   # Unix ts → Feb 27, 2025
    },
}

# Mutable session state shared across subagents within one coordinator run.
# The prerequisite gate reads this; the verification PostToolUse hook writes it.
session = {"customer_verified": False, "customer_id": None}

def get_customer(customer_id: str) -> dict:
    customer = FAKE_DB.get(customer_id)
    if customer:
        return {"found": True, "customer_id": customer_id, **customer}
    return {"found": False, "error": f"No customer with id {customer_id}"}

def lookup_order(order_id: str) -> dict:
    order = FAKE_ORDERS.get(order_id)
    if order:
        # Return RAW fields (id, status code, Unix ts, cents).
        # The PostToolUse hook will normalize these before the model sees them.
        return {"found": True, "id": order_id, **order}
    return {"found": False, "error": f"No order with id {order_id}"}

def process_refund(order_id: str, amount: float) -> dict:
    order = FAKE_ORDERS.get(order_id)
    if not order:
        return {"success": False, "error": "Order not found"}
    if order["status"] == 5:  # 5 = Refunded (raw status code)
        return {"success": False, "error": "Order already refunded"}
    return {"success": True, "refund_id": f"REF-{order_id}", "amount": amount}

# Map tool names → functions
TOOL_REGISTRY = {
    "get_customer":  get_customer,
    "lookup_order":  lookup_order,
    "process_refund": process_refund,
}

# ─────────────────────────────────────────────
# PRE-TOOL-USE HOOK
# Runs BEFORE a tool executes. Can block the call outright (policy gate).
# Use it for guardrails: spend limits, PII checks, destructive-action review.
# ─────────────────────────────────────────────

def prerequisite_gate(tool_name, tool_params):
    """PreToolUse: block refund/lookup until the customer has been verified."""
    if tool_name in ("process_refund", "lookup_order"):
        if not session["customer_verified"]:
            return {
                "allowed":       False,
                "reason":        "Call get_customer first to verify identity.",
                "required_tool": "get_customer",
            }
    return {"allowed": True}

def enforce_refund_policy(tool_name, tool_params):
    """PreToolUse: block refunds above the $500 agent limit."""
    if tool_name != "process_refund":
        return {"allowed": True}   # pass through — only gate refunds

    amount = tool_params.get("amount", 0)   # our schema uses USD floats

    if amount > 500:
        return {
            "allowed":         False,
            "reason":          f"Refund ${amount:.2f} exceeds $500 agent limit.",
            "action_required": "escalate_to_human",
            "escalation_tier": "senior_support",
        }

    return {"allowed": True}

# Registry of pre-tool-use hooks. First hook that returns allowed=False wins.
# Order matters: check prerequisites BEFORE business-rule checks.
PRE_TOOL_HOOKS = [prerequisite_gate, enforce_refund_policy]

def apply_pre_tool_hooks(tool_name, tool_params):
    """Run hooks in order; stop at the first block. Returns the decision dict."""
    for hook in PRE_TOOL_HOOKS:
        decision = hook(tool_name, tool_params)
        if not decision.get("allowed", True):
            return decision
    return {"allowed": True}

# ─────────────────────────────────────────────
# POST-TOOL-USE HOOK
# Runs AFTER a tool returns, BEFORE the result is sent back to the model.
# Use it to reshape raw data into a model-friendly form (and save tokens).
# ─────────────────────────────────────────────

def normalize_order_result(tool_name, raw_result):
    if tool_name != "lookup_order":
        return raw_result   # pass through — only normalize lookup_order
    if not raw_result.get("found"):
        return raw_result   # don't touch error shapes

    # Map status codes → human-readable strings
    status_map = {
        1: "Processing",  2: "Shipped",
        3: "Delivered",   4: "Return Initiated",  5: "Refunded",
    }

    # Convert Unix timestamp → readable date
    order_date = datetime.utcfromtimestamp(
        raw_result["ordered_at"]
    ).strftime("%B %d, %Y")   # "February 20, 2025"

    # Convert cents → display currency
    amount = f"${raw_result['amount_cents'] / 100:.2f}"

    return {
        "order_id":    raw_result["id"],
        "customer_id": raw_result["customer_id"],
        "status":      status_map.get(raw_result["status"], "Unknown"),
        "order_date":  order_date,   # ← readable date
        "amount":      amount,       # ← formatted currency
        "items":       raw_result["items"],
    }

def update_verification_state(tool_name, raw_result):
    """PostToolUse: flip the verification flag ONLY if get_customer succeeded.

    This must live in PostToolUse — not PreToolUse — because only after the
    tool runs do we know whether the customer actually exists.
    """
    if tool_name == "get_customer" and raw_result.get("found"):
        session["customer_verified"] = True
        session["customer_id"]       = raw_result.get("customer_id")
        print(f"  [HOOK] Verified session for {session['customer_id']}")
    return raw_result   # pass the result through unchanged

# Registry of post-tool-use hooks. Add more hooks here as the system grows.
POST_TOOL_HOOKS = [normalize_order_result, update_verification_state]

def apply_post_tool_hooks(tool_name, raw_result):
    """Run every registered hook in order. Each hook sees the previous output."""
    result = raw_result
    for hook in POST_TOOL_HOOKS:
        result = hook(tool_name, result)
    return result

# ─────────────────────────────────────────────
# TOOL SCHEMAS
# These descriptions are the ONLY thing the model reads when deciding
# which tool to call and in what order. Four levers:
#   1. WHAT it does        — so the model picks the right tool
#   2. WHEN to call it     — ordering & prerequisites
#   3. WHAT NOT to use it for — prevents common mix-ups
#   4. WHAT it returns     — so the model knows what data it'll get back
# ─────────────────────────────────────────────

TOOLS = [
    {
        "name": "get_customer",
        "description": (
            "Retrieve a verified customer profile by customer ID. "
            "Returns name, email, plan tier, and account standing. "
            "ALWAYS call this FIRST before any other tool — the system "
            "requires customer verification before order lookups or refunds. "
            "Do NOT use this for order details; use lookup_order instead."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Customer ID (format: C followed by digits, e.g. C001)",
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "lookup_order",
        "description": (
            "Fetch full order details by order ID. "
            "Returns item list, amount, order date, delivery status, and "
            "the linked customer_id. "
            "REQUIRES: get_customer must have been called first to verify identity. "
            "Do NOT use this to issue refunds; use process_refund for that."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Order ID (format: O followed by digits, e.g. O100)",
                }
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "process_refund",
        "description": (
            "Issue a monetary refund for a specific order. "
            "REQUIRES: call get_customer first to verify identity, then "
            "call lookup_order to confirm the order exists and belongs to "
            "that customer. Only call this AFTER both checks pass. "
            "Do NOT guess the amount — use the exact amount from lookup_order."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID to refund (must match a prior lookup_order call)",
                },
                "amount": {
                    "type": "number",
                    "description": "Refund amount in USD — must match the order total from lookup_order",
                }
            },
            "required": ["order_id", "amount"]
        }
    }
]


# ─────────────────────────────────────────────
# EP 01 — AGENTIC LOOP
# The core loop: send → check stop_reason → run tools → repeat
# ─────────────────────────────────────────────

def run_agentic_loop(system_prompt: str, user_message: str, tools: list) -> str:
    """
    Ep 01 concept: the agentic loop.
    Keeps running until stop_reason == "end_turn".
    Correctly appends assistant message BEFORE tool results each round.
    """
    messages = [{"role": "user", "content": user_message}]
    print(f"\n  [LOOP] Starting. User: {user_message[:60]}...")

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system_prompt,
            tools=tools,
            messages=messages
        )

        print(f"  [LOOP] stop_reason = {response.stop_reason}")

        # ── Ep 01: stop_reason == "end_turn" → we're done ──
        if response.stop_reason == "end_turn":
            final_text = next(
                (b.text for b in response.content if hasattr(b, "text")), ""
            )
            print(f"  [LOOP] Done. Response: {final_text[:80]}...")
            return final_text

        # ── Ep 01: stop_reason == "tool_use" → run tools ──
        if response.stop_reason == "tool_use":

            # Step 1: append the FULL assistant message first (Ep 01 rule)
            messages.append({"role": "assistant", "content": response.content})

            # Step 2: collect tool results
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":

                    # ── PreToolUse hook ───────────────────────────────
                    # Policy gate: decide whether the tool is allowed to run
                    # AT ALL. If blocked, we never touch the tool — we just
                    # hand the model a structured "blocked" result so it can
                    # explain the situation or escalate.
                    decision = apply_pre_tool_hooks(block.name, block.input)
                    if not decision["allowed"]:
                        print(f"  [HOOK] BLOCKED {block.name}({block.input})")
                        print(f"  [HOOK] Reason: {decision['reason']}")
                        tool_results.append({
                            "type":        "tool_result",
                            "tool_use_id": block.id,
                            "is_error":    True,
                            "content":     json.dumps(decision),
                        })
                        continue   # skip the real tool call

                    print(f"  [TOOL] Calling {block.name}({block.input})")
                    raw_result = TOOL_REGISTRY[block.name](**block.input)
                    print(f"  [TOOL] Raw result:        {raw_result}")

                    # ── PostToolUse hook ──────────────────────────────
                    # Reshape raw data into a model-friendly form BEFORE
                    # the model ever sees it. Deterministic work belongs
                    # in code, not in the LLM.
                    result = apply_post_tool_hooks(block.name, raw_result)
                    if result is not raw_result:
                        print(f"  [HOOK] Normalized result: {result}")

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": block.id,       # must match exactly (Ep 01)
                        "content":     json.dumps(result)
                    })

            # Step 3: append tool results as a user message
            messages.append({"role": "user", "content": tool_results})
            # Loop continues → next iteration sends full history


# ─────────────────────────────────────────────
# EP 02 — COORDINATOR PATTERN
# The coordinator decomposes the task and delegates to subagents.
# Each subagent gets only what the coordinator explicitly passes.
# ─────────────────────────────────────────────

def run_subagent(role: str, task_prompt: str, tools: list) -> dict:
    """
    Ep 02 concept: subagent invocation.
    The subagent is just another agentic loop — but with a focused role
    and only the context the coordinator chose to give it.
    Returns a structured result (not prose) for Ep 03 context passing.
    """
    print(f"\n  ── Subagent [{role}] starting ──")
    job_desc = task_prompt.split('Task:')[-1].split('\n')[0].strip() if 'Task:' in task_prompt else 'complete your assigned task'
    system_prompt = f"""You are the {role} subagent in a customer support system.
Your job: {job_desc}
Be concise. Return factual results only. Do not make up data."""
    
    handoff_prompt = "Before escalating, output a structured handoff"
    escalate_params = {}

    result_text = run_agentic_loop(system_prompt, task_prompt, tools)

    # Ep 03: wrap result as a structured finding object (not raw prose)
    return {
        "subagent_role": role,
        "task":          task_prompt[:100],
        "result":        result_text,
        "status":        "complete"
    }


def coordinator(customer_id: str, order_id: str) -> str:
    """
    Ep 02 concept: coordinator decomposition.
    Coordinator breaks the request into subtasks and delegates.
    Each subagent gets ONLY the context needed for its role.

    Ep 03 concept: structured context passing.
    Findings from subagent 1 are passed to subagent 2 as a typed object,
    not as a free-form prose summary.
    """
    print("\n" + "="*60)
    print("COORDINATOR: Decomposing task")
    print("="*60)

    # Reset session state at the start of every coordinator run so each
    # case starts unverified. The prerequisite_gate will block refund/lookup
    # until the Customer Verifier subagent successfully runs get_customer.
    session["customer_verified"] = False
    session["customer_id"]       = None

    # ── Subtask 1: verify the customer (Subagent 1) ──
    # Only gets customer_id — nothing else. Context isolation.
    verification_task = f"""Task: Look up customer {customer_id} and confirm they exist.
Return their name and plan tier."""

    verification_finding = run_subagent(
        role="Customer Verifier",
        task_prompt=verification_task,
        tools=[TOOLS[0]]  # only get_customer
    )

    # ── Ep 03: pass structured finding to next subagent ──
    # Not "here's what the last agent found" as prose.
    # A typed dict with explicit fields.
    print("\n  [COORDINATOR] Passing structured finding to next subagent:")
    print(f"  {json.dumps(verification_finding, indent=2)}")

    # ── Subtask 2: process the refund (Subagent 2) ──
    # Gets the verification finding explicitly — context must be passed
    refund_task = f"""Task: Process a refund for order {order_id}.

PRIOR VERIFICATION (from Customer Verifier subagent):
{json.dumps(verification_finding, indent=2)}

Steps:
1. Look up the order
2. Confirm it belongs to customer {customer_id}
3. If confirmed, process the refund for the full order amount"""

    refund_finding = run_subagent(
        role="Refund Processor",
        task_prompt=refund_task,
        tools=[TOOLS[1], TOOLS[2]]  # lookup_order + process_refund
    )

    # ── Coordinator aggregates results (Ep 02: result aggregation) ──
    print("\n" + "="*60)
    print("COORDINATOR: Aggregating results")
    print("="*60)

    final_summary = f"""
Customer support case resolved.

Verification: {verification_finding['result']}
Refund:       {refund_finding['result']}
"""
    print(final_summary)
    return final_summary


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║  Claude Certified Architect — Episodes 01-03 Demo            ║
║  Ep01: Agentic loop  |  Ep02: Coordinator  |  Ep03: Context  ║
╚══════════════════════════════════════════════════════════════╝

Scenario: Customer C001 wants a refund for order O100.
The coordinator will:
  1. Spawn a Customer Verifier subagent  (Ep02: decomposition)
  2. Pass its structured finding forward  (Ep03: context passing)
  3. Spawn a Refund Processor subagent   (Ep02: delegation)
  4. Aggregate the results               (Ep02: aggregation)

Each subagent runs its own agentic loop  (Ep01: stop_reason)
""")

    coordinator(customer_id="C001", order_id="O102")

    print("\n" + "─"*60)
    print("Try changing customer_id to 'C999' to see error handling.")
    print("Try order_id to 'O101' to see 'already refunded' case.")
    print("Try order_id to 'O102' (with C001) to see the PreToolUse BLOCK.")