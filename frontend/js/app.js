// Common API address
const BASE_URL = "http://localhost:8001";


// Fetch categories from API and populate menus
async function loadCategories() {
    try {
        const response = await fetch(`${BASE_URL}/api/v1/categories/main`);
        if (!response.ok) return;
        
        const data = await response.json();
        const categories = Array.isArray(data) ? data : (data.data || []);
        
        // Top menu (Navbar)
        const navbar = document.querySelector("#navbar .navbar-nav");
        if (navbar) {
            navbar.innerHTML = ""; // Clear existing static items
            categories.slice(0, 5).forEach(cat => {
                navbar.innerHTML += `<li class="nav-item"><a href="#" class="nav-link category-link" data-id="${cat.id}">${cat.name}</a></li>`;
            });
            // Make the rest a dropdown
            if (categories.length > 5) {
                let dropdownHtml = `<li class="nav-item dropdown">
                    <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown">Other Categories</a>
                    <ul class="dropdown-menu">`;
                categories.slice(5).forEach(cat => {
                    dropdownHtml += `<li><a href="#" class="dropdown-item category-link" data-id="${cat.id}">${cat.name}</a></li>`;
                });
                dropdownHtml += `</ul></li>`;
                navbar.innerHTML += dropdownHtml;
            }
        }
        

                
        // Add click event to category links
        document.querySelectorAll('.category-link').forEach(link => {
            link.addEventListener('click', async function(e) {
                e.preventDefault();
                
                const catId = this.getAttribute('data-id');
                const catName = this.innerText;
                await loadProductsByCategory(catId, catName);
            });
        });
        
    } catch (error) {
        console.error("Failed to load categories:", error);
    }
}

// Fetch Products by Selected Category
async function loadProductsByCategory(categoryId, categoryName) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = `
        <div class="col-12 text-center mt-5">
            <div class="spinner-border text-primary" role="status"></div>
            <h5 class="mt-3 text-muted">Loading products in ${categoryName}...</h5>
        </div>
    `;
    
    try {
        const response = await fetch(`${BASE_URL}/api/v1/products/main-category/${categoryId}`);
        if (!response.ok) throw new Error("Network error");
        
        const data = await response.json();
        const productsList = Array.isArray(data) ? data : (data.data || []);
        
        // Update title
        const sectionTitle = document.querySelector("#sectionTitle");
        if (sectionTitle) sectionTitle.innerText = `${categoryName} (${productsList.length} Products)`;
        
        renderProducts(productsList);
    } catch (error) {
        console.error("Failed to load category products:", error);
        resultsDiv.innerHTML = `<div class="col-12 text-center mt-5 text-danger"><h5>An error occurred while fetching products.</h5></div>`;
    }
}

// Initial Load for Homepage - Demo Products
async function loadProducts() {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = `
        <div class="col-12 text-center mt-5">
            <div class="spinner-border text-primary" role="status"></div>
            <h5 class="mt-3 text-muted">Ürünler Yükleniyor...</h5>
        </div>
    `;
    
    await loadCategories();

    try {
        const response = await fetch(`${BASE_URL}/api/v1/products?limit=12`);
        if (!response.ok) throw new Error("Network error");
        
        const data = await response.json();
        const productsList = Array.isArray(data) ? data : (data.data || []);
        
        const sectionTitle = document.querySelector("#sectionTitle");
        if (sectionTitle) sectionTitle.innerText = `Öne Çıkan Ürünler`;
        
        renderProducts(productsList);
    } catch (error) {
        console.error("Failed to load initial products:", error);
        resultsDiv.innerHTML = `<div class="col-12 text-center mt-5 text-danger"><h5>Ürünler yüklenirken bir hata oluştu.</h5></div>`;
    }
}

// Common Function to Render Product Cards
function renderProducts(products, isAiSearch = false) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = ""; // Clear content

    if (!products || products.length === 0) {
        resultsDiv.innerHTML = `<div class="col-12 text-center mt-5"><h5>No products found matching your criteria.</h5></div>`;
        return;
    }

    products.forEach(p => {
        const priceText = p.price ? `${p.price} ${p.currency || 'TL'}` : 'Fiyat Belirtilmemiş';
        const imageUrl = p.image_url || p.images?.[0] || "https://via.placeholder.com/300x300?text=No+Image";
        const productLink = `product.html?id=${p.id}`;
        const productName = p.name || p.title || 'Ürün Adı Yok';

        // Rating calculation
        const rating = p.rating || 0;
        const reviewCount = p.review_count || p.rating_count || 0;
        let starsHtml = '';
        if (rating > 0) {
            const fullStars = Math.floor(rating);
            const halfStar = (rating % 1) >= 0.5 ? 1 : 0;
            const emptyStars = 5 - fullStars - halfStar;
            
            for(let i=0; i<fullStars; i++) starsHtml += '<i class="fa-solid fa-star text-warning" style="font-size:0.8rem;"></i>';
            if(halfStar) starsHtml += '<i class="fa-solid fa-star-half-stroke text-warning" style="font-size:0.8rem;"></i>';
            for(let i=0; i<emptyStars; i++) starsHtml += '<i class="fa-regular fa-star text-warning" style="font-size:0.8rem;"></i>';
        } else {
            starsHtml = '<span class="text-muted small">Değerlendirme yok</span>';
        }
        
        const ratingText = rating > 0 ? `<span class="fw-bold ms-1" style="font-size:0.85rem;">${rating.toFixed(1)}</span> <span class="text-muted ms-1" style="font-size:0.75rem;">(${reviewCount} değerlendirme)</span>` : '';

        let badgeHtml = "";
        // Show AI match badge if isAiSearch is true or score < 100
        if (isAiSearch && p.cross_encoder_score) {
            badgeHtml = `<span class="badge bg-success position-absolute top-0 end-0 m-2 shadow-sm">Eşleşme: ${p.cross_encoder_score.toFixed(1)}%</span>`;
        } else if (p.cross_encoder_score && p.cross_encoder_score < 100) {
            badgeHtml = `<span class="badge bg-success position-absolute top-0 end-0 m-2 shadow-sm">Eşleşme: ${p.cross_encoder_score.toFixed(1)}%</span>`;
        }

        const brandText = p.brand ? `<span class="fw-bold text-dark me-1" style="font-size: 0.9rem;">${p.brand}</span>` : '';

        resultsDiv.innerHTML += `
            <div class="col">
                <div class="card h-100 border product-card" onclick="window.location.href='${productLink}'" style="cursor: pointer; border-radius: 8px; overflow: hidden; transition: box-shadow 0.2s; box-shadow: 0 1px 4px rgba(0,0,0,0.05);" onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)'" onmouseout="this.style.boxShadow='0 1px 4px rgba(0,0,0,0.05)'">
                    <div class="img-wrap bg-white" style="height: 250px; display: flex; align-items: center; justify-content: center; overflow: hidden; position: relative;">
                        <img src="${imageUrl}" alt="${productName}" style="max-height: 100%; max-width: 100%; object-fit: cover;">
                        ${badgeHtml}
                        
                        <!-- AI Add Button (Shows on Hover) -->
                        <div class="position-absolute p-2 ai-hover-overlay" style="top: 0; right: 0; z-index: 10;">
                            <button class="btn btn-sm btn-warning rounded shadow fw-bold ai-add-btn" 
                                    title="AI'a Sor (Bağlama Ekle)" 
                                    data-id="${p.id}" 
                                    data-name="${(p.name || p.title || '').replace(/"/g, '&quot;')}" 
                                    data-image="${imageUrl}" 
                                    data-price="${priceText}"
                                    onclick="event.stopPropagation(); addToAIContext(this.getAttribute('data-id'), this.getAttribute('data-name'), this.getAttribute('data-image'), this.getAttribute('data-price'))">
                                <i class="fa-solid fa-plus me-1"></i> Ekle
                            </button>
                        </div>
                    </div>

                    <div class="info-wrap p-2 d-flex flex-column bg-white text-start" style="flex-grow: 1;">
                        <div class="title text-truncate-2 d-block mb-1" title="${productName}" style="color: #333; font-size: 0.85rem; line-height: 1.3; height: 2.6em; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                            ${brandText}${productName}
                        </div>
                        
                        <div class="mb-2 mt-1 d-flex align-items-center">
                            ${starsHtml}
                            ${ratingText}
                        </div>
                        
                        <div class="mt-auto pt-1 text-start">
                            <span class="price-discount text-danger fw-bold" style="font-size: 1.1rem;">${priceText}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}

// Global context array to hold selected products
window.aiSelectedProducts = [];

// Function to add product to AI Context
function addToAIContext(id, name, image, price) {
    // Check if already added
    if (window.aiSelectedProducts.find(p => p.id === id)) {
        openAIPanel();
        return;
    }

    const product = { id, name, image, price };
    window.aiSelectedProducts.push(product);
    
    renderAIContext();
    openAIPanel();
}

// Function to remove product from AI Context
function removeFromAIContext(id) {
    window.aiSelectedProducts = window.aiSelectedProducts.filter(p => p.id !== id);
    renderAIContext();
}

// Function to render the context area above the chat input
function renderAIContext() {
    const contextArea = document.getElementById("aiContextArea");
    if (!contextArea) return;
    
    if (window.aiSelectedProducts.length === 0) {
        contextArea.style.setProperty("display", "none", "important");
        contextArea.innerHTML = "";
        return;
    }
    
    contextArea.style.setProperty("display", "flex", "important");
    contextArea.innerHTML = window.aiSelectedProducts.map(p => `
        <div class="d-inline-flex align-items-center bg-white border rounded shadow-sm p-1 position-relative" style="min-width: 150px; max-width: 200px;">
            <img src="${p.image}" class="rounded" style="width: 30px; height: 30px; object-fit: cover; margin-right: 8px;">
            <div class="text-truncate" style="font-size: 0.75rem; line-height: 1.1;">
                <div class="fw-bold text-truncate">${p.name}</div>
                <div class="text-primary">${p.price}</div>
            </div>
            <button onclick="removeFromAIContext('${p.id}')" class="btn btn-sm btn-link text-danger position-absolute top-0 end-0 p-0 m-1" style="line-height: 0.5;">
                <i class="fa-solid fa-times-circle"></i>
            </button>
        </div>
    `).join("");
}

// Helper to open the AI offcanvas
function openAIPanel() {
    const aiPanelEl = document.getElementById('aiPanel');
    if (aiPanelEl) {
        const bsOffcanvas = bootstrap.Offcanvas.getOrCreateInstance(aiPanelEl);
        bsOffcanvas.show();
    }
}

// AI Chat Interaction Logic
async function sendMessageToAI() {
    const inputEl = document.getElementById("chatInput");
    const query = inputEl.value.trim();
    if (!query) return;

    const chatMessages = document.getElementById("chatMessages");

    // Add user message to UI
    chatMessages.innerHTML += `
        <div class="d-flex mb-3 justify-content-end">
            <div class="bg-primary text-white p-2 rounded shadow-sm" style="max-width: 80%; border-radius: 15px 15px 0 15px !important;">
                ${query}
            </div>
        </div>
    `;
    inputEl.value = "";
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Add typing indicator
    const typingId = "typing-" + Date.now();
    chatMessages.innerHTML += `
        <div id="${typingId}" class="d-flex mb-3">
            <div class="bg-light text-dark p-2 rounded shadow-sm border" style="max-width: 80%; border-radius: 15px 15px 15px 0 !important;">
                <i class="fa-solid fa-ellipsis fa-fade"></i> Düşünüyor...
            </div>
        </div>
    `;
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch("http://localhost:8000/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query,
                context_products: window.aiSelectedProducts
            })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        
        // Remove typing indicator
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();

        // Convert newlines to HTML breaks and render markdown if possible (simple fallback)
        const formattedResponse = data.response.replace(/\n/g, '<br>');

        // Add AI response to UI
        chatMessages.innerHTML += `
            <div class="d-flex mb-3">
                <div class="bg-white text-dark p-3 rounded shadow-sm border" style="max-width: 90%; border-radius: 15px 15px 15px 0 !important;">
                    ${formattedResponse}
                </div>
            </div>
        `;
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Clear context after successful query if desired (optional)
        // window.aiSelectedProducts = [];
        // renderAIContext();

    } catch (error) {
        console.error("AI Error:", error);
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();
        
        chatMessages.innerHTML += `
            <div class="d-flex mb-3">
                <div class="bg-danger text-white p-2 rounded shadow-sm" style="max-width: 80%; border-radius: 15px 15px 15px 0 !important;">
                    Üzgünüm, şu an bağlantı kuramıyorum. Lütfen sistemin çalıştığından emin olun.
                </div>
            </div>
        `;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadProducts();
    
    // Bind chat events
    const sendBtn = document.getElementById("chatSendBtn");
    const inputEl = document.getElementById("chatInput");
    
    if (sendBtn) {
        sendBtn.addEventListener("click", sendMessageToAI);
    }
    if (inputEl) {
        inputEl.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                sendMessageToAI();
            }
        });
    }
});