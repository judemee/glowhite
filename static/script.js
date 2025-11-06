// ---------- Image Modal ----------
function openModal(src) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImg');
    modalImg.src = src;
    modal.style.display = 'flex';
}
function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
}

// ---------- Confirmation Modal ----------
document.addEventListener("DOMContentLoaded", () => {
    const orderForm = document.getElementById("orderForm");
    const modal = document.getElementById("confirmModal");
    const details = document.getElementById("confirmDetails");
    const yesBtn = document.getElementById("confirmYes");
    const noBtn = document.getElementById("confirmNo");

    if (!orderForm) return;

    orderForm.addEventListener("submit", (e) => {
        e.preventDefault();

        const name = orderForm.querySelector('[name="name"]').value.trim();
        const phone = orderForm.querySelector('[name="phone"]').value.trim();
        const address = orderForm.querySelector('[name="address"]').value.trim();

        if (!name || !phone || !address) {
            alert("Please fill in all fields before submitting your order.");
            return;
        }

        details.innerHTML = `
      <strong>Name:</strong> ${name}<br>
      <strong>Phone:</strong> ${phone}<br>
      <strong>Address:</strong> ${address}<br><br>
      Confirm to send your order?
    `;
        modal.style.display = "flex";

        // Confirm
        yesBtn.onclick = () => {
            modal.style.display = "none";
            orderForm.submit();
        };

        // Cancel
        noBtn.onclick = () => {
            modal.style.display = "none";
        };
    });
});

// ---------- Popup Ad ----------
function showPopupAd() {
    const ad = document.createElement("div");
    ad.className = "popup-ad";
    ad.innerHTML = `
    <h4>🔥 Special Offer</h4>
    <p>Buy 2 packs and get <strong>free shipping</strong>!</p>
    <a class="close-ad" href="#" onclick="this.parentElement.remove();return false;">Close</a>
  `;
    document.body.appendChild(ad);
    ad.style.display = "block";
    setTimeout(() => { if (ad.parentElement) ad.remove(); }, 10000);
}

window.addEventListener("load", () => {
    setTimeout(showPopupAd, 10000);
});
