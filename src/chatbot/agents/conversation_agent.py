from chatbot.agents.base_agent import BaseAgent

class ConversationAgent(BaseAgent):
    """
    Agent responsible for casual conversation, greetings, and handling general 
    chat messages that are not related to product search or compatibility.
    """
    def __init__(self, temperature: float = 0.7):
        super().__init__(temperature=temperature)
        self.system_prompt = (
            "Yardımsever ve kibar bir E-ticaret Asistanısınız. "
            "Kullanıcı sizinle sadece sohbet ediyor veya selamlaşıyor. "
            "Kibar, kısa ve net bir şekilde yanıt verin ve bugün alışveriş ihtiyaçları konusunda onlara nasıl yardımcı olabileceğinizi sorun."
        )

    def chat(self, user_message: str) -> str:
        """
        Generates a conversational response to the user's message.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        response = self.llm.invoke(messages)
        return response.content.strip()
