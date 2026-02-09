

// camera_add_student.js

const saveInfoBtn = document.getElementById("saveInfoBtn");
const startCaptureBtn = document.getElementById("startCaptureBtn");
const video = document.getElementById("video");
const captureStatus = document.getElementById("captureStatus");
const progressBar = document.getElementById("progressBar");

let student_id = null;
let captured = 0;
const maxImages = 50;
let images = [];
let stream = null;

/* ===============================
   SAVE STUDENT INFO
================================ */
document.getElementById("studentForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const fd = new FormData(e.target); // ✅ FULL FORM DATA

    const res = await fetch("/add_student", {
      method: "POST",
      body: fd
    });

    if (!res.ok) {
      alert("Failed to save student info");
      return;
    }

    const j = await res.json();
    student_id = data.student_id;

    alert("Student saved. Click Start Capture");
    startCaptureBtn.disabled = false;
});
  
/* ===============================
   START CAMERA
================================ */
startCaptureBtn.addEventListener("click", async () => {
  startCaptureBtn.disabled = true;
  captured = 0;
  progressBar.max = maxImages;
  progressBar.value = 0;

  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480 }
    });

    video.srcObject = stream;
    await video.play();
    captureImagesLoop();

  } catch (err) {
    alert("Camera error: " + err.message);
    startCaptureBtn.disabled = false;
  }
});

/* ===============================
   CAPTURE IMAGES LOOP
================================ */
async function captureImagesLoop() {
  if (captured >= maxImages) {
    captureStatus.innerText = "Capture Completed ✅";
    stream.getTracks().forEach(track => track.stop());
    return;
  }

  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);


    }const fd = new FormData(); // ✅ SAME LINE

fd.append("image", blob, `img_${captured}.jpg`); // ✅ backticks

fd.append("student_id", student_id); // ✅ comma added

canvas.toBlob(async (blob) => {
  const fd = new FormData();

  fd.append("image", blob, `img_${captured}.jpg`);
  fd.append("student_id", student_id);

  try {
    await fetch("/save_image", {
      method: "POST",
      body: fd
    });

    captured++;
    progressBar.value = captured;

    setTimeout(captureImagesLoop, 300);

  } catch (err) {
    console.error(err);
  }
}, "image/jpeg");
