from ollama import chat
class ConceptAgent:
    def __init__(self, model_name='phi3'):
        self.model_name = model_name

    def generate_concepts(self, user_prompt: str):
        base_prompt = (
            "You are a helpful assistant that suggests products. "
            "Always give exactly 5 product names only, very short (1-5 words each). "
            "Do NOT add descriptions, technical details, brands, or store names. "
            "Make them stylish, functional, and safe when applicable. "
            "Simplify the user's request if it's long or complex. "
            "For specific equipment (like 'New Holland T480 S/B'), suggest compatible products only. "
        )
        full_prompt = base_prompt + "Now: " + user_prompt
        
        stream = chat(
            model=self.model_name,
            messages=[{'role': 'user', 'content': full_prompt}],
            stream=True
        )
        
        concepts = []
        for chunk in stream:
            concepts.append(chunk['message']['content'])
        
        return concepts
