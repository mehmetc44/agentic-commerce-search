document.addEventListener("DOMContentLoaded", () => {
    const chatInput = document.getElementById("chatInput");
    const chatSendBtn = document.getElementById("chatSendBtn");
    const chatMessages = document.getElementById("chatMessages");
    const searchInput = document.getElementById("searchInput");

    // Yardımcı: Mesaj Ekleme
    function addMessage(text, isUser = false) {
        if (!text.trim()) return;
        
        const msgDiv = document.createElement("div");
        msgDiv.className = "d-flex mb-3 " + (isUser ? "justify-content-end" : "");
        
        const innerDiv = document.createElement("div");
        innerDiv.className = isUser 
            ? "bg-light text-dark p-2 rounded shadow-sm border" 
            : "bg-primary text-white p-2 rounded shadow-sm";
        
        // Chat baloncuğu yuvarlaklık ayarı
        innerDiv.style.maxWidth = "80%";
        innerDiv.style.borderRadius = isUser ? "15px 15px 0 15px" : "15px 15px 15px 0";
        innerDiv.innerText = text;
        
        msgDiv.appendChild(innerDiv);
        chatMessages.appendChild(msgDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Chat'ten Mesaj Gönderme
    function handleChatSend() {
        const text = chatInput.value.trim();
        if (text) {
            addMessage(text, true); // Kullanıcı mesajı
            chatInput.value = "";
            
            // İşlevsiz bot cevabı (demo amaçlı)
            setTimeout(() => {
                addMessage("Şu an geliştirilme aşamasındayım, maalesef mesajınıza yanıt veremiyorum.");
            }, 1000);
        }
    }

    if (chatSendBtn) {
        chatSendBtn.addEventListener("click", handleChatSend);
    }

    if (chatInput) {
        chatInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") handleChatSend();
        });
    }

    // Arama Çubuğu (Üst Kısım) Entegrasyonu
    if (searchInput) {
        searchInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                const query = searchInput.value.trim();
                if (query) {
                    // Paneli Aç
                    const aiPanelEl = document.getElementById("aiPanel");
                    const aiPanel = bootstrap.Offcanvas.getOrCreateInstance(aiPanelEl);
                    aiPanel.show();
                    
                    // Arama sorgusunu chat'e aktar
                    addMessage(query, true);
                    searchInput.value = "";
                    
                    // İşlevsiz cevap
                    setTimeout(() => {
                        addMessage(`"${query}" araması için henüz sonuç getiremiyorum.`);
                    }, 1000);
                }
            }
        });
    }
});

// Küresel arama butonu işlevi (Eğer index.html'den çağrılıyorsa)
function search() {
    const searchInput = document.getElementById("searchInput");
    if (searchInput && searchInput.value.trim()) {
        const query = searchInput.value.trim();
        const aiPanelEl = document.getElementById("aiPanel");
        const aiPanel = bootstrap.Offcanvas.getOrCreateInstance(aiPanelEl);
        aiPanel.show();
        
        const chatMessages = document.getElementById("chatMessages");
        
        const msgDiv = document.createElement("div");
        msgDiv.className = "d-flex mb-3 justify-content-end";
        const innerDiv = document.createElement("div");
        innerDiv.className = "bg-light text-dark p-2 rounded shadow-sm border";
        innerDiv.style.maxWidth = "80%";
        innerDiv.style.borderRadius = "15px 15px 0 15px";
        innerDiv.innerText = query;
        msgDiv.appendChild(innerDiv);
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        searchInput.value = "";
        
        setTimeout(() => {
            const botDiv = document.createElement("div");
            botDiv.className = "d-flex mb-3";
            const botInnerDiv = document.createElement("div");
            botInnerDiv.className = "bg-primary text-white p-2 rounded shadow-sm";
            botInnerDiv.style.maxWidth = "80%";
            botInnerDiv.style.borderRadius = "15px 15px 15px 0";
            botInnerDiv.innerText = `"${query}" araması için sonuç getirme işlemi şu an devre dışı.`;
            botDiv.appendChild(botInnerDiv);
            chatMessages.appendChild(botDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
    }
}