from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ShoppingState(TypedDict):
    user_query: str
    analysis: str
    response: str