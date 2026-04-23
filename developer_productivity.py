# Agent task: "Understand how refunds are processed in this codebase"

# Turn 1: Find the entry point
grep(pattern="def process_refund", path="./src")
# → Found: src/billing/refunds.py:15

# Turn 2: Read that file to understand the implementation
read(file_path="src/billing/refunds.py")
# → Reveals it calls validate_customer() from auth module

# Turn 3: Trace that dependency
grep(pattern="def validate_customer", path="./src")
# → Found: src/auth/customer_validator.py:8

# Turn 4: Read only the files we actually need
read(file_path="src/auth/customer_validator.py")
# → Now we understand the full flow: refund → validate → auth

# Total files loaded: 2 (not 30)
# Context window: efficient
# Understanding: deep and targeted



## Phase 1: Discovery — What files exist?

# Glob: Find all Python files in the orders module
glob(pattern="src/orders/**/*.py")
# → returns list of 12 files

# Grep: Find the main order processing entry point
grep(pattern="class OrderProcessor", path="./src/orders")
# → src/orders/processor.py:1

## Phase 2: Understanding — Read the key files

read(file_path="src/orders/processor.py")
# → Shows it uses STATUS_CODES dict, calls notify_customer()

# Trace the dependency
grep(pattern="STATUS_CODES", path="./src/orders")
# → src/orders/constants.py:5

read(file_path="src/orders/constants.py")
# → Reveals legacy numeric status codes (1,2,3) not descriptive strings

## Phase 3: Action — Generate the new endpoint boilerplate

write(
  file_path="src/orders/routes/order_status.py",
  content="""
from src.orders.constants import STATUS_CODES
from src.orders.processor import OrderProcessor

class OrderStatusEndpoint:
    # Generated endpoint using discovered constants and patterns
    ...
"""
)

## Phase 4: Fix a specific legacy issue Claude found

# Edit the constants file to add descriptive string aliases
edit(
  file_path="src/orders/constants.py",
  old_string="STATUS_CODES = {1: 'pending', 2: 'processing', 3: 'complete'}",
  new_string="STATUS_CODES = {1: 'pending', 2: 'processing', 3: 'complete', 'PENDING': 1, 'PROCESSING': 2, 'COMPLETE': 3}"
)