{
  "invoice_number": {
    "value": "INV-2024-0891",
    "confidence": 0.97,        // ✅ High — route automatically
    "source_region": "top-right header"
  },
  "total_amount": {
    "value": "$4,280.00",
    "confidence": 0.91,        // ✅ High — route automatically
    "source_region": "bottom table row 12"
  },
  "vendor_address": {
    "value": "14 Main St, Austin TX",
    "confidence": 0.63,        // 🔴 Below threshold — flag for human
    "source_region": "handwritten section"
  }
}