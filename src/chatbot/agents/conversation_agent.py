from chatbot.agents.base_agent import BaseAgent

class ConversationAgent(BaseAgent):
    """
    Agent responsible for casual conversation, greetings, and handling general 
    chat messages that are not related to product search or compatibility.
    """
    def __init__(self, temperature: float = 0.7):
        super().__init__(temperature=temperature)
        self.system_prompt = (
            "You are a helpful and polite E-commerce Assistant. "
            "The user is just chatting or greeting you. "
            "Respond politely, concisely, and ask how you can help them with their shopping needs today."
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
