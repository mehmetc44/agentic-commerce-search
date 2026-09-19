// ================================================================
//  product.js — Ürün Detay Sayfası
//  catalog-api'den (:8001) tekil ürün getirir ve sayfayı doldurur.
// ================================================================

const CATALOG_API = "http://localhost:8001";

// Deterministik fiyat üretici (app.js ile aynı algoritma)
function generatePrice(productId) {
    let hash = 0;
    for (let i = 0; i < productId.length; i++) {
        hash = productId.charCodeAt(i) + ((hash << 5) - hash);
    }
    return (199 + (Math.abs(hash) % 1800)).toFixed(2);
}

// Deterministik yıldız sayısı (3–5)
function generateStars(productId) {
    return 3 + (Math.abs(productId.charCodeAt(0) || 0) % 3);
}

// Deterministik değerlendirme sayısı (15–114)
function generateReviewCount(productId) {
    return (Math.abs(productId.charCodeAt(1) || 0) % 100) + 15;
}

document.addEventListener("DOMContentLoaded", async () => {
    const params    = new URLSearchParams(window.location.search);
    const productId = params.get("id");

    const titleEl       = document.getElementById("productTitle");
    const priceEl       = document.getElementById("productPrice");
    const descEl        = document.getElementById("productDescription");
    const starsEl       = document.getElementById("ratingStars");
    const reviewEl      = document.getElementById("ratingCount");
    const breadCatEl    = document.getElementById("breadcrumbCategory");
    const breadTitleEl  = document.getElementById("breadcrumbTitle");
    const mainImgEl     = document.getElementById("mainImage");
    const mainImgLinkEl = document.getElementById("mainImageLink");
    const specsEl       = document.querySelector("dl.row");
    const storeEl       = document.getElementById("productStore");
    const mainCatEl     = document.getElementById("productMainCat");

    if (!productId) {
        if (titleEl) titleEl.innerText = "Ürün ID bulunamadı.";
        return;
    }

    // Yükleniyor göstergesi
    if (titleEl) titleEl.innerText = "Yükleniyor...";

    try {
        const res = await fetch(`${CATALOG_API}/products/${encodeURIComponent(productId)}`);

        if (res.status === 404) {
            if (titleEl) titleEl.innerText = "Ürün bulunamadı.";
            if (descEl)  descEl.innerText  = "Bu ürün mevcut değil veya kaldırılmış olabilir.";
            return;
        }
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const { data: p } = await res.json();

        // ── Başlık & Breadcrumb ──────────────────────────────
        const title = p.title || "Başlık Yok";
        if (titleEl)      titleEl.innerText      = title;
        if (breadTitleEl) breadTitleEl.innerText  = title;
        if (breadCatEl)   breadCatEl.innerText    = p.category_taxonomy || p.product_type || "Genel";

        // ── Fiyat ───────────────────────────────────────────
        const price = generatePrice(String(p.product_id));
        if (priceEl) priceEl.innerText = `${price} ₺`;

        // ── Açıklama ─────────────────────────────────────────
        if (descEl) descEl.innerText = p.description || "Bu ürün için henüz açıklama eklenmemiş.";

        // ── Yıldız & Değerlendirme ───────────────────────────
        if (starsEl) {
            const stars = generateStars(String(p.product_id));
            starsEl.innerHTML = Array.from({ length: 5 }, (_, i) =>
                `<span class="fa fa-star ${i < stars ? "text-warning" : "text-secondary"}"></span>`
            ).join("");
        }
        if (reviewEl) reviewEl.innerText = `${generateReviewCount(String(p.product_id))} Değerlendirme`;

        // ── Teknik Özellikler ────────────────────────────────
        if (specsEl) {
            const specs = [
                ["Marka",           p.brand],
                ["Renk",            p.color],
                ["Malzeme",         p.material],
                ["Stil",            p.style],
                ["Ürün Tipi",       p.product_type],
                ["Model Yılı",      p.model_year],
                ["Kategori",        p.category_taxonomy],
            ].filter(([, val]) => val);

            if (specs.length > 0) {
                specsEl.innerHTML = specs
                    .map(([label, val]) =>
                        `<dt class="col-4 text-muted">${label}</dt><dd class="col-8">${val}</dd>`
                    ).join("");
            }
        }

        // ── Mağaza / Ana Kategori ────────────────────────────
        if (storeEl)   storeEl.innerText   = "AgenticCommerce";
        if (mainCatEl) mainCatEl.innerText = p.category_taxonomy ? p.category_taxonomy.split("/")[0] : "—";

        // ── Görsel ──────────────────────────────────────────
        const imageUrl = p.image_url || "https://placehold.co/600x600/f5f0eb/8B4513?text=Görsel+Yok";
        if (mainImgEl) {
            mainImgEl.src             = imageUrl;
            mainImgEl.alt             = title;
            mainImgEl.style.mixBlendMode = "multiply";
            mainImgEl.onerror = () => {
                mainImgEl.src = "https://placehold.co/600x600/f5f0eb/8B4513?text=Görsel+Yok";
            };
        }
        if (mainImgLinkEl) {
            mainImgLinkEl.href = imageUrl;
        }

        // FSLightbox yenile (eğer yüklüyse)
        if (typeof refreshFsLightbox === "function") refreshFsLightbox();

    } catch (err) {
        console.error("Ürün yüklenirken hata:", err);
        if (titleEl) titleEl.innerText = "Ürün yüklenirken bir hata oluştu.";
        if (descEl)  descEl.innerText  = "";
    }
});