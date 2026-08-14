import json
import re
from typing import Dict, Any
from app.infrastructure.llm.ollama_client import OllamaClient
from app.core.config import settings

class QueryTokenizerService:
    """
    Stage 1: Kullanıcı sorgularını tokenize eden, genişleten ve 
    metadata filtrelerini söken ana mimari servis katmanı.
    """
    def __init__(self, ollama_client: OllamaClient):
        self.client = ollama_client
        # Vektör arama uzayını kirletmesini istemediğimiz para birimi gürültüleri için regex
        self.noise_pattern = re.compile(r'\b(tl|lira|buck|bucks|budget|price|prices)\b', re.IGNORECASE)
        self.instructions = settings.SYSTEM_INSTRUCTIONS

    def _clean_rewritten_query_noise(self, query_str: str) -> str:
        """Sorgu genişletme dizesindeki (rewritten_query) finansal birim kalıntılarını temizler."""
        if not query_str:
            return ""
        tokens = query_str.split(',')
        cleaned_tokens = []
        for token in tokens:
            cleaned_token = self.noise_pattern.sub('', token).strip()
            # Eğer temizleme sonrası token sadece sayılardan ibaret kalmadıysa veya boş değilse ekle
            if cleaned_token and not cleaned_token.replace('-', '').isdigit():
                cleaned_tokens.append(cleaned_token)
        return ", ".join(cleaned_tokens)

    def tokenize_user_query(self, raw_query: str) -> Dict[str, Any]:
        """Ham sorguyu işler, LLM'e gönderir, doğrular, temizler ve python dict yapısı döner."""
        full_prompt = f"{self.instructions}\n\nACTUAL USER INPUT:\n\" {raw_query} \"\n\nOutput JSON:"
        
        # LLM'den ham yanıtı al
        raw_response = self.client.post_generation(prompt=full_prompt)
        
        # Olası markdown çapaklarını temizle
        raw_response = re.sub(r'^```json\s*|```$', '', raw_response, flags=re.MULTILINE).strip()
        
        # JSON Parse
        try:
            parsed_data = json.loads(raw_response)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned an invalid JSON schema. Raw string: {raw_response}. Error: {str(e)}")

        # Yapısal Düğüm Kontrolü
        analysis_node = parsed_data.get("analysis")
        if not analysis_node:
            analysis_node = parsed_data
            parsed_data = {"analysis": analysis_node}

        # 🛡️ POST-PROCESSING: Vector Search için 'rewritten_query' gürültü temizliği
        if "rewritten_query" in analysis_node:
            raw_rewritten = analysis_node["rewritten_query"]
            analysis_node["rewritten_query"] = self._clean_rewritten_query_noise(raw_rewritten)

        # Güvence: category_taxonomy her koşulda boş liste kalmalı
        filters = analysis_node.get("extracted_filters", {})
        filters["category_taxonomy"] = []
        analysis_node["extracted_filters"] = filters

        return parsed_data
