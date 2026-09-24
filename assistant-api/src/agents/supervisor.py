from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from agents.base_agent import BaseAgent
from graph.state import AgenticCommerceState
from prompts.supervisor_prompt import SUPERVISOR_SYSTEM_PROMPT
from schemas.intent_output import IntentOutput

class SupervisorAgent(BaseAgent):
    """
    Kullanıcı mesajını analiz edip doğru Agent'a yönlendiren (Router) node.
    """

    def __init__(self):
        # agent_config.yaml içindeki "supervisor" ayarlarını kullanır
        super().__init__(config_key="supervisor")
        
        # YAML'dan gelen geçerli niyet listesi
        self.valid_intents = self.config.get("intents", [])
        
        # LLM çıktısını Pydantic nesnesine zorlar (JSON mode / Function calling)
        self.structured_llm = self.llm.with_structured_output(IntentOutput)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SUPERVISOR_SYSTEM_PROMPT),
            ("user", "{input}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def invoke(self, state: AgenticCommerceState) -> dict:
        """
        LangGraph node metodu. State'i alır, intent belirler ve döndürür.
        """
        user_input = state.get("user_query", "")
        
        # Eğer geçmiş mesajlar varsa onları da analiz için verebiliriz ama
        # şu an basitçe son sorguyu veriyoruz.
        
        result: IntentOutput = self.chain.invoke({
            "input": user_input,
            "intents_list": ", ".join(self.valid_intents)
        })
        
        # LangGraph için partial state döneriz, mevcut state'i günceller
        return {
            "intent": result.intent,
            "supervisor_reasoning": result.reasoning
        }
