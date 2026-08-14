import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Chatbot UI",
    page_icon="💬",
    layout="centered"
)

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

st.markdown("<h1>🛍️ E-Commerce Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Local Prototype Interface (Offline Mode)</p>", unsafe_allow_html=True)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Merhaba! Ben e-ticaret asistanınız. Şu an model bağlantısı olmadan, çevrimdışı (offline) modda çalışıyorum. Size nasıl yardımcı olabilirim?"}
    ]

# Render chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input loop
if prompt := st.chat_input("Mesajınızı buraya yazın..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render a placeholder assistant response
    with st.chat_message("assistant"):
        response = f"Mesajınızı aldım: **\"{prompt}\"**\n\n*(Not: Şu an model bağlantısı devre dışı bırakılmıştır. Bu bir arayüz demo yanıtıdır.)*"
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
