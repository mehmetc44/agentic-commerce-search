import streamlit as st
import sys
import os
import json

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from chatbot.graph import app_graph

# Page Configuration
st.set_page_config(
    page_title="Chatbot UI - Intent Analyzer Routing Test",
    page_icon="🎯",
    layout="centered"
)

# Custom Styling
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

st.markdown("<h1>🎯 Intent Analyzer Agent Router</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>E-Commerce Intent Classification & Routing Flow</p>", unsafe_allow_html=True)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Merhaba! Ben Intent Analyzer yönlendirme asistanınız. Arama, tavsiye veya sohbet mesajlarınızı yazabilirsiniz."
        }
    ]

# Render chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input loop
if prompt := st.chat_input("Mesajınızı yazın (Örn: 'I am looking for a black case for iPhone 14' veya 'Merhaba nasılsın?')..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render assistant response by invoking the compiled LangGraph workflow
    with st.chat_message("assistant"):
        with st.spinner("Niyet analiz ediliyor ve yönlendiriliyor (LangGraph)..."):
            try:
                # 1. Initialize State
                initial_state = {
                    "user_query": prompt,
                    "analysis": "",
                    "response": ""
                }
                
                # 2. Invoke Graph
                final_state = app_graph.invoke(initial_state)
                
                # 3. Retrieve results
                analysis_str = final_state.get("analysis", "")
                response_text = final_state.get("response", "Yanıt oluşturulamadı.")
                
                # 4. Display Intent Analysis JSON schema
                try:
                    analysis_dict = json.loads(analysis_str)
                    st.markdown("### 🎯 Niyet Analiz Sonucu (Intent Analyzer)")
                    st.json(analysis_dict)
                except Exception:
                    st.markdown("⚠️ Niyet analizi çözümlenemedi.")
                
                # 5. Display Node's final response
                st.markdown("### 💬 Yönlendirilen Düğüm Yanıtı")
                st.markdown(response_text)
                
                # Combine both for persistent message history
                full_display = ""
                if analysis_str:
                    full_display += f"**🎯 Niyet Analiz Sonucu:**\n```json\n{json.dumps(json.loads(analysis_str), indent=2, ensure_ascii=False)}\n```\n\n"
                full_display += f"**💬 Yönlendirilen Düğüm Yanıtı:**\n{response_text}"
                response = full_display
                
            except Exception as ex:
                response = f"❌ İş akışı yürütülürken hata oluştu:\n`{str(ex)}`"
                st.markdown(response)
                
    st.session_state.messages.append({"role": "assistant", "content": response})
