from chatbot.agents.base_agent import BaseAgent
from chatbot.tools.web_search import web_search_tool
from chatbot.tools.catalog_search import catalog_search_tool
from chatbot.core.schemas.intent_analyzer import IntentAnalysis # Not used now, keeping for ref
from langgraph.prebuilt import create_react_agent

ORCHESTRATOR_SYSTEM_PROMPT = """Sen AgenticCommerce'in Akıllı Asistanı ve Yöneticisisin (Orchestrator).
Görevlerin:
1. Müşteriyle doğal ve samimi bir dilde iletişim kurmak.
2. Müşterinin isteği belirsizse veya eksikse, ona netleştirici sorular sormak (Örn: Hediye kime, bütçe ne kadar?).
3. Gerekli tüm bilgileri aldıktan sonra uygun ARAÇLARI (tools) kullanmak.
4. Teknik bilgi veya uyumluluk (Örn: Bu parça şu modele uyar mı?) gerektiren konularda `web_search_tool` kullan.
5. Ürün aramak veya fiyat/stok kontrolü yapmak için YALNIZCA `catalog_search_tool` kullan. 
6. ASLA internetten bulduğun başka mağazaların ürünlerini müşteriye satmaya çalışma veya tavsiye etme. Sadece kendi veritabanımızdan (`catalog_search_tool` ile) gelen ürünleri sun.
"""

class OrchestratorAgent(BaseAgent):
    def __init__(self, temperature: float = 0.2):
        super().__init__(temperature=temperature)
        self.tools = [web_search_tool, catalog_search_tool]
        # create_react_agent is a prebuilt LangGraph that handles tool execution loops automatically
        self.agent_executor = create_react_agent(
            self.llm, 
            self.tools, 
            prompt=ORCHESTRATOR_SYSTEM_PROMPT
        )
        
    def invoke(self, messages: list) -> dict:
        """
        messages: A list of HumanMessage/AIMessage or simple dicts like [{"role": "user", "content": "..."}]
        """
        return self.agent_executor.invoke({"messages": messages})
