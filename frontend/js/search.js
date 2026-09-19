let ws = null;

function initWebSocket() {
    if (!ws || ws.readyState === WebSocket.CLOSED) {
        const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
        const wsUrl = `${protocol}${window.location.host}/api/v1/ws-search`;
        ws = new WebSocket(wsUrl);
        
        ws.onopen = () => console.log("WebSocket connection established.");
        
        ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            const logsContainer = document.getElementById("aiLogsContainer");
            
            if (msg.type === "log") {
                // Clear the container if it has the "waiting" message
                if (logsContainer.innerHTML.includes("Waiting for a search query")) {
                    logsContainer.innerHTML = "";
                }
                const logEntry = document.createElement("div");
                logEntry.className = "mb-3 p-3 rounded bg-white border-start border-4 border-primary shadow-sm";
                logEntry.innerHTML = msg.message;
                logsContainer.appendChild(logEntry);
                logsContainer.scrollTop = logsContainer.scrollHeight;
            } 
            else if (msg.type === "result") {
                // Update UI Title
                const sectionTitle = document.querySelector("h3.h4");
                if (sectionTitle) {
                    sectionTitle.innerText = `Search Results for "${msg.data.original_query}" (${msg.data.total_found} Products Found)`;
                }
                
                // Hide slider
                const hero = document.getElementById("heroSection");
                if (hero) hero.style.display = "none";
                
                // Render products with AI match badges
                renderProducts(msg.data.products, true);
                
                const logEntry = document.createElement("div");
                logEntry.className = "mb-3 p-3 rounded bg-success text-white shadow-sm text-center";
                logEntry.innerHTML = `<strong><i class="fa fa-check-circle"></i> Completed!</strong><br>Total ${msg.data.total_found} products recommended.`;
                logsContainer.appendChild(logEntry);
                logsContainer.scrollTop = logsContainer.scrollHeight;
            } 
            else if (msg.type === "error") {
                const logEntry = document.createElement("div");
                logEntry.className = "mb-3 p-3 rounded bg-danger text-white shadow-sm";
                logEntry.innerHTML = `<strong><i class="fa fa-exclamation-triangle"></i> Error:</strong><br>${msg.message}`;
                logsContainer.appendChild(logEntry);
                
                // Remove loading animation from main screen
                const resultsDiv = document.getElementById("results");
                resultsDiv.innerHTML = `<div class="col-12 text-center mt-5 text-danger"><h5>An error occurred. Check the AI Panel.</h5></div>`;
            }
        };
        
        ws.onclose = () => {
            console.log("WebSocket disconnected, retrying in 2 seconds...");
            setTimeout(initWebSocket, 2000);
        };
    }
}

// Search Action
function search() {
    const query = document.getElementById("searchInput").value.trim();

    if (!query) return;

    // Hide slider/hero section
    const hero = document.getElementById("heroSection");
    if (hero) hero.style.display = "none";

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = `
        <div class="col-12 text-center mt-5">
            <div class="spinner-border text-primary" role="status"></div>
            <h5 class="mt-3 text-muted">AI Hybrid Search is running...</h5>
            <small class="text-muted">Please follow the process via the 'AI Panel' on the right.</small>
        </div>
    `;

    // Clear log panel and add loading animation
    const logsContainer = document.getElementById("aiLogsContainer");
    logsContainer.innerHTML = `
        <div class="text-center mt-3 text-primary">
            <div class="spinner-border spinner-border-sm mb-2" role="status"></div><br>
            Processing query...
        </div>
    `;
    
    // Auto-open panel
    const aiPanelEl = document.getElementById("aiPanel");
    const aiPanel = bootstrap.Offcanvas.getOrCreateInstance(aiPanelEl);
    aiPanel.show();

    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ query: query }));
    } else {
        console.error("WebSocket is not ready yet. Please wait.");
        initWebSocket(); // Force retry
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initWebSocket();
    
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