# Claude emits this tool call in its response
{
  "type": "tool_use",
  "name": "grep",
  "input": {
    "pattern": "process_refund",      # what to search for
    "path":    "./src",               # where to look
    "include": "*.py"                # optionally filter by extension
  }
}

# Tool returns something like:
# src/billing/refunds.py:42:   process_refund(order_id, amount)
# src/agents/support_agent.py:118:   await process_refund(order_id, ...)
# tests/test_billing.py:77:   mock_process_refund.assert_called_once()



{
  "type": "tool_use",
  "name": "glob",
  "input": {
    "pattern": "**/*.test.tsx",    # any .test.tsx file, any depth
    "path":    "./src"            # starting from here
  }
}

# Returns:
# src/components/Button.test.tsx
# src/components/Modal.test.tsx
# src/hooks/useAuth.test.tsx
# src/pages/Checkout.test.tsx



{
  "type": "tool_use",
  "name": "read",
  "input": {
    "file_path": "src/billing/refunds.py"  # exact path from Grep result
  }
}
# Returns the full file contents as a string



{
  "type": "tool_use",
  "name": "write",
  "input": {
    "file_path": "src/utils/date_formatter.py",
    "content": "from datetime import datetime\n\ndef format_iso(ts: int) -> str:\n    ..."
  }
}



{
  "type": "tool_use",
  "name": "edit",
  "input": {
    "file_path":   "src/billing/refunds.py",
    "old_string":  "def process_refund(order_id: str) -> bool:",
    "new_string":  "def process_refund(order_id: str, amount: float) -> RefundResult:"
  }
}

# Edit finds the old_string, replaces it with new_string
# Everything else in the file stays exactly as-is


# Suppose refunds.py contains this three times:
logger.info("Processing...")
logger.info("Processing...")   # same string → Edit fails!
logger.info("Processing...")

# Edit call with old_string = 'logger.info("Processing...")'
# → ERROR: old_string matches multiple locations



# Step 1: Edit fails (non-unique anchor text)
# Agent recognizes the failure in the tool result

# Step 2: Read the full file
{
  "name": "read",
  "input": { "file_path": "src/billing/refunds.py" }
}

# Step 3: Claude now has the full file in context
# It can make the targeted change in its reasoning,
# then produce the entire updated file

# Step 4: Write the updated version back
{
  "name": "write",
  "input": {
    "file_path": "src/billing/refunds.py",
    "content": "... entire updated file content ..."
  }
}