// ================================================================
//  API Endpoints
// ================================================================
const BASE_URL       = window.location.origin;          // AI Servisi  (:8000)
const CATALOG_API    = "http://localhost:8001";          // Catalog API (:8001)

// ================================================================
//  Yardımcı: Ürün ID'den deterministik fiyat üret (₺)
// ================================================================
function generatePrice(productId) {
    let hash = 0;
    for (let i = 0; i < productId.length; i++) {
        hash = productId.charCodeAt(i) + ((hash << 5) - hash);
    }
    return (199 + (Math.abs(hash) % 1800)).toFixed(2); // 199 ₺ – 1999 ₺
}

// ================================================================
//  Kategorileri Yükle → Navbar + Sidebar
// ================================================================
async function loadCategories() {
    try {
        const res = await fetch(`${CATALOG_API}/categories?limit=20`);
        if (!res.ok) return;
        const { data: categories } = await res.json();

        // — Navbar
        const navbar = document.querySelector("#navbar .navbar-nav");
        if (navbar) {
            navbar.innerHTML = "";
            categories.slice(0, 5).forEach(cat => {
                navbar.innerHTML += `
                    <li class="nav-item">
                        <a href="#" class="nav-link category-link" data-id="${cat.id}">${cat.name}</a>
                    </li>`;
            });
            if (categories.length > 5) {
                let dropdown = `
                    <li class="nav-item dropdown">
                        <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown">Diğer Kategoriler</a>
                        <ul class="dropdown-menu">`;
                categories.slice(5).forEach(cat => {
                    dropdown += `<li><a href="#" class="dropdown-item category-link" data-id="${cat.id}">${cat.name}</a></li>`;
                });
                dropdown += `</ul></li>`;
                navbar.innerHTML += dropdown;
            }
        }

        // — Sidebar
        const sidebar = document.querySelector(".slider_nav");
        if (sidebar) {
            sidebar.innerHTML = "";
            categories.forEach((cat, i) => {
                sidebar.innerHTML += `
                    <a href="#" class="nav-link category-link ${i === 0 ? 'active' : ''}"
                       data-id="${cat.id}">${cat.name}</a>`;
            });
        }

        // — Tıklama olayları
        document.querySelectorAll(".category-link").forEach(link => {
            link.addEventListener("click", async function (e) {
                e.preventDefault();
                document.querySelectorAll(".slider_nav .nav-link").forEach(n => n.classList.remove("active"));
                if (this.closest(".slider_nav")) this.classList.add("active");
                await loadProductsByCategory(this.dataset.id, this.innerText.trim());
            });
        });

        // İlk kategorinin ürünlerini otomatik yükle
        if (categories.length > 0) {
            await loadProductsByCategory(categories[0].id, categories[0].name);
        }

    } catch (err) {
        console.error("Kategoriler yüklenemedi:", err);
    }
}

// ================================================================
//  Kategoriye Göre Ürün Yükle
// ================================================================
async function loadProductsByCategory(categoryId, categoryName) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = `
        <div class="col-12 text-center mt-5">
            <div class="spinner-border text-primary" role="status"></div>
            <h5 class="mt-3 text-muted">${categoryName} kategorisi yükleniyor...</h5>
        </div>`;

    try {
        const res = await fetch(`${CATALOG_API}/products/category/${categoryId}?limit=20`);
        if (!res.ok) throw new Error("Sunucu hatası");
        const { data: products } = await res.json();

        const title = document.querySelector("h3.h4");
        if (title) title.innerText = `${categoryName}  (${products.length} ürün)`;

        renderProducts(products, false);
    } catch (err) {
        console.error("Ürünler yüklenemedi:", err);
        resultsDiv.innerHTML = `
            <div class="col-12 text-center mt-5 text-danger">
                <i class="fa fa-triangle-exclamation fa-2x mb-2"></i>
                <h5>Ürünler getirilirken bir hata oluştu.</h5>
            </div>`;
    }
}

// ================================================================
//  Sayfa İlk Yüklendiğinde
// ================================================================
async function loadProducts() {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = `
        <div class="col-12 text-center mt-5">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-3 text-muted">Kategoriler yükleniyor...</p>
        </div>`;
    await loadCategories();
}

// ================================================================
//  Ürün Kartlarını Render Et
// ================================================================
function renderProducts(products, isAiSearch = false) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (!products || products.length === 0) {
        resultsDiv.innerHTML = `
            <div class="col-12 text-center mt-5">
                <i class="fa fa-box-open fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">Arama kriterlerinize uygun ürün bulunamadı.</h5>
            </div>`;
        return;
    }

    products.forEach(p => {
        const price    = generatePrice(String(p.product_id));
        const imageUrl = p.image_url || "https://placehold.co/300x300/f5f0eb/8B4513?text=Görsel+Yok";
        const link     = `product.html?id=${encodeURIComponent(p.product_id)}`;

        // AI eşleşme rozeti: match_score "82.3%" formatında veya cross_encoder_score sayı
        let badgeHtml = "";
        const score = p.match_score
            ? parseFloat(p.match_score)
            : (p.cross_encoder_score !== undefined ? p.cross_encoder_score : null);

        if (isAiSearch && score !== null) {
            const color = score >= 70 ? "success" : score >= 40 ? "warning" : "secondary";
            badgeHtml = `<span class="badge bg-${color} position-absolute top-0 end-0 m-2 shadow-sm">
                            <i class="fa fa-bolt me-1"></i>${score.toFixed(1)}% Eşleşme
                         </span>`;
        }

        resultsDiv.innerHTML += `
            <div class="col">
                <div class="card h-100 product-card">
                    <div class="img-wrap position-relative">
                        <a href="${link}">
                            <img src="${imageUrl}" alt="${p.title}"
                                 onerror="this.src='https://placehold.co/300x300/f5f0eb/8B4513?text=Görsel+Yok'">
                        </a>
                        ${badgeHtml}
                    </div>
                    <div class="info-wrap">
                        <a href="${link}" class="title" title="${p.title}">${p.title}</a>
                        <div class="d-flex justify-content-between align-items-center mb-2 mt-1">
                            ${p.brand
                                ? `<small class="text-muted border px-2 py-1 bg-white rounded-pill" style="font-size:.75rem;">
                                       <i class="fa fa-tag" style="color:var(--secondary)"></i> ${p.brand}
                                   </small>`
                                : "<span></span>"}
                            ${p.color
                                ? `<small class="text-muted"><i class="fa fa-circle" style="color:var(--secondary);font-size:.7rem;"></i> ${p.color}</small>`
                                : ""}
                        </div>
                        <div class="mt-auto d-flex justify-content-between align-items-center pt-2">
                            <span class="price fw-bold">${price} ₺</span>
                            <a href="${link}" class="btn btn-sm btn-outline-primary rounded-pill px-3">
                                İncele <i class="fa fa-arrow-right ms-1"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>`;
    });
}

document.addEventListener("DOMContentLoaded", loadProducts);