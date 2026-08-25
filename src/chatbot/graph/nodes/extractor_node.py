import json
from chatbot.graph.state import ShoppingState
from chatbot.agents.extractor_agent import ExtractorAgent

extractor_agent = ExtractorAgent(temperature=0.0)

def extractor_node(state: ShoppingState):
    query = state["user_query"]
    analysis_raw = state.get("analysis", "")
    
    context_dict = {}
    if analysis_raw:
        try:
            context_dict = json.loads(analysis_raw)
        except Exception:
            context_dict = {}

    # Run Extractor Agent logic
    extract_result = extractor_agent.extract(query, context_analysis=context_dict)
    ext_data = extract_result.get("extraction", {})

    rewritten_q = ext_data.get("rewritten_query", query)
    filters = ext_data.get("extracted_filters", {})
    strategy = ext_data.get("search_strategy", "hybrid_search")
    reasoning = ext_data.get("reasoning", "")

    # Format human-readable Extractor Agent output for UI
    formatted_output = f"**🔍 Rewritten Semantic Search Query:** `{rewritten_q}`\n\n"
    formatted_output += f"**⚙️ Retrieval Strategy:** `{strategy.upper()}`\n\n"
    formatted_output += f"**🧠 Extraction Reasoning:** {reasoning}\n\n"
    formatted_output += "**📌 Extracted Filter Attributes:**\n"

    filter_items = []
    if isinstance(filters, dict):
        for k, v in filters.items():
            if v is not None and v != [] and v != {}:
                filter_items.append(f"- **{k.capitalize()}:** `{json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v}`")

    if filter_items:
        formatted_output += "\n".join(filter_items) + "\n\n"
    else:
        formatted_output += "- *No explicit SQL filters extracted (pure vector search).* \n\n"

    formatted_output += "⚡ **Database & Vector Search Execution:** Retrieval pipeline ready to query SQL/NoSQL & PgVector index."

    return {
        "response": formatted_output
    }
