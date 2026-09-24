from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
import json

@tool
def web_search_tool(query: str) -> str:
    """
    Kullanıcının sorgusuyla ilgili internette teknik bilgi ve uyumluluk araştırması yapar.
    YALNIZCA bilgi edinmek içindir. Dışarıdan ürün önermek için KULLANILAMAZ.
    """
    search = DuckDuckGoSearchResults()
    results = search.invoke(query)
    return f"İnternet Arama Sonuçları: {results}\n(Not: Sadece teknik bilgi çıkarımı için kullanın.)"
