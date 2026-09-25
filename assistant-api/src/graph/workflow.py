from langgraph.graph import StateGraph, START, END
from graph.state import AgenticCommerceState
from agents.supervisor import SupervisorAgent
from agents.search_agent import SearchAgent
from agents.simple_nodes import ClarificationNode, CompareNode, ReviewNode, GeneralChatNode

def route_by_intent(state: AgenticCommerceState) -> str:
    """Supervisor'ın belirlediği intent'e göre gidilecek node'u seçer."""
    intent = state.get("intent", "general_chat")
    
    routes = {
        "product_search": "search_node",
        "product_compare": "compare_node",
        "product_review": "review_node",
        "clarification_needed": "clarification_node",
        "general_chat": "chat_node"
    }
    
    return routes.get(intent, "chat_node")

class AgenticCommerceWorkflow:
    """
    Sistemin ana iş akışını (LangGraph) yöneten sınıf.
    """
    def __init__(self):
        # 1. Bağımlılıkları başlat
        self.supervisor = SupervisorAgent()
        self.search_agent = SearchAgent()
        self.clarification = ClarificationNode()
        self.compare = CompareNode()
        self.review = ReviewNode()
        self.chat = GeneralChatNode()
        
        # 2. Graph'ı inşa et
        self.app_graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgenticCommerceState)

        # Node'ları ekle
        workflow.add_node("supervisor_node", self.supervisor.invoke)
        workflow.add_node("search_node", self.search_agent.invoke)
        workflow.add_node("clarification_node", self.clarification.invoke)
        workflow.add_node("compare_node", self.compare.invoke)
        workflow.add_node("review_node", self.review.invoke)
        workflow.add_node("chat_node", self.chat.invoke)

        # Entry point -> Supervisor
        workflow.add_edge(START, "supervisor_node")

        # Supervisor -> Conditional Routing
        workflow.add_conditional_edges("supervisor_node", route_by_intent)

        # Tüm alt node'lar bittiğinde akışı sonlandır
        workflow.add_edge("search_node", END)
        workflow.add_edge("clarification_node", END)
        workflow.add_edge("compare_node", END)
        workflow.add_edge("review_node", END)
        workflow.add_edge("chat_node", END)

        return workflow.compile()

    def execute(self, user_query: str) -> dict:
        """
        Sistemi dışarıdan tetiklemek için kullanılacak yardımcı metot.
        State'i hazırlar ve graph'ı çalıştırıp sonucu döner.
        """
        initial_state = {
            "user_query": user_query,
            "messages": [],
            "intent": "",
            "supervisor_reasoning": "",
            "response": ""
        }
        
        # Graph'ı senkron olarak çalıştır
        result = self.app_graph.invoke(initial_state)
        return result
