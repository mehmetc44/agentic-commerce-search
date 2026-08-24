import json
from langgraph.graph import StateGraph, START, END
from chatbot.graph.state import ShoppingState
from chatbot.graph.nodes.intent_analyzer_node import intent_analyzer_node
from chatbot.graph.nodes.conversation_node import conversation_node
from chatbot.graph.nodes.recommendation_node import recommendation_node
from chatbot.graph.nodes.extractor_node import extractor_node

def route_intent(state: ShoppingState):
    """
    Conditional routing function. Extracts the classified intent from the 
    intent analysis state and directs the graph flow accordingly.
    """
    try:
        # Load the intent analyzer's JSON output
        analysis = json.loads(state["analysis"])
        intent = analysis.get("intent", "")
    except Exception:
        # Fallback to direct extraction/search if parsing fails
        intent = "product_search"
        
    if intent == "conversation":
        return "conversation"
    elif intent == "product_recommendation":
        return "recommendation"
    else:
        # Direct Clear Query -> Extractor Agent
        return "extractor"

# Define the StateGraph with the ShoppingState TypedDict
workflow = StateGraph(ShoppingState)

# Add all nodes to the workflow graph
workflow.add_node("intent_analyzer", intent_analyzer_node)
workflow.add_node("conversation", conversation_node)
workflow.add_node("recommendation", recommendation_node)
workflow.add_node("extractor", extractor_node)

# Set the entry flow logic
workflow.add_edge(START, "intent_analyzer")

# Route dynamically based on the intent result of the intent analyzer
workflow.add_conditional_edges(
    "intent_analyzer",
    route_intent,
    {
        "conversation": "conversation",
        "recommendation": "recommendation",
        "extractor": "extractor"
    }
)

# Connect endpoints to the END state
workflow.add_edge("conversation", END)
workflow.add_edge("recommendation", END)
workflow.add_edge("extractor", END)

# Compile the final agentic graph application
app_graph = workflow.compile()
