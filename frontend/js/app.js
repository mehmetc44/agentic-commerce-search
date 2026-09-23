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

document.addEventListener("DOMContentLoaded", loadProducts);