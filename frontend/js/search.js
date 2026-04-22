// Arama İşlemi
async function search() {
    const query = document.getElementById("searchInput").value.trim();

    if (!query) return;

    const resultsDiv = document.getElementById("results");
    
    // Kullanıcıya arama yapıldığını hissettirmek için yükleniyor (spinner) gösterelim
    resultsDiv.innerHTML = `
        <div class="col-12 text-center mt-5">
            <div class="spinner-border text-primary" role="status"></div>
            <h5 class="mt-3 text-muted">En alakalı ürünler aranıyor...</h5>
        </div>
    `;

    try {
        // limit=20 olarak güncelledik. En alakalı 20 sonuç gelecek.
        const response = await fetch(`http://127.0.0.1:8000/search?query=${encodeURIComponent(query)}&limit=20`, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            console.error("Arama sırasında hata oluştu. Status:", response.status);
            resultsDiv.innerHTML = `<div class="col-12 text-center mt-5 text-danger"><h5>Arama yapılamadı. Sunucu hatası.</h5></div>`;
            return;
        }

        const data = await response.json();
        
        // renderProducts fonksiyonu app.js içerisinde tanımlı. 
        // İki JS dosyası da aynı HTML'de olduğu için birbirlerini tanırlar.
        renderProducts(data.data); 
        
    } catch (error) {
        console.error("Arama isteği başarısız:", error);
        resultsDiv.innerHTML = `<div class="col-12 text-center mt-5 text-danger"><h5>Sunucuya bağlanılamadı. Backend açık mı?</h5></div>`;
    }
}

// Arama kutusundayken "Enter" tuşuna basılırsa otomatik arama yapma
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault(); // Sayfanın yenilenmesini engeller
                search(); // Arama fonksiyonunu tetikler
            }
        });
    }
});