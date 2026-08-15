import json
from langgraph.graph import StateGraph, START, END
from chatbot.graph.state import ShoppingState
from chatbot.graph.nodes.intent_analyzer_node import intent_analyzer_node
from chatbot.graph.nodes.conversation_node import conversation_node
from chatbot.graph.nodes.search_node import search_node

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
        # Fallback to searching if parsing fails
        intent = "product_search"
        
    if intent == "conversation":
        return "conversation"
    else:
        # Handles both product_search and product_recommendation
        return "searching"

# Define the StateGraph with the ShoppingState TypedDict
workflow = StateGraph(ShoppingState)

# Add all nodes to the workflow graph
workflow.add_node("intent_analyzer", intent_analyzer_node)
workflow.add_node("conversation", conversation_node)
workflow.add_node("searching", search_node)

# Set the flow logic
workflow.add_edge(START, "intent_analyzer")

# Route dynamically based on the intent result of the intent analyzer
workflow.add_conditional_edges(
    "intent_analyzer",
    route_intent,
    {
        "conversation": "conversation",
        "searching": "searching"
    }
)

# Connect endpoints to the END state
workflow.add_edge("conversation", END)
workflow.add_edge("searching", END)

# Compile the final agentic graph application
app_graph = workflow.compile()
