from ollama import chat

class JsonFormatterAgent:
    def __init__(self, model_name='flan-t5-small'):
        self.model_name = model_name

    def format_to_json(self, concepts: str, metadata: dict) -> dict:
        """
        LLM kullanarak konseptleri ve kullanıcı metadata'sını
        JSON formatına dönüştürür.
        """
        # Prompt oluştur
        base_prompt = (
            "You are a helpful assistant that converts product concepts "
            "and user preferences into a clean JSON format. "
            "Use the following rules:\n"
            "1. Validate query: set is_query_valid True/False.\n"
            "2. Include metadata_filter for SQL querying.\n"
            "3. List concepts in expanded_semantic_queries.\n"
            "Input concepts:\n"
        )
        full_prompt = base_prompt + concepts + "\nMetadata:\n" + str(metadata)

        # LLM çağrısı
        stream = chat(
            model=self.model_name,
            messages=[{'role': 'user', 'content': full_prompt}],
            stream=True
        )

        # Stream'i birleştir
        json_text = ""
        for chunk in stream:
            json_text += chunk['message']['content']

        # JSON string'ini dict'e çevir (hata yakalama eklemek iyi olur)
        import json
        try:
            json_data = json.loads(json_text)
        except json.JSONDecodeError:
            # fallback: temel JSON oluştur
            json_data = {
                "is_query_valid": True,
                "metadata_filter": "stock > 0 AND category='gift'",
                "expanded_semantic_queries": concepts.split("\n")
            }

        return json_data