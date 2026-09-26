from agents.base_agent import BaseAgent
from graph.state import AgenticCommerceState
import requests
from core.config import settings

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
        context_products = state.get("context_products", [])
        
        if not context_products:
            return {"response": "Lütfen yorumlarını öğrenmek istediğiniz ürünü seçin (Ürün kartı üzerindeki 'AI'a Sor' butonunu kullanabilirsiniz)."}
            
        product = context_products[0]
        product_id = product.get("id")
        product_name = product.get("name", "Seçili Ürün")
        
        # Yorumları catalog-api'den çek
        reviews_text = "Bu ürün için henüz yorum bulunmamaktadır."
        try:
            resp = requests.get(f"{settings.CATALOG_API_URL}/api/v1/reviews/product/{product_id}", timeout=5)
            if resp.status_code == 200:
                reviews_data = resp.json()
                if reviews_data:
                    # YAML'da belirtilen sayı kadar (veya örneğin ilk 20) yorumu al
                    max_reviews = self.config.get("max_reviews_to_process", 20)
                    reviews_list = reviews_data[:max_reviews]
                    
                    formatted_reviews = []
                    for i, r in enumerate(reviews_list, 1):
                        rating = r.get("rating", "?")
                        review_text_content = r.get("review_text", "")
                        if review_text_content:
                            formatted_reviews.append(f"{i}. [Puan: {rating}/5] {review_text_content}")
                    
                    if formatted_reviews:
                        reviews_text = "\n".join(formatted_reviews)
        except Exception as e:
            print(f"Yorumlar çekilirken hata: {e}")
            reviews_text = "Yorumlar çekilirken sistemsel bir hata oluştu."
            
        prompt = (
            f"Kullanıcının Sorusu: '{query}'\n\n"
            f"Ürün: {product_name}\n\n"
            f"Müşteri Yorumları:\n{reviews_text}\n\n"
            "Görevin: Yukarıdaki müşteri yorumlarını dikkatlice analiz et.\n"
            "1. Yorumlara göre genel müşteri memnuniyetini özetle (olumlu mu olumsuz mu?).\n"
            "2. Ürünün en çok övülen yönlerini (Artılar) sırala.\n"
            "3. En çok şikayet edilen yönlerini (Eksiler) sırala.\n"
            "4. Varsa, kullanıcının sorduğu özel soruya bu yorumlardan yola çıkarak doğrudan cevap ver."
        )
        
        response = self.llm.invoke(prompt)
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
