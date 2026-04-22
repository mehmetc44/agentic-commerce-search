document.addEventListener("DOMContentLoaded", async () => {
    // 1. URL'den ürün ID'sini al (Örn: product.html?id=B08FX1F9XX)
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');

    if (!productId) {
        document.getElementById("productTitle").innerText = "Product ID not found.";
        return;
    }

    try {
        // 2. Backend'den ürün detaylarını çek
        const response = await fetch(`/api/product/${productId}`);
        
        if (!response.ok) {
            throw new Error("Product could not be loaded.");
        }

        const product = await response.json();

        // 3. HTML elemanlarını verilerle doldur
        document.getElementById("productTitle").innerText = product.title || "No Title Available";
        document.getElementById("breadcrumbTitle").innerText = product.title || "Product";
        document.getElementById("breadcrumbCategory").innerText = product.main_category || "General";
        
        document.getElementById("productPrice").innerText = product.price > 0 ? `${product.price} ₺` : "Price not available";
        document.getElementById("productDescription").innerText = product.description || "No description available for this product.";
        
        document.getElementById("productStore").innerText = product.store || "Unknown";
        document.getElementById("productMainCat").innerText = product.main_category || "-";

        // Görsel yerleştirme
        if (product.image) {
            const mainImg = document.getElementById("mainImage");
            mainImg.src = product.image;
            document.getElementById("mainImageLink").href = product.image;
            
            // fslightbox'ı yenile (yeni resim için)
            if (typeof refreshFsLightbox === 'function') refreshFsLightbox();
        }

        // Rating Yıldızlarını Oluşturma (Basit mantık)
        const ratingStars = document.getElementById("ratingStars");
        const rating = Math.round(product.average_rating || 0);
        ratingStars.innerHTML = "";
        for (let i = 1; i <= 5; i++) {
            ratingStars.innerHTML += `<span class="fa fa-star ${i <= rating ? 'text-warning' : 'text-secondary'}"></span>`;
        }
        document.getElementById("ratingCount").innerText = `(${product.rating_number || 0} reviews)`;

    } catch (error) {
        console.error("Error loading product:", error);
        document.getElementById("productTitle").innerText = "Error loading product details.";
    }
});