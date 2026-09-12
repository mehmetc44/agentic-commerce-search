document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');

    // Simulate backend LangGraph process
    const mockBackendCall = async (query) => {
        return new Promise(resolve => {
            setTimeout(() => {
                let intent = "UNKNOWN";
                let responseText = "";

                const lowerQuery = query.toLowerCase();
                
                if (lowerQuery.includes('ara') || lowerQuery.includes('kılıf') || lowerQuery.includes('telefon')) {
                    intent = "SEARCH";
                    responseText = "Harika! Siyah iPhone 14 kılıflarını sizin için arıyorum. İşte en çok satan 3 model:\n\n1. Spigen Liquid Air Siyah Kılıf\n2. Apple Orijinal Deri Kılıf (Siyah)\n3. Baseus Ultra İnce Silikon Kılıf";
                } else if (lowerQuery.includes('öner') || lowerQuery.includes('tavsiye')) {
                    intent = "RECOMMENDATION";
                    responseText = "Size özel önerilerim var! Son incelediğiniz ürünlere dayanarak Spigen'in kılıfları tam size göre olabilir. Şık ve dayanıklı bir tasarıma sahipler.";
                } else {
                    intent = "CHAT";
                    responseText = "Merhaba! Size e-ticaret deneyiminizde nasıl yardımcı olabilirim? Ürün arayabilir veya tavsiye isteyebilirsiniz.";
                }

                const analysis = {
                    intent: intent,
                    confidence: 0.95,
                    entities: {
                        product_type: lowerQuery.includes('kılıf') ? "kılıf" : null,
                        color: lowerQuery.includes('siyah') ? "siyah" : null
                    }
                };

                resolve({
                    analysis: JSON.stringify(analysis, null, 2),
                    response: responseText
                });
            }, 1500); // 1.5 second simulated delay
        });
    };

    // Format the assistant's message with JSON block and text
    const formatAssistantMessage = (data) => {
        let html = '';
        if (data.analysis) {
            html += `<h3><i class="fa-solid fa-bullseye"></i> Niyet Analiz Sonucu:</h3>`;
            html += `<pre><code>${data.analysis}</code></pre>`;
        }
        html += `<h3><i class="fa-regular fa-comment-dots"></i> Yönlendirilen Düğüm Yanıtı:</h3>`;
        // Convert basic newlines to paragraphs
        const paragraphs = data.response.split('\n').filter(p => p.trim() !== '');
        paragraphs.forEach(p => {
            html += `<p>${p}</p>`;
        });
        return html;
    };

    // Add a message to the UI
    const addMessage = (content, sender, isHTML = false) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (isHTML) {
            contentDiv.innerHTML = content;
        } else {
            const p = document.createElement('p');
            p.textContent = content;
            contentDiv.appendChild(p);
        }

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.parentElement.scrollTop = chatMessages.parentElement.scrollHeight;
    };

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = userInput.value.trim();
        
        if (!query) return;

        // 1. Add user message to UI
        addMessage(query, 'user');
        
        // 2. Clear input
        userInput.value = '';
        
        // 3. Show typing indicator
        typingIndicator.style.display = 'flex';
        chatMessages.parentElement.scrollTop = chatMessages.parentElement.scrollHeight;

        // 4. Simulate API call
        try {
            const result = await mockBackendCall(query);
            
            // 5. Hide typing indicator
            typingIndicator.style.display = 'none';
            
            // 6. Format and display response
            const formattedResponse = formatAssistantMessage(result);
            addMessage(formattedResponse, 'assistant', true);
            
        } catch (error) {
            typingIndicator.style.display = 'none';
            addMessage("❌ İş akışı yürütülürken hata oluştu. Lütfen tekrar deneyin.", 'assistant');
        }
    });
});
