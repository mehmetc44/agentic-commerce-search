import json
from chatbot.graph.state import ShoppingState
from chatbot.agents.recommendation_agent import RecommendationAgent

recommendation_agent = RecommendationAgent(temperature=0.2)

def recommendation_node(state: ShoppingState):
    query = state["user_query"]
    analysis_raw = state.get("analysis", "")
    
    analysis_dict = {}
    if analysis_raw:
        try:
            analysis_dict = json.loads(analysis_raw)
        except Exception:
            analysis_dict = {}
            
    # Execute recommendation agent logic
    rec_result = recommendation_agent.recommend(query, intent_analysis=analysis_dict)
    rec_data = rec_result.get("recommendation", {})
    
    action = rec_data.get("action", "search_products")
    need_summary = rec_data.get("implicit_need_summary", "")
    reasoning = rec_data.get("reasoning", "")
    search_targets = rec_data.get("search_targets", [])
    clarification_q = rec_data.get("clarification_question")

    # Format clean, human-readable response for the chat UI (in English)
    formatted_output = f"**💡 Scenario Analysis:** {need_summary}\n\n"
    formatted_output += f"**🧠 Solution Strategy & Reasoning:** {reasoning}\n\n"

    if action == "ask_clarification" and clarification_q:
        formatted_output += f"**❓ Clarification Required:** {clarification_q}\n"
    elif search_targets:
        formatted_output += "**🔍 Extractor Agent Search Targets:**\n"
        for idx, target in enumerate(search_targets, 1):
            category = target.get("category", "")
            sq = target.get("search_query", "")
            filters = target.get("filters", {})
            filter_str = f" | Filters: {json.dumps(filters, ensure_ascii=False)}" if filters else ""
            formatted_output += f"{idx}. **[{category.upper()}]** {sq}{filter_str}\n"

    return {
        "response": formatted_output
    }
