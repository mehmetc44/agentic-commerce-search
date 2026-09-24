from langgraph.graph import StateGraph, START, END
from graph.state import AgenticCommerceState
from agents.supervisor import SupervisorAgent

def create_workflow() -> StateGraph:
    """
    Sistemin ana LangGraph iş akışını (workflow) oluşturur.
    Şu an için sadece Supervisor Agent tanımlı.
    """
    workflow = StateGraph(AgenticCommerceState)

    # 1. Agent'ı başlat
    supervisor = SupervisorAgent()

    # 2. Node olarak ekle (node fonksiyonu: state alır, dict döner)
    workflow.add_node("supervisor_node", supervisor.invoke)

    # 3. Kenarları (Edge) tanımla
    workflow.add_edge(START, "supervisor_node")
    workflow.add_edge("supervisor_node", END)

    return workflow.compile()

# Dışarıdan kullanılacak ana graph nesnesi
app_graph = create_workflow()
