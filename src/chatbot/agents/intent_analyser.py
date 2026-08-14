import json
import re
from typing import Dict, Any
from chatbot.agents.base import BaseAgent

class IntentAnalyserAgent(BaseAgent):
    """
    Agent responsible for analyzing the user's intent, expanding the query,
    and extracting filters such as brand, color, and price limits.
    """
    def __init__(self, temperature: float = 0.2):
        # Initialize BaseAgent which handles ChatOllama configuration
        super().__init__(temperature=temperature)
        
        self.system_prompt = """You are an expert E-commerce Query Tokenizer and Metadata Extractor.
You must output a JSON object with exactly four fields: "original_query", "summary", "rewritten_query", and "extracted_filters".

STRICT PROCESSING RULES:
1. "summary": Clean, concise, human-readable title (2-4 words max) representing the core product type (e.g., "Winter Boots", "Laptop Sleeve").

2. "rewritten_query": This must be a raw, comma-separated English search string optimized STRICTLY for semantic/vector search. 
CRITICAL RULES FOR REWRITING:
- NO STRUCTURED FILTERS: Absolutely DO NOT include brands (e.g., "Metallica", "Nike"), colors (e.g., "red", "black"), prices/budgets (e.g., "under 100", "cheap"), sizes, or genders. These are handled by metadata.
- NO EXACT REPETITIONS: Do not repeat the same word consecutively.
- SEMANTIC & VISUAL EXPANSION: Imagine the aesthetic, style, and core nature of the user's request. Expand the query with highly descriptive, visual, and contextual attributes that define that specific vibe or product type (e.g., If the user wants a "Metallica t-shirt", infer the subculture/style and expand to: "graphic tee, rock band t-shirt, heavy metal merchandise, skull print, vintage wash, comfortable cotton apparel").
- Focus on materials, print types, style genres, and usage contexts that enhance vector similarity.

3. "extracted_filters": Extract shopping filters explicitly mentioned or strongly implied:
   - "brand": Brand or distinct entity name if mentioned (e.g., "Metallica", "Nike"). If none, set to null.
   - "color": Array of colors if mentioned (e.g., ["red"]). If none, set to null.
   - "max_price": Extract maximum financial threshold as a pure integer/number. If none, set to null.
   - "min_price": Extract minimum limit as a pure integer/number if mentioned. If none, set to null.
   - "category_taxonomy": Always set this exact field to an empty array []. DO NOT try to guess the category here.

4. Output MUST be ONLY the raw JSON object. No markdown formatting (like ```json), no conversational filler. Just raw JSON."""

    def _clean_json_structure(self, obj: Any) -> Any:
        """
        Recursively cleans keys and values in a dictionary or list,
        stripping whitespace and removing control characters from keys.
        """
        if isinstance(obj, dict):
            cleaned = {}
            for k, v in obj.items():
                k_cleaned = str(k).strip().replace('\n', '').replace('\r', '')
                cleaned[k_cleaned] = self._clean_json_structure(v)
            return cleaned
        elif isinstance(obj, list):
            return [self._clean_json_structure(x) for x in obj]
        elif isinstance(obj, str):
            return obj.strip()
        return obj

    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Analyzes the query and returns parsed intent and filters.
        """
        prompt = f"{self.system_prompt}\n\nACTUAL USER INPUT:\n\"{query}\"\n\nOutput JSON:"
        
        response = self.llm.invoke(prompt)
        raw_content = response.content.strip()
        
        # Clean potential markdown block wrappers (like ```json ... ```)
        clean_content = re.sub(r'^```json\s*|```$', '', raw_content, flags=re.MULTILINE).strip()
        
        parsed = None
        # Step 1: Try parsing directly with strict=False
        try:
            parsed = json.loads(clean_content, strict=False)
        except json.JSONDecodeError:
            # Step 2: Try auto-completing closing braces (common LLM truncation issue)
            for suffix in ["}", "}}", "}}}"]:
                try:
                    parsed = json.loads(clean_content + suffix, strict=False)
                    break
                except json.JSONDecodeError:
                    continue
            
            # Step 3: Try to find a JSON pattern using regex if direct parses and completions failed
            if parsed is None:
                match = re.search(r'\{.*\}', clean_content, re.DOTALL)
                if match:
                    try:
                        parsed = json.loads(match.group(0), strict=False)
                    except json.JSONDecodeError as re_err:
                        raise ValueError(f"LLM response JSON parsing failed. Raw response: {raw_content}. Error: {str(re_err)}")
                else:
                    raise ValueError(f"LLM response did not contain a valid JSON object. Raw response: {raw_content}")

        # Recursively clean up key whitespaces/newlines (e.g. "category_taxonomy\n" -> "category_taxonomy")
        parsed = self._clean_json_structure(parsed)

        # Ensure "analysis" is the top-level key as expected by the system structure
        if "analysis" not in parsed:
            parsed = {"analysis": parsed}
            
        # Standardize the extracted filters structure
        analysis_node = parsed["analysis"]
        if "extracted_filters" not in analysis_node:
            analysis_node["extracted_filters"] = {}
            
        filters = analysis_node["extracted_filters"]
        if "category_taxonomy" not in filters:
            filters["category_taxonomy"] = []
            
        return parsed

