import anthropic

client = anthropic.Anthropic()

# ── Imagine we have a baseline session with full codebase analysis ──
baseline_session_id = "baseline-arch-analysis-001"

# ── Fork it to explore two different refactoring approaches ──
fork_a = client.beta.sessions.fork(
    session_id=baseline_session_id,
    system_prompt_addition="Explore refactoring approach A: extract service layer pattern."
)

fork_b = client.beta.sessions.fork(
    session_id=baseline_session_id,
    system_prompt_addition="Explore refactoring approach B: CQRS pattern."
)

# ── Run both forks independently ──
# fork_a gets the same baseline context but explores approach A
# fork_b gets the same baseline context but explores approach B
# Neither contaminates the other



# ── Instead of resuming a stale session, inject findings as structured summary ──

prior_findings_summary = """
PRIOR ANALYSIS SUMMARY (from 2025-03-13):
- Architecture: monolith, Django 4.2, PostgreSQL 14
- Key coupling points: auth and billing share the User model directly
- Identified debt: payment_service.py has 3 untested code paths
- Recommended next steps: extract billing into separate bounded context

NOTE: This summary is from 2 days ago. The codebase has since been updated.
Please treat these as hypotheses to validate, not established facts.
Re-explore the current file structure before acting on these findings.
"""

# ── Start a fresh session and inject the summary ──
messages = [
    {
        "role": "user",
        "content": prior_findings_summary + "\n\nNow please begin fresh analysis of the current codebase state."
    }
]