import json
from chatbot.graph.state import ShoppingState
from chatbot.agents.intent_analyser import IntentAnalyserAgent

# Initialize the Intent Analyser Agent (defaults to Llama 3.2 settings)
analyser_agent = IntentAnalyserAgent(temperature=0.0)

def query_analyzer(state: ShoppingState):
    query = state["user_query"]
    
    # Run the analysis using our dedicated agent
    analysis_result = analyser_agent.analyze(query)
    
    # Return the analysis node serialized as a JSON string to fit in state["analysis"]
    return {
        "analysis": json.dumps(analysis_result["analysis"])
    }

