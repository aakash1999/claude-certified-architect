system = """
You are investigating a production incident.
Start with error logs from the last 24 hours.
Based on what you find, decide your next investigation step.
Continue until you identify root cause and remediation.
Tools: read_logs, query_db, check_config, trace_request
Generate subtasks dynamically — next steps depend on findings.
"""

# Model determines the sequence from discoveries:
# Turn 1: read_logs     → finds DB timeout errors
# Turn 2: query_db      → finds an unindexed query
# Turn 3: check_config  → confirms missing index on prod
# Turn 4: end_turn      → root cause + remediation plan
#
# Sequence emerged from the work — it was NOT predictable upfront