# These three tools will confuse Claude constantly
tools = [
  {
    "name": "search_web",
    "description": "Search for information"
  },
  {
    "name": "search_documents",
    "description": "Search documents for information"
  },
  {
    "name": "analyze_content",
    "description": "Analyze and extract information from content"
  }
]

# Result: Claude picks whichever it hits first, or
# alternates randomly between search_web and search_documents



tools = [
  {
    "name": "search_web",
    "description": """
      Query live web pages via search engine. Use for current events,
      recent publications, URLs not yet in the document corpus.
      Input: query string. Returns ranked URLs + snippets.
      Do NOT use for documents already loaded into the research corpus.
    """
  },
  {
    "name": "search_documents",
    "description": """
      Full-text search across the pre-loaded research corpus (PDFs,
      reports, cached articles). Use ONLY for documents already ingested.
      Faster and more precise than web search for known sources.
      Input: query string + optional doc_id filter.
      Do NOT use to find new sources — use search_web for that.
    """
  },
  {
    "name": "analyze_content",
    "description": """
      Deep analysis of a specific piece of content already retrieved.
      Extracts key claims, identifies contradictions, assesses credibility.
      Input: content (string), analysis_type (claims|contradictions|summary).
      Use AFTER search_web or search_documents — not as a search tool itself.
    """
  }
]

SYSTEM_PROMPT = "You are a customer support assistant, your goal is first-contract resolution of returns and refunds" \
"" \
"Tool Use Sequence:" \
"1. Always call get cuystoner first " \
"2. call lookuop_order to lookup the orders"