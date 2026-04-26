# Claude Certified Architect — Course Project

Demo code for the **Claude Certified Architect** course (Episodes 01–05). Most files are teaching artifacts, not a production app: some are runnable scripts, others are illustrative snippets that won't execute as-is.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

The SDK reads `ANTHROPIC_API_KEY` from the environment — never hardcode keys.

## File map

**Runnable scripts** (have `if __name__ == "__main__"` or top-level calls):
- `api_check.py` — smoke test that the API key works
- `agent.py` — the canonical single-agent loop with structured error categories (Ep 01)
- `capstone_project.py` — multi-agent demo connecting Ep 01–05
- `fork_session.py` — `client.beta.sessions.fork` example

**Illustrative snippets** (don't run standalone — they're embedded code samples for teaching):
- `inbuilt_tools.py`, `multi_agents.py`, `tool_choice.py`, `tool_misrouting.py`
- `developer_productivity.py`, `dynamic_decomposition.py`, `subagent_context.py`
- `prompt_chaining` (no `.py` extension on purpose)

When editing snippet files, preserve their pedagogical shape — comments and ordering matter more than executability.

## Conventions

1. **Model pinning**: all examples use `claude-haiku-4-5` deliberately (cost + speed for learners). Don't bump to Sonnet/Opus without asking.
2. **Error categories**: tool errors must use the four-category schema from `agent.py` — `transient`, `permission`, `validation`, `internal`. New tools should follow the same pattern.
3. **Agentic loop exit**: `stop_reason == "end_turn"` is the only valid primary exit. `MAX_ITERATIONS` is a safety valve, not a stop condition.
4. **No real secrets**: mock data only (see `FAKE_DB`, `FAKE_ORDERS` in `capstone_project.py`).

## Reference

Deeper SDK guide (single-agent loop, inbuilt tools, coordinator pattern): `docs/agent-guide.md`.
