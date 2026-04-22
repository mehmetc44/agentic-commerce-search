// Ortak API adresimiz (Eğer search rotan /api/search ise onu da ayarlamayı unutma)
const BASE_URL = "http://127.0.0.1:8000";

// Arama İşlemi
async function search() {
    const query = document.getElementById("searchInput").value.trim();

    if (!query) return;

    // Backend artık GET isteği ve Query parametresi bekliyor (?query=...)
    try {
        const response = await fetch(`${BASE_URL}/search?query=${encodeURIComponent(query)}&limit=12`, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            console.error("Arama sırasında hata oluştu. Status:", response.status);
            return;
        }

        const data = await response.json();
        renderProducts(data.data); // data.data içerisinde ürün listesi var
    } catch (error) {
        console.error("Arama isteği başarısız:", error);
    }
}

// Ana Sayfa İlk Yükleme İşlemi
async function loadProducts() {
    try {
        // page=40 çok ileri bir sayfa, test için page=1 ve page_size=20 yapıyoruz
        const response = await fetch(`${BASE_URL}/api/products?page=1&page_size=20`, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            console.error("Ürünler çekilirken hata oluştu. Status:", response.status);
            return;
        }

        const data = await response.json();
        renderProducts(data.data);
    } catch (error) {
        console.error("Ürünleri getirme isteği başarısız:", error);
    }
}

// Ekrana Ürün Kartlarını Basan Ortak Fonksiyon
function renderProducts(products) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = ""; // İçeriyi temizle

    // Eğer ürün bulunamazsa kullanıcıya bilgi ver
    if (!products || products.length === 0) {
        resultsDiv.innerHTML = `<div class="col-12 text-center mt-5"><h5>Aradığınız kriterlere uygun ürün bulunamadı.</h5></div>`;
        return;
    }

    products.forEach(p => {
        // Pydantic modelindeki alanlara (parent_asin, title, image, price) göre verileri okuyoruz
        
        // Fiyat 0 ise veya yoksa düzgün bir mesaj gösterelim
        const priceText = (p.price && p.price > 0) ? `${p.price} ₺` : 'Fiyat Belirtilmemiş';
        
        // Resim URL'si boşsa yer tutucu (placeholder) bir görsel koyalım
        const imageUrl = p.image ? p.image : "https://via.placeholder.com/300x300?text=Gorsel+Yok";

        resultsDiv.innerHTML += `
            <div class="col">
                <div class="card shadow h-100">
                    <div class="img-wrap" style="height: 200px; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 10px;">
                        <img src="${imageUrl}" alt="${p.title}" class="card-img-top" style="max-height: 100%; max-width: 100%; object-fit: contain;">
                    </div>

                    <div class="border-top info-wrap p-3 d-flex flex-column" style="flex-grow: 1;">
                        <a href="product.html?id=${p.parent_asin}" class="title text-truncate d-block mb-2" title="${p.title}" style="color: #212529; text-decoration: none; font-weight: 500;">
                            ${p.title}
                        </a>
                        
                        <div class="mt-auto d-flex justify-content-between align-items-center">
                            <span class="price-discount text-success fw-bold" style="font-size: 1.1rem;">${priceText}</span>
                            <a href="#" class="btn btn-light btn-sm text-danger">
                                <i class="fa fa-heart"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}

// Ana menü açıldığında otomatik yükleme
document.addEventListener("DOMContentLoaded", loadProducts);