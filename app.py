import streamlit as st
import sys
import os
import json

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from chatbot.agents.query_analyzer import QueryAnalyzerAgent

# Page Configuration
st.set_page_config(
    page_title="Chatbot UI - Query Analyzer Test",
    page_icon="🔍",
    layout="centered"
)

# Cache agent initialization to prevent reloading LLM on every page refresh
@st.cache_resource
def get_query_analyzer():
    return QueryAnalyzerAgent(temperature=0.0)

try:
    analyzer = get_query_analyzer()
    offline_mode = False
except Exception as e:
    offline_mode = True
    offline_error = str(e)

# Premium Custom CSS Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@600;800&display=swap');

/* Apply global theme background and typography */
.stApp {
    background: linear-gradient(135deg, #0b0813 0%, #16122c 100%);
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

/* Gradient Header Styling */
h1 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.2rem !important;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* Premium Chat Input styling */
div[data-testid="stChatInput"] {
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    background: rgba(255, 255, 255, 0.03) !important;
    padding: 6px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

/* Modern styling for chat messages */
div[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 16px !important;
    margin-bottom: 12px !important;
    padding: 18px !important;
    transition: all 0.2s ease;
}

div[data-testid="stChatMessage"]:hover {
    border-color: rgba(99, 102, 241, 0.3) !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🔍 Query Analyzer Agent Tester</h1>", unsafe_allow_html=True)
if offline_mode:
    st.markdown(f"<p class='subtitle' style='color: #ef4444;'>Offline Mode (Error: {offline_error})</p>", unsafe_allow_html=True)
else:
    st.markdown("<p class='subtitle'>Live Ollama (Llama 3.2) Query Analysis</p>", unsafe_allow_html=True)

# Initialize message history
if "messages" not in st.session_state:
    if offline_mode:
        st.session_state.messages = [
            {"role": "assistant", "content": f"⚠️ **Ollama bağlantı hatası!** Local modelinize bağlanılamadı. Lütfen Ollama sunucunuzun açık olduğundan emin olun.\n\nHata: `{offline_error}`"}
        ]
    else:
        st.session_state.messages = [
            {"role": "assistant", "content": "Merhaba! Ben Sorgu Çözümleme Ajanı (Query Analyzer Agent). Arama sorgunuzu girin, ben de onu arka planda analiz edip filtreleri ve intent bilgisini çıkarayım."}
        ]

# Render chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input loop
if prompt := st.chat_input("Sorgulamak istediğiniz ürünü yazın (Örn: siyah su geçirmez çocuk botu, bütçe 1000 TL)..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render assistant response using the QueryAnalyzerAgent
    with st.chat_message("assistant"):
        if offline_mode:
            response = f"⚠️ Ollama sunucusuna bağlanılamadığı için sorgu analiz edilemedi.\n\nHata: `{offline_error}`"
            st.markdown(response)
        else:
            with st.spinner("Sorgu analiz ediliyor..."):
                try:
                    # Run analysis
                    analysis_result = analyzer.analyze(prompt)
                    # Pretty format the dict to JSON string
                    json_str = json.dumps(analysis_result, indent=2, ensure_ascii=False)
                    response = f"### 📊 Çözümleme Sonucu\n\n```json\n{json_str}\n```"
                except Exception as ex:
                    response = f"❌ Sorgu analiz edilirken bir hata oluştu:\n`{str(ex)}`"
                st.markdown(response)
                
    st.session_state.messages.append({"role": "assistant", "content": response})

