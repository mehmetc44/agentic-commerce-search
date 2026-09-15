from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver

from chatbot.agents.base_agent import BaseAgent
from chatbot.tools.web_search import web_search_tool
from chatbot.tools.category_tools import get_closest_categories, get_category_filters
from chatbot.tools.product_tools import list_closest_products
import json

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    products: list

ORCHESTRATOR_SYSTEM_PROMPT = """Sen AgenticCommerce'in Akıllı Asistanı ve Yöneticisisin (Orchestrator).
Görevlerin:
1. Müşteriyle doğal ve samimi bir dilde iletişim kurmak.
2. Müşteri genel bir kategori istediyse ('elbise', 'ayakkabı'), onu soru yağmuruna tutma. Hemen `get_closest_categories` ile kategoriyi bul ve `list_closest_products` ile en popüler ürünleri getir. Ancak müşteri detay verdikçe (örn: 'kırmızı olsun') filtreleri daralt.
3. Müşteri bir ürün sorduğunda:
   a) Önce `get_closest_categories` ile uygun kategori ID'lerini bul.
   b) İstersen (gerekliyse) `get_category_filters` ile o kategoriye özel hangi soruları sorabileceğini öğren.
   c) Son olarak `list_closest_products` aracını tetikleyerek kesin ürünleri getir.
4. Teknik bilgi veya uyumluluk (Örn: Bu parça şu modele uyar mı?) gerektiren konularda `web_search_tool` kullan.
5. ASLA internetten bulduğun başka mağazaların ürünlerini müşteriye satmaya çalışma veya tavsiye etme. Sadece kendi araçlarından dönen sonuçları sun.
"""

# 1. Araçları Tanımla
tools = [web_search_tool, get_closest_categories, get_category_filters, list_closest_products]
tool_node = ToolNode(tools)

# 2. LLM'i Hazırla
base_agent = BaseAgent(temperature=0.2)
llm_with_tools = base_agent.llm.bind_tools(tools)

# 3. Ana Ajan Düğümü
def orchestrator_node(state: GraphState):
    messages = state["messages"]
    
    # Sistem komutunu en başa ekle (eğer daha önce eklenmemişse)
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT)] + messages
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Ürünleri state içine almak için Tool düğümünden sonra çalışan bir hook
def parse_products_node(state: GraphState):
    messages = state["messages"]
    products = state.get("products", [])
    
    # Eğer son mesaj bir ToolMessage ise ve adı list_closest_products ise, JSON'u parse et
    if messages and isinstance(messages[-1], ToolMessage):
        last_msg = messages[-1]
        if last_msg.name == "list_closest_products":
            try:
                data = json.loads(last_msg.content)
                if isinstance(data, list):
                    products = data
            except:
                pass
                
    return {"products": products}

# 4. Grafiği İnşa Et
workflow = StateGraph(GraphState)

workflow.add_node("agent", orchestrator_node)
workflow.add_node("tools", tool_node)
workflow.add_node("parse_products", parse_products_node)

workflow.add_edge(START, "agent")

# Ajan tool kullandıysa 'tools' düğümüne git, yoksa işlemi bitir (END)
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

# Araçlar çalıştıktan sonra products parse et ve ajana dön
workflow.add_edge("tools", "parse_products")
workflow.add_edge("parse_products", "agent")

memory = MemorySaver()
# Grafiği derle
compiled_graph = workflow.compile(checkpointer=memory)

# FastAPI için Sarıcı (Wrapper)
class WrapperGraph:
    def invoke(self, state: dict) -> dict:
        user_query = state.get("user_query", "")
        config = {"configurable": {"thread_id": "kullanici_123"}}
        
        result = compiled_graph.invoke({"messages": [("user", user_query)]}, config)
        
        final_message = result["messages"][-1].content
        products = result.get("products", [])
        
        return {
            "analysis": "LangGraph Çalıştı",
            "response": final_message,
            "products": products
        }

app_graph = WrapperGraph()
