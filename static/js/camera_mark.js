

/* ===============================
   STOP MARKING
================================ */
stopMarkBtn.addEventListener("click", () => {
  if (markInterval) clearInterval(markInterval);
  if (markStream) {
    markStream.getTracks().forEach(t => t.stop());
  }

  startMarkBtn.disabled = false;
  stopMarkBtn.disabled = true;
  markStatus.innerText = "Stopped";
});

/* ===============================
   CAPTURE + RECOGNIZE
================================ */
async function captureAndRecognize() {
  const canvas = document.createElement("canvas");
  canvas.width = markVideo.videoWidth || 640;
  canvas.height = markVideo.videoHeight || 480;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(markVideo, 0, 0, canvas.width, canvas.height);

  const blob = await new Promise(resolve =>
    canvas.toBlob(resolve, "image/jpeg", 0.85)
  );

  const fd = new FormData();
  fd.append("image", blob, "snap.jpg");

  try {
    const res = await fetch("/recognize_face", {
      method: "POST",
      body: fd
    });

    const j = await res.json();

    if (j.recognized) {
      markStatus.innerText =
        `Recognized: ${j.name} (conf ${Math.round(j.confidence * 100)}%)`;

      if (!recognizedIds.has(j.student_id)) {
        recognizedIds.add(j.student_id);

        const li = document.createElement("li");
        li.className = "list-group-item";
        li.innerText = `${j.name} - ${new Date().toLocaleTimeString()}`;
        recognizedList.prepend(li);
      }
    } else {
      if (j.error) {
        markStatus.innerText = `Not recognized: ${j.error}`;
      } else {
        markStatus.innerText = "Not recognized_attach";
      }
    }

  } catch (err) {
    console.error(err);
  }
}
const markVideo = document.getElementById("markVideo");
const startMarkBtn = document.getElementById("startMarkBtn");
const stopMarkBtn = document.getElementById("stopMarkBtn");
const markStatus = document.getElementById("markStatus");
const recognizedList = document.getElementById("recognizedList");

let markStream = null;
let markInterval = null;
let recognizedIds = new Set();

/* ===============================
   START MARKING
================================ */
startMarkBtn.addEventListener("click", async () => {
  try {
    markStream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false
    });

    markVideo.srcObject = markStream;
    await markVideo.play();

    startMarkBtn.disabled = true;
    stopMarkBtn.disabled = false;
    markStatus.innerText = "Camera started. Recognizing...";

    recognizedIds.clear();
    recognizedList.innerHTML = "";

    markInterval = setInterval(captureAndRecognize, 2000);

  } catch (err) {
    console.error(err);
    markStatus.innerText = "Unable to access camera";
    alert("Camera permission denied or camera not available");
  }
});