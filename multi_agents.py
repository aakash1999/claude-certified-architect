# ── Coordinator agent configuration ──────────────────────────────────
coordinator_config = {
    "model": "claude-haiku-4-5",      # cost-efficient for orchestration
    "system": """You are a research coordinator.
Decompose tasks and delegate to specialized subagents.
Specify research goals and quality criteria.
Do NOT provide step-by-step procedures.""",

    "tools": [
        # ── The Task tool enables subagent spawning ──────────────────
        {
            "type": "task",           # built-in Task tool type
            "name": "Task",           # must be exactly "Task" (capital T)
        },
    ],
    # ── allowedTools MUST explicitly include "Task" ───────────────────
    "allowedTools": ["Task", "compile_report"]
}

task_tool_call = {
    "type": "tool_use",
    "id":   "tu_web_search_001",
    "name": "Task",
    "input": {
        # ── AgentDefinition fields ─────────────────────────────────
        "description":   "Web Search Specialist",    # label
        "prompt": """Research goal: Find 5-8 recent papers (2022-2025)
on offshore wind energy environmental impact in the EU.
Quality criteria: peer-reviewed, include key findings,
flag conflicting conclusions. Return as structured JSON.""",

        # ── Subagent scoped to its role — NO Task tool here ──────────
        "allowed_tools": ["web_search", "read_url"],

        "model": "claude-haiku-4-5"
    }
}

coordinator_response = {
    "role": "assistant",
    "content": [
        {"type": "text", "text": "Researching in parallel across 3 domains."},

        # ── Task 1 ─────────────────────────────────────────────────────
        {"type": "tool_use", "id": "tu_env", "name": "Task",
         "input": {"description": "Environmental Researcher", ...}},

        # ── Task 2 ─────────────────────────────────────────────────────
        {"type": "tool_use", "id": "tu_econ", "name": "Task",
         "input": {"description": "Economic Data Researcher", ...}},

        # ── Task 3 ─────────────────────────────────────────────────────
        {"type": "tool_use", "id": "tu_policy", "name": "Task",
         "input": {"description": "EU Policy Analyst", ...}},
    ]
    # ↑ ALL THREE in the same content array = PARALLEL execution
    # Separate turns = sequential anti-pattern
}

