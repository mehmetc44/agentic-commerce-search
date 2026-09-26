from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgenticCommerceState(TypedDict):
    """
    LangGraph için minimal durum (state) yapısı.
    """
    user_query: str
    messages: Annotated[Sequence[BaseMessage], add_messages]
    intent: str
    supervisor_reasoning: str
    response: str
    context_products: list[dict]