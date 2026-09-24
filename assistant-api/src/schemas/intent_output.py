from pydantic import BaseModel, Field

class IntentOutput(BaseModel):
    """Supervisor LLM'in döneceği yapısal çıktı formatı."""
    intent: str = Field(
        description="Kullanıcının niyetine göre seçilen kategori. Mutlaka verilen listeden biri olmalı."
    )
    confidence: float = Field(
        description="Bu karara ne kadar güvendiğini gösteren 0.0 ile 1.0 arası değer."
    )
    reasoning: str = Field(
        description="Bu niyeti neden seçtiğine dair 1-2 cümlelik kısa mantık açıklaması."
    )
