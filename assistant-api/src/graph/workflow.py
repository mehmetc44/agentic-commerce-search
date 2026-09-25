from langgraph.graph import StateGraph, START, END
from graph.state import AgenticCommerceState
from agents.supervisor import SupervisorAgent

class AgenticCommerceWorkflow:
    """
    Sistemin ana iş akışını (LangGraph) yöneten sınıf.
    Bağımlılıkları (Agent'ları) başlatır, düğümleri (node) bağlar ve execution işlemlerini yönetir.
    """

    def __init__(self):
        # 1. Bağımlılıkları (Agent'ları) başlat
        self.supervisor = SupervisorAgent()
        
        # 2. Graph'ı inşa et ve derle
        self.app_graph = self._build_graph()

    def _build_graph(self):
        """Graph yapısını (Node'lar ve Edge'ler) kurar."""
        workflow = StateGraph(AgenticCommerceState)

        # Node'ları ekle
        workflow.add_node("supervisor_node", self.supervisor.invoke)

        # Temel Edge'leri kur (Şimdilik çok basit)
        workflow.add_edge(START, "supervisor_node")
        workflow.add_edge("supervisor_node", END)

        # Graph'ı derle (Compile) ve geri dön
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
