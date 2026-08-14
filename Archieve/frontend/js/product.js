// Consistent random price generator (based on Product ID) - 5$ ile 25$ arası
function generatePrice(productId) {
    let hash = 0;
    for (let i = 0; i < productId.length; i++) {
        hash = productId.charCodeAt(i) + ((hash << 5) - hash);
    }
    const price = 5 + (Math.abs(hash) % 21); // Between 5 and 25
    return price.toFixed(2);
}

document.addEventListener("DOMContentLoaded", async () => {
    // 1. Get product ID from URL (e.g. product.html?id=some-product-id)
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');

    if (!productId) {
        document.getElementById("productTitle").innerText = "Product ID not found.";
        return;
    }

    try {
        // 2. Fetch product details from Backend
        const response = await fetch(`/api/v1/products/${productId}`);
        
        if (!response.ok) {
            throw new Error("Product could not be loaded.");
        }

        const data = await response.json();
        const product = data.data;

        // Price Generation
        const priceValue = generatePrice(product.product_id);

        // 3. Fill HTML elements
        document.getElementById("productTitle").innerText = product.title || "No Title Available";
        document.getElementById("breadcrumbTitle").innerText = product.title || "Product";
        document.getElementById("breadcrumbCategory").innerText = product.category_taxonomy || product.product_type || "General";
        
        document.getElementById("productPrice").innerText = `${priceValue} $`;
        document.getElementById("productDescription").innerText = product.description || "No description available for this product yet.";
        
        // Add extra specs
        let specsHtml = "";
        if (product.brand) specsHtml += `<dt class="col-4 text-muted">Brand</dt><dd class="col-8">${product.brand}</dd>`;
        if (product.color) specsHtml += `<dt class="col-4 text-muted">Color</dt><dd class="col-8">${product.color}</dd>`;
        if (product.material) specsHtml += `<dt class="col-4 text-muted">Material</dt><dd class="col-8">${product.material}</dd>`;
        if (product.style) specsHtml += `<dt class="col-4 text-muted">Style</dt><dd class="col-8">${product.style}</dd>`;
        if (product.product_type) specsHtml += `<dt class="col-4 text-muted">Type</dt><dd class="col-8">${product.product_type}</dd>`;
        if (product.category_taxonomy) specsHtml += `<dt class="col-4 text-muted">Category</dt><dd class="col-8">${product.category_taxonomy}</dd>`;
        
        const detailsContainer = document.querySelector("dl.row");
        if (detailsContainer && specsHtml) {
            detailsContainer.innerHTML = specsHtml;
        }

        // Image placement
        const imageUrl = product.image_url ? product.image_url : "https://via.placeholder.com/600x600?text=No+Image";
        const mainImg = document.getElementById("mainImage");
        if (mainImg) {
            mainImg.src = imageUrl;
            mainImg.style.mixBlendMode = "multiply";
            document.getElementById("mainImageLink").href = imageUrl;
            
            // Refresh fslightbox
            if (typeof refreshFsLightbox === 'function') refreshFsLightbox();
        }

        // Rating Stars (Random 3-5 stars)
        const ratingStars = document.getElementById("ratingStars");
        if (ratingStars) {
            ratingStars.innerHTML = "";
            const stars = 3 + (Math.abs(productId.charCodeAt(0)) % 3); // Between 3 and 5
            for (let i = 1; i <= 5; i++) {
                if (i <= stars) {
                    ratingStars.innerHTML += `<span class="fa fa-star text-warning"></span>`;
                } else {
                    ratingStars.innerHTML += `<span class="fa fa-star text-secondary"></span>`;
                }
            }
            document.getElementById("ratingCount").innerText = `${(Math.abs(productId.charCodeAt(1)) % 100) + 15} Reviews`;
        }

    } catch (error) {
        console.error("Error loading product:", error);
        document.getElementById("productTitle").innerText = "An error occurred while loading the product.";
        document.getElementById("productDescription").innerText = "";
    }
});