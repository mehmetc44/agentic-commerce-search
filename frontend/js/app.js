// Common API address
const BASE_URL = window.location.origin;

// Consistent random price generator (based on Product ID) - 5$ ile 25$ arası
function generatePrice(productId) {
    let hash = 0;
    for (let i = 0; i < productId.length; i++) {
        hash = productId.charCodeAt(i) + ((hash << 5) - hash);
    }
    const price = 5 + (Math.abs(hash) % 21); // Between 5 and 25
    return price.toFixed(2);
}

// Fetch categories from API and populate menus
async function loadCategories() {
    try {
        const response = await fetch(`${BASE_URL}/api/v1/categories`);
        if (!response.ok) return;
        
        const data = await response.json();
        const categories = data.data;
        
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
        
        // Left menu (Sidebar Slider)
        const sidebar = document.querySelector(".slider_nav");
        if (sidebar) {
            sidebar.innerHTML = ""; // Clear existing static items
            categories.forEach((cat, index) => {
                sidebar.innerHTML += `<a href="#" class="nav-link category-link ${index === 0 ? 'active' : ''}" data-id="${cat.id}">${cat.name}</a>`;
            });
        }
        
        // Add click event to category links
        document.querySelectorAll('.category-link').forEach(link => {
            link.addEventListener('click', async function(e) {
                e.preventDefault();
                // Update sidebar active state
                document.querySelectorAll('.slider_nav .nav-link').forEach(n => n.classList.remove('active'));
                if (this.closest('.slider_nav')) {
                    this.classList.add('active');
                }
                
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
        const response = await fetch(`${BASE_URL}/api/v1/products/category/${categoryId}`);
        if (!response.ok) throw new Error("Network error");
        
        const data = await response.json();
        
        // Update title
        const sectionTitle = document.querySelector("h3.h4");
        if (sectionTitle) sectionTitle.innerText = `${categoryName} (${data.data.length} Products)`;
        
        renderProducts(data.data);
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
            <h5 class="text-muted">You can type in the search bar (e.g., "waterproof boots for baby") to search...</h5>
            <p class="text-muted">Or select a category from the menu above.</p>
        </div>
    `;
    
    await loadCategories();
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
        const priceValue = generatePrice(p.product_id);
        const priceText = `${priceValue} $`;
        const imageUrl = p.image_url ? p.image_url : "https://via.placeholder.com/300x300?text=No+Image";
        const productLink = `product.html?id=${p.product_id}`;

        let badgeHtml = "";
        // Show AI match badge if isAiSearch is true or score < 100
        if (isAiSearch && p.cross_encoder_score) {
            badgeHtml = `<span class="badge bg-success position-absolute top-0 end-0 m-2 shadow-sm">Match Rate: ${p.cross_encoder_score.toFixed(1)}%</span>`;
        } else if (p.cross_encoder_score && p.cross_encoder_score < 100) {
            badgeHtml = `<span class="badge bg-success position-absolute top-0 end-0 m-2 shadow-sm">Match Rate: ${p.cross_encoder_score.toFixed(1)}%</span>`;
        }

        resultsDiv.innerHTML += `
            <div class="col">
                <div class="card shadow-sm h-100 border-0 product-card">
                    <div class="img-wrap bg-white" style="height: 220px; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 15px; position: relative;">
                        <a href="${productLink}" class="d-block w-100 h-100 text-center">
                            <img src="${imageUrl}" alt="${p.title}" style="max-height: 100%; max-width: 100%; object-fit: contain; mix-blend-mode: multiply;">
                        </a>
                        ${badgeHtml}
                    </div>

                    <div class="border-top info-wrap p-3 d-flex flex-column bg-light" style="flex-grow: 1;">
                        <a href="${productLink}" class="title text-truncate d-block mb-2" title="${p.title}" style="color: #212529; text-decoration: none; font-weight: 500; font-size: 0.95rem;">
                            ${p.title}
                        </a>
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            ${p.brand ? `<small class="text-muted border px-2 py-1 bg-white rounded-pill" style="font-size: 0.75rem;"><i class="fa fa-tag text-primary"></i> ${p.brand}</small>` : '<span></span>'}
                            ${p.color ? `<small class="text-muted"><i class="fa fa-palette text-secondary"></i> ${p.color}</small>` : ''}
                        </div>
                        
                        <div class="mt-auto d-flex justify-content-between align-items-center pt-2">
                            <span class="price-discount text-danger fw-bold fs-5">${priceText}</span>
                            <a href="${productLink}" class="btn btn-outline-primary btn-sm rounded-pill px-3">
                                View <i class="fa fa-arrow-right ms-1"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}

document.addEventListener("DOMContentLoaded", loadProducts);