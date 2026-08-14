import json
from langgraph.graph import StateGraph, START, END
from chatbot.graph.state import ShoppingState
from chatbot.graph.nodes.query_analyzer_node import query_analyzer
from chatbot.graph.nodes.conversation_node import conversation_node
from chatbot.graph.nodes.search_node import search_node

def route_intent(state: ShoppingState):
    """
    Conditional routing function. Extracts the classified intent from the 
    query analysis state and directs the graph flow accordingly.
    """
    try:
        # Load the query analyzer's JSON output
        analysis = json.loads(state["analysis"])
        intent = analysis.get("intent", "")
    except Exception:
        # Fallback to searching if parsing fails
        intent = "searching"
        
    if intent == "conversation":
        return "conversation"
    else:
        return "searching"

# Define the StateGraph with the ShoppingState TypedDict
workflow = StateGraph(ShoppingState)

# Add all nodes to the workflow graph
workflow.add_node("query_analyzer", query_analyzer)
workflow.add_node("conversation", conversation_node)
workflow.add_node("searching", search_node)

# Set the flow logic
workflow.add_edge(START, "query_analyzer")

# Route dynamically based on the intent result of the query analyzer
workflow.add_conditional_edges(
    "query_analyzer",
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
