let player = document.getElementById("player");
let statusText = document.getElementById("status");
let loader = document.getElementById("loader");

function showLoader(msg) {
    loader.style.display = "inline-block";
    statusText.innerText = msg;
}

function hideLoader(msg) {
    loader.style.display = "none";
    statusText.innerText = msg;
}

// TEXT
function generateAudio() {
    const text = document.getElementById("text").value;

    showLoader("⏳ O‘qilmoqda...");

    fetch("/api/read/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text: text})
    })
    .then(res => res.blob())
    .then(blob => {
        player.src = URL.createObjectURL(blob);
        player.play();
        hideLoader("✅ Tayyor!");
    })
    .catch(() => hideLoader("❌ Xatolik"));
}

// PDF
function uploadPDF() {
    const file = document.getElementById("pdfFile").files[0];

    if (!file) {
        statusText.innerText = "❗ PDF tanlanmagan";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    showLoader("⏳ PDF yuklanmoqda...");

    fetch("/api/pdf/", {
        method: "POST",
        body: formData
    })
    .then(res => res.blob())
    .then(blob => {
        player.src = URL.createObjectURL(blob);
        player.play();
        hideLoader("✅ Tayyor!");
    })
    .catch(() => hideLoader("❌ Xatolik"));
}

// IMAGE
function uploadImage() {
    const file = document.getElementById("imageFile").files[0];

    if (!file) {
        statusText.innerText = "❗ Rasm tanlanmagan";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    showLoader("⏳ OCR ishlayapti...");

    fetch("/api/image/", {
        method: "POST",
        body: formData
    })
    .then(res => res.blob())
    .then(blob => {
        player.src = URL.createObjectURL(blob);
        player.play();
        hideLoader("✅ Tayyor!");
    })
    .catch(() => hideLoader("❌ Xatolik"));
}

// PLAYER
function playAudio() { player.play(); }
function pauseAudio() { player.pause(); }
function restartAudio() { player.currentTime = 0; player.play(); }
function rewind() { player.currentTime -= 5; }
function forward() { player.currentTime += 5; }
function changeSpeed(speed) { player.playbackRate = speed; }

// Keyboard
document.addEventListener("keydown", function(e) {
    if (e.code === "Space") {
        e.preventDefault();
        player.paused ? player.play() : player.pause();
    }
});