// Initialize Chat
document.addEventListener("DOMContentLoaded", () => {
    const aiChatInput = document.getElementById("aiChatInput");
    if (aiChatInput) {
        aiChatInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendChatMessage();
            }
        });
    }

    // Override the top bar search button to also use the chat
    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                search();
            }
        });
    }
});

function search() {
    const query = document.getElementById("searchInput").value.trim();
    if (!query) return;

    // Open AI Panel and send message
    const aiPanelEl = document.getElementById("aiPanel");
    const aiPanel = bootstrap.Offcanvas.getOrCreateInstance(aiPanelEl);
    aiPanel.show();
    
    document.getElementById("aiChatInput").value = query;
    sendChatMessage();
}

async function sendChatMessage() {
    const inputEl = document.getElementById("aiChatInput");
    const message = inputEl.value.trim();
    if (!message) return;

    const logsContainer = document.getElementById("aiLogsContainer");

    // Clear initial empty state message
    if (logsContainer.innerHTML.includes("Merhaba! Size nasıl yardımcı olabilirim")) {
        logsContainer.innerHTML = "";
    }

    // Append user message
    logsContainer.innerHTML += `
        <div class="d-flex justify-content-end mb-3">
            <div class="bg-primary text-white p-2 rounded shadow-sm" style="max-width: 80%;">
                ${message}
            </div>
        </div>
    `;
    logsContainer.scrollTop = logsContainer.scrollHeight;
    
    // Clear input
    inputEl.value = "";
    inputEl.disabled = true;
    document.getElementById("aiChatBtn").disabled = true;

    // Append typing indicator
    const typingId = 'typing-' + Date.now();
    logsContainer.innerHTML += `
        <div id="${typingId}" class="d-flex justify-content-start mb-3">
            <div class="bg-white p-2 rounded shadow-sm text-muted" style="max-width: 80%;">
                <div class="spinner-grow spinner-grow-sm text-primary" role="status"></div>
                <div class="spinner-grow spinner-grow-sm text-primary" role="status"></div>
                <div class="spinner-grow spinner-grow-sm text-primary" role="status"></div>
            </div>
        </div>
    `;
    logsContainer.scrollTop = logsContainer.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: message })
        });
        
        if (!response.ok) throw new Error("Sunucu hatası: " + response.status);
        
        const data = await response.json();
        
        // Remove typing indicator
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();

        // Check if there are products in the response (we will add this capability later)
        if (data.products && data.products.length > 0) {
            // Render products on the main screen
            const hero = document.getElementById("heroSection");
            if (hero) hero.style.display = "none";
            
            const sectionTitle = document.querySelector("h3.h4");
            if (sectionTitle) {
                sectionTitle.innerText = `Sizin için bulunan ürünler (${data.products.length})`;
            }
            renderProducts(data.products, true);
        }

        // Add AI response to chat
        const parsedResponse = marked.parse ? marked.parse(data.response) : data.response;
        
        logsContainer.innerHTML += `
            <div class="d-flex justify-content-start mb-3">
                <div class="bg-white p-3 rounded shadow-sm" style="max-width: 90%; border-left: 4px solid #0d6efd;">
                    ${parsedResponse}
                </div>
            </div>
        `;
        logsContainer.scrollTop = logsContainer.scrollHeight;

    } catch (error) {
        console.error(error);
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();

        logsContainer.innerHTML += `
            <div class="d-flex justify-content-start mb-3">
                <div class="bg-danger text-white p-2 rounded shadow-sm" style="max-width: 80%;">
                    <i class="fa fa-exclamation-triangle"></i> Bir hata oluştu. Lütfen tekrar deneyin.
                </div>
            </div>
        `;
        logsContainer.scrollTop = logsContainer.scrollHeight;
    } finally {
        inputEl.disabled = false;
        document.getElementById("aiChatBtn").disabled = false;
        inputEl.focus();
    }
}