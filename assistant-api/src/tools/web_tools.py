from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """Katalogda olmayan genel bilgiler için internette arama yapar."""
    # TODO: DuckDuckGo veya Tavily entegrasyonu yapılacak
    raise NotImplementedError("Henüz implement edilmedi")
