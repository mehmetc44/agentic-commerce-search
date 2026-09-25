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

class ResponseBuilderNode(BaseAgent):
    """Sistemdeki tüm ajan/node cevaplarını derleyip son, şık ve derli toplu bir Markdown cevabına dönüştüren düğüm."""
    def __init__(self):
        super().__init__("response_builder")
        
    def invoke(self, state: AgenticCommerceState) -> dict:
        query = state["user_query"]
        # Önceki ajanın ürettiği taslak/ham cevap
        draft_response = state.get("response", "")
        intent = state.get("intent", "bilinmiyor")
        
        prompt = (
            f"Kullanıcı talebi: '{query}'\n"
            f"Tespit Edilen Niyet: {intent}\n\n"
            f"Sistemden gelen ham cevap verisi:\n{draft_response}\n\n"
            "Görevin:\n"
            "Bu ham veriyi incele ve kullanıcıya, son derece kibar, profesyonel, "
            "iyi formatlanmış (gerekirse Markdown, liste veya tablo) bir asistan cevabı olarak sun. "
            "Bilgiyi değiştirme veya yeni bilgi ekleme, sadece harika bir sunum yap."
        )
        
        final_response = self.llm.invoke(prompt)
        return {"response": final_response.content}
