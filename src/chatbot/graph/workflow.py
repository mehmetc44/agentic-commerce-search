from chatbot.agents.orchestrator_agent import OrchestratorAgent

# We instantiate the Orchestrator which internally uses a LangGraph React Agent
orchestrator = OrchestratorAgent(temperature=0.2)

class WrapperGraph:
    """
    A simple wrapper to maintain compatibility with the existing
    app_graph.invoke({"user_query": "..."}) interface in app.py and ui.py
    """
    def invoke(self, state: dict) -> dict:
        user_query = state.get("user_query", "")
        
        # Convert to LangChain messages format
        messages = [{"role": "user", "content": user_query}]
        
        # Invoke the React Agent graph
        result = orchestrator.invoke(messages)
        
        # Extract the final AI response string
        final_message = result["messages"][-1].content
        
        # For debugging, we can dump the tool calls or intermediate steps into 'analysis'
        # But for now, we just return the final response
        return {
            "analysis": "Orchestrator Agent handled the request directly.",
            "response": final_message
        }

# Export the compatible wrapper as app_graph
app_graph = WrapperGraph()
