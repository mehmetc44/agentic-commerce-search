document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');

    // Call backend LangGraph API
    const callBackendAPI = async (query) => {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        if (!response.ok) {
            throw new Error(`API hatası: ${response.status}`);
        }
        
        return await response.json();
    };

    // JSON Syntax Highlighter
    const syntaxHighlight = (jsonStr) => {
        let json = jsonStr.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
            let cls = 'number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'key';
                } else {
                    cls = 'string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'boolean';
            } else if (/null/.test(match)) {
                cls = 'null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        });
    };

    // Format the assistant's message with JSON block and text
    const formatAssistantMessage = (data) => {
        let html = '';
        if (data.analysis) {
            let prettyJson = data.analysis;
            try {
                // Prettify if it is a valid JSON string but compressed
                const parsed = JSON.parse(data.analysis);
                prettyJson = JSON.stringify(parsed, null, 2);
            } catch(e) {}
            
            html += `<h3><i class="fa-solid fa-bullseye"></i> Niyet Analiz Sonucu:</h3>`;
            html += `<pre><code>${syntaxHighlight(prettyJson)}</code></pre>`;
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

        // 4. Call API
        try {
            const result = await callBackendAPI(query);
            
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
