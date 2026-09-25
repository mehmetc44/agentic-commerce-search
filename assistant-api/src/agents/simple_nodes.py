from agents.base_agent import BaseAgent
from graph.state import AgenticCommerceState

class ClarificationNode(BaseAgent):
    """Eksik veya muğlak sorguları netleştirmek için soru soran düğüm."""
    def __init__(self):
        super().__init__("clarification_node")
        
    def invoke(self, state: AgenticCommerceState) -> dict:
        query = state["user_query"]
        prompt = f"Kullanıcının şu talebi çok muğlak: '{query}'. Lütfen bütçe, marka veya renk gibi detayları öğrenmek için nazik ve kısa tek bir soru sor."
        
        response = self.llm.invoke(prompt)
        return {"response": response.content}

class CompareNode(BaseAgent):
    """İki veya daha fazla ürünü karşılaştıran düğüm."""
    def __init__(self):
        super().__init__("compare_node")
        
    def invoke(self, state: AgenticCommerceState) -> dict:
        query = state["user_query"]
        response = self.llm.invoke(f"Şu ürünleri karşılaştır ve özelliklerini tablo yap: {query}")
        return {"response": response.content}

class ReviewNode(BaseAgent):
    """Ürün yorumlarını çeken ve özetleyen düğüm."""
    def __init__(self):
        super().__init__("review_node")
        
    def invoke(self, state: AgenticCommerceState) -> dict:
        query = state["user_query"]
        response = self.llm.invoke(f"Şu ürünün yorumlarını özetle ve genel duygu analizini yap: {query}")
        return {"response": response.content}

class GeneralChatNode(BaseAgent):
    """Sıradan sohbetlere (selamlama vb.) cevap veren düğüm."""
    def __init__(self):
        super().__init__("general_chat")
        
    def invoke(self, state: AgenticCommerceState) -> dict:
        query = state["user_query"]
        response = self.llm.invoke(f"Sen e-ticaret asistanısın. Kullanıcıya şu mesaj için samimi, kısa bir cevap ver: '{query}'")
        return {"response": response.content}
