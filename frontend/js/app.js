async function search() {
    const query = document.getElementById("searchInput").value;

    if (!query) return;

    const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
    });

    const data = await response.json();

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = ""; // temizle

    data.results.forEach(p => {
        resultsDiv.innerHTML += `
            <div class="col">
                <div class="card shadow">
                    <div class="img-wrap">
                        <img src="${p.image}" class="card-img-top">
                    </div>

                    <div class="border-top info-wrap">
                        <a href="product.html?id=${p.id}" class="title text-truncate">
                            ${p.name}
                        </a>

                        <div class="price-wrap">
                            <span class="price-discount">${p.price} ₺</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}
async function loadProducts() {
    const response = await fetch("http://127.0.0.1:8000/api/products?page=40&page_size=50");
    const data = await response.json();

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = ""; // önce temizle

    data.data.forEach(p => {
        resultsDiv.innerHTML += `
            <div class="col">
                <div class="card shadow">
                    <div class="img-wrap">
                        <span class="badge bg-success">İndirim</span>
                        <img src="${p.imgUrl}" alt="${p.title}" class="card-img-top">
                    </div>

                    <div class="border-top info-wrap">
                        <a href="#" class="float-end btn btn-light">
                            <i class="fa fa-heart"></i>
                        </a>
                        <a href="product.html?id=${p.asin}" class="title text-truncate">${p.title}</a>
                        <div class="price-wrap">
                            <span class="price-discount">${p.price ?? 'Görünmüyor'} ₺</span>
                        </div>
                    </div>
                </div>
            </div>`;
    });
}

// Ana menü açıldığında otomatik yükleme
document.addEventListener("DOMContentLoaded", loadProducts);
window.addEventListener("DOMContentLoaded", loadProducts);