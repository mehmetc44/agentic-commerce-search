from langchain_ollama import ChatOllama
from chatbot.core.config import settings
from chatbot.graph.state import ShoppingState

# Initialize LLM with settings loaded from .env
llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0.0
)

def query_analyzer(state: ShoppingState):
    query = state["user_query"]

    response = llm.invoke(
        f"""
        Analyze the following shopping-related user request.

        User request:
        {query}
        """
    )

    return {
        "analysis": response.content
    }
