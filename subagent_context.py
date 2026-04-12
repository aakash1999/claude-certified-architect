research_findings = [
    {
        "finding": "Claude's tool_use stop_reason requires the full assistant message to be appended before tool results.",
        "source_url": "https://docs.anthropic.com/agents/tool-use",
        "source_title": "Anthropic Tool Use Documentation",
        "page_number": None,
        "retrieved_at": "2025-03-15T09:12:00Z",
        "confidence": "high"
    },
    {
        "finding": "Using an iteration cap as a primary stop condition is an anti-pattern.",
        "source_url": "https://docs.anthropic.com/agents/loops",
        "source_title": "Agentic Loop Best Practices",
        "page_number": None,
        "retrieved_at": "2025-03-15T09:14:00Z",
        "confidence": "high"
    }
]

# ── Build the synthesis prompt with full context ──
synthesis_prompt = f"""
You are a synthesis agent. Your task is to produce a structured research report.

FINDINGS TO SYNTHESIZE:
{json.dumps(research_findings, indent=2)}

Requirements:
- Every claim in the report MUST cite its source_url
- Preserve the retrieved_at date for temporal accuracy
- Flag any conflicting findings with both sources annotated
- Output format: JSON with keys: summary, claims[], conflicts[]
"""

# ── Pass to subagent via Task tool ──
task_call = {
    "type": "tool_use",
    "name": "Task",
    "input": {
        "description": "Synthesize research findings into structured report",
        "prompt": synthesis_prompt
    }
}


# ── Every synthesis step must output claim-source pairs ──

intermediate_output = {
    "claims": [
        {
            "claim_id": "c001",
            "text": "Subagents do not inherit coordinator conversation history.",
            "source_id": "src_001",       # links back to source object
            "confidence": "high"
        },
        {
            "claim_id": "c002",
            "text": "Parallel subagents require multiple Task calls in one coordinator response.",
            "source_id": "src_002",
            "confidence": "high"
        }
    ],
    "sources": [
        {
            "source_id": "src_001",
            "url": "https://docs.anthropic.com/multi-agent",
            "title": "Multi-Agent Architecture Guide",
            "retrieved_at": "2025-03-15T09:12:00Z"
        },
        {
            "source_id": "src_002",
            "url": "https://docs.anthropic.com/task-tool",
            "title": "Task Tool Reference",
            "retrieved_at": "2025-03-15T09:14:00Z"
        }
    ],
    "conflicts": []  # if two sources say different things, both go here
}

# ── When passing to the next agent, pass the WHOLE object ──
# Never extract just "claims" and drop "sources"
# The next agent needs both to produce accurate output
    

# ── When two sources conflict, add to conflicts array ──
conflict = {
    "conflict_id": "conf_001",
    "topic": "parallel subagent invocation",
    "claim_a": {
        "text": "Multiple Task calls in one response run in parallel.",
        "source_id": "src_002"
    },
    "claim_b": {
        "text": "Task calls are always sequential regardless of placement.",
        "source_id": "src_003"
    },
    "resolution": "unresolved"  # coordinator must decide
}

# ── Best practice: inform resumed session about changes ──
resume_context = """
Resuming from previous analysis session.

CHANGES SINCE LAST SESSION:
- auth/middleware.py has been modified (new rate limiting added)
- requirements.txt updated (added redis==5.0.1)
- The TODO in payment_service.py line 142 has NOT been addressed yet

Please re-analyze only the changed files and continue from your prior findings.
"""