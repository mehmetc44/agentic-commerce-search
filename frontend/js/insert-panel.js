/**
 * Ekle (Insert) Toolbar Panel Controller
 * Handles Image options (Linkle/Bilgisayardan), Table Matrix Grid selection, Link Modal, and Emoji Picker.
 */

document.addEventListener("DOMContentLoaded", () => {
    initInsertPanel();
});

function initInsertPanel() {
    const insertBtn = document.getElementById("insertMainBtn");
    const insertMenu = document.getElementById("insertMenuDropdown");
    const feedbackToast = document.getElementById("insertFeedbackToast");
    const feedbackText = document.getElementById("insertFeedbackText");

    if (!insertBtn || !insertMenu) return;

    // 1. Toggle main dropdown
    insertBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        insertMenu.classList.toggle("show");
    });

    // Close menu when clicking outside
    document.addEventListener("click", (e) => {
        if (!insertMenu.contains(e.target) && !insertBtn.contains(e.target)) {
            insertMenu.classList.remove("show");
        }
    });

    // Helper: Display action toast feedback
    function showFeedback(message, icon = "fa-check-circle") {
        if (feedbackToast && feedbackText) {
            feedbackText.innerHTML = `<i class="fa ${icon} me-1 text-secondary"></i> <strong>Bildirim:</strong> ${message}`;
            feedbackToast.style.display = "block";
        }
    }

    // 2. Görsel (Image) Options (Linkle / Bilgisayardan)
    const btnImageLink = document.getElementById("btnImageLink");
    const btnImageFile = document.getElementById("btnImageFile");

    if (btnImageLink) {
        btnImageLink.addEventListener("click", (e) => {
            e.stopPropagation();
            showFeedback("Görsel seçeneği seçildi: <strong>Linkle (URL İle Görsel Ekle)</strong>", "fa-link");
            insertMenu.classList.remove("show");
        });
    }

    if (btnImageFile) {
        btnImageFile.addEventListener("click", (e) => {
            e.stopPropagation();
            showFeedback("Görsel seçeneği seçildi: <strong>Bilgisayardan Yükle</strong>", "fa-desktop");
            insertMenu.classList.remove("show");
        });
    }

    // 3. Tablo (Table) Matrix Selection (8x8 Grid)
    const matrixGridContainer = document.getElementById("matrixGridContainer");
    const matrixDimensionLabel = document.getElementById("matrixDimensionLabel");

    if (matrixGridContainer && matrixDimensionLabel) {
        // Generate 8x8 matrix cells
        matrixGridContainer.innerHTML = "";
        const maxRows = 8;
        const maxCols = 8;

        for (let r = 1; r <= maxRows; r++) {
            for (let c = 1; c <= maxCols; c++) {
                const cell = document.createElement("div");
                cell.className = "matrix-cell";
                cell.dataset.row = r;
                cell.dataset.col = c;

                // Mouse hover on cell
                cell.addEventListener("mouseenter", () => {
                    highlightMatrix(r, c);
                });

                // Click cell to select dimensions
                cell.addEventListener("click", (e) => {
                    e.stopPropagation();
                    showFeedback(`Tablo matrisi seçildi: <strong>${c} x ${r} Tablo</strong>`, "fa-table");
                    insertMenu.classList.remove("show");
                });

                matrixGridContainer.appendChild(cell);
            }
        }

        // Reset highlight when leaving grid container
        matrixGridContainer.addEventListener("mouseleave", () => {
            highlightMatrix(0, 0);
            matrixDimensionLabel.textContent = "Matris Boyutu Seçin";
        });

        function highlightMatrix(targetRow, targetCol) {
            const cells = matrixGridContainer.querySelectorAll(".matrix-cell");
            cells.forEach(cell => {
                const r = parseInt(cell.dataset.row);
                const c = parseInt(cell.dataset.col);
                if (r <= targetRow && c <= targetCol) {
                    cell.classList.add("highlighted");
                } else {
                    cell.classList.remove("highlighted");
                }
            });

            if (targetRow > 0 && targetCol > 0) {
                matrixDimensionLabel.textContent = `${targetCol} x ${targetRow} Tablo`;
            }
        }
    }

    // 4. Link Ekleme (Gösterilecek Metin & Link URL)
    const linkSubmitBtn = document.getElementById("btnInsertLinkSubmit");
    const linkCancelBtn = document.getElementById("btnInsertLinkCancel");
    const linkTextInput = document.getElementById("insertLinkText");
    const linkUrlInput = document.getElementById("insertLinkUrl");

    if (linkSubmitBtn) {
        linkSubmitBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            const textVal = linkTextInput ? linkTextInput.value.trim() : "";
            const urlVal = linkUrlInput ? linkUrlInput.value.trim() : "";

            if (!textVal || !urlVal) {
                alert("Lütfen hem gösterilecek metni hem de link adresini girin.");
                return;
            }

            showFeedback(`Link eklendi: <a href="${urlVal}" target="_blank" class="fw-bold text-decoration-underline">${textVal}</a> (${urlVal})`, "fa-paperclip");
            if (linkTextInput) linkTextInput.value = "";
            if (linkUrlInput) linkUrlInput.value = "";
            insertMenu.classList.remove("show");
        });
    }

    if (linkCancelBtn) {
        linkCancelBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            insertMenu.classList.remove("show");
        });
    }

    // 5. Emoji Seçeneği
    const emojiGrid = document.getElementById("emojiGridContainer");
    const popularEmojis = [
        "😊", "😃", "😍", "🥳", "😎", "👍", 
        "🔥", "⚡", "⭐", "🎉", "💡", "❤️", 
        "🛍️", "🛒", "📦", "🏷️", "💳", "🚀", 
        "💻", "📱", "🎯", "🎨", "✨", "📌"
    ];

    if (emojiGrid) {
        emojiGrid.innerHTML = "";
        popularEmojis.forEach(emoji => {
            const emojiEl = document.createElement("div");
            emojiEl.className = "emoji-item";
            emojiEl.textContent = emoji;
            emojiEl.addEventListener("click", (e) => {
                e.stopPropagation();
                showFeedback(`Emoji seçildi: <span class="fs-5">${emoji}</span>`, "fa-smile");
                insertMenu.classList.remove("show");
            });
            emojiGrid.appendChild(emojiEl);
        });
    }
}
