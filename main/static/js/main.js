// === Fade-In Cards on Page Load ===
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card");
  cards.forEach((card, i) => {
    card.style.opacity = 0;
    card.style.transform = "translateY(20px)";
    setTimeout(() => {
      card.style.transition = "0.5s ease";
      card.style.opacity = 1;
      card.style.transform = "translateY(0)";
    }, 100 + i * 100); // Staggered animation
  });

  // === Bootstrap Toast Auto Show ===
  const toasts = document.querySelectorAll(".toast");
  toasts.forEach((toast) => {
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
  });
});

// === Attendance Confirmation Dialog ===
function confirmAttendance() {
  return confirm(
    "Are you sure you want to start face detection for attendance?"
  );
}

// === Webcam Setup and Face Capture (if elements exist) ===
const webcam =
  document.getElementById("webcam") || document.getElementById("video");
const canvas =
  document.getElementById("snapshot") || document.getElementById("canvas");
const imageInput = document.getElementById("webcam_image");

if (webcam && canvas) {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      webcam.srcObject = stream;
    })
    .catch((err) => {
      console.warn("Webcam access denied or unavailable:", err);
      alert(
        "⚠️ Webcam not accessible. Please allow permission or use upload instead."
      );
    });
}

function captureFace() {
  if (!webcam || !canvas) return alert("Webcam or canvas not found!");

  const context = canvas.getContext("2d");
  canvas.width = webcam.videoWidth;
  canvas.height = webcam.videoHeight;
  context.drawImage(webcam, 0, 0, canvas.width, canvas.height);

  if (imageInput) {
    canvas.toBlob((blob) => {
      const file = new File([blob], "face.png", { type: "image/png" });
      const dt = new DataTransfer();
      dt.items.add(file);
      imageInput.files = dt.files;
    });
  }

  canvas.style.display = "block";
  canvas.style.border = "3px solid green";
  alert("✅ Face captured successfully!");
}
