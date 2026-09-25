from agents.base_agent import BaseAgent
from langgraph.prebuilt import create_react_agent
from tools.catalog_tools import get_closest_categories, list_closest_products, get_category_filters
from graph.state import AgenticCommerceState

class SearchAgent(BaseAgent):
    """
    Ürün arama işlemini (ReAct Pattern) yürüten ajan.
    Katalog API araçlarını kullanarak kullanıcının talebine en uygun ürünü bulur.
    """
    def __init__(self):
        super().__init__("search_agent")
        self.tools = [get_closest_categories, list_closest_products, get_category_filters]
        
        # LangChain'in hazır ReAct fonksiyonu LLM ve toolları birbirine bağlar
        self.react_agent = create_react_agent(self.llm, tools=self.tools)

    def invoke(self, state: AgenticCommerceState) -> dict:
        """LangGraph node metodu"""
        # Ajanı çalıştır (Mesaj geçmişini de verebiliriz)
        response = self.react_agent.invoke({"messages": [("user", state["user_query"])]})
        
        # Son mesajı response olarak alıyoruz
        final_answer = response["messages"][-1].content
        return {"response": final_answer}
