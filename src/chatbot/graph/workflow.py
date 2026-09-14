from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from chatbot.agents.base_agent import BaseAgent
from chatbot.tools.web_search import web_search_tool
from chatbot.tools.catalog_search import catalog_search_tool
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver



ORCHESTRATOR_SYSTEM_PROMPT = """Sen AgenticCommerce'in Akıllı Asistanı ve Yöneticisisin (Orchestrator).
Görevlerin:
1. Müşteriyle doğal ve samimi bir dilde iletişim kurmak.
2. Müşterinin isteği belirsizse veya eksikse, ona netleştirici sorular sormak (Örn: Hediye kime, bütçe ne kadar?).
3. Gerekli tüm bilgileri aldıktan sonra uygun ARAÇLARI (tools) kullanmak.
4. Teknik bilgi veya uyumluluk (Örn: Bu parça şu modele uyar mı?) gerektiren konularda `web_search_tool` kullan.
5. Ürün aramak veya fiyat/stok kontrolü yapmak için YALNIZCA `catalog_search_tool` kullan. 
6. ASLA internetten bulduğun başka mağazaların ürünlerini müşteriye satmaya çalışma veya tavsiye etme. Sadece kendi veritabanımızdan (`catalog_search_tool` ile) gelen ürünleri sun.
"""

# 1. Araçları Tanımla (Define Tools)
tools = [web_search_tool, catalog_search_tool]
tool_node = ToolNode(tools)

# 2. LLM'i Hazırla (Prepare LLM and bind tools)
base_agent = BaseAgent(temperature=0.2)
llm_with_tools = base_agent.llm.bind_tools(tools)

# 3. Ana Ajan Düğümü (Main Agent Node)
def orchestrator_node(state: MessagesState):
    messages = state["messages"]
    
    # Sistem komutunu en başa ekle (eğer daha önce eklenmemişse)
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT)] + messages
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 4. Grafiği İnşa Et (Build the StateGraph)
workflow = StateGraph(MessagesState)

workflow.add_node("agent", orchestrator_node)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

# Eğer ajan tool kullanmaya karar verdiyse 'tools' düğümüne git, yoksa işlemi bitir (END)
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

# Araçlar çalıştıktan sonra sonuçları yorumlaması için tekrar ajana dön
workflow.add_edge("tools", "agent")

memory = MemorySaver()
# Grafiği derle
compiled_graph = workflow.compile(checkpointer=memory)

# Eski app.py yapısına ({"user_query": "..."}) uyumlu olması için basit bir sarıcı
class WrapperGraph:
    def invoke(self, state: dict) -> dict:
        user_query = state.get("user_query", "")
        config = {"configurable": {"thread_id": "kullanici_123"}}
        # Derlenmiş LangGraph'ı çalıştır
        result = compiled_graph.invoke({"messages": [("user", user_query)]}, config)
       
        # Son AI mesajını al
        final_message = result["messages"][-1].content
        
        return {
            "analysis": "LangGraph StateGraph Başarıyla Çalıştı.",
            "response": final_message
        }

app_graph = WrapperGraph()
