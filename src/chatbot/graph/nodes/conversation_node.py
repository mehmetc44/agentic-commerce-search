from chatbot.graph.state import ShoppingState
from chatbot.agents.conversation_agent import ConversationAgent

# Initialize the conversation agent
conversation_agent = ConversationAgent()

def conversation_node(state: ShoppingState):
    query = state["user_query"]
    
    # Generate conversational response
    response_text = conversation_agent.chat(query)
    
    return {
        "response": response_text
    }
