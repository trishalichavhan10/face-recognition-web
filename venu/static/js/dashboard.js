// static/js/dashboard.js

document.addEventListener("DOMContentLoaded", () => {
  const trainBtn = document.getElementById("trainBtn");
  const trainProgress = document.getElementById("trainProgress");
  const trainMsg = document.getElementById("trainMsg");

  let chart = null;

  // -------------------------------
  // Poll Training Status
  // -------------------------------
  async function pollStatus() {
    try {
      const res = await fetch("/train_status");
      const data = await res.json();

      trainProgress.style.width = data.progress + "%";
      trainProgress.innerText = data.progress + "%";
      trainMsg.innerText = data.message;

      return data;
    } catch (err) {
      console.error(err);
      return null;
    }
  }

  // -------------------------------
  // Start Training
  // -------------------------------
  trainBtn.addEventListener("click", async () => {
    trainBtn.disabled = true;
    trainMsg.innerText = "Training started...";

    const start = await fetch("/train_model");

    if (!start.ok) {
      alert("Failed to start training");
      trainBtn.disabled = false;
      return;
    }

    const interval = setInterval(async () => {
      const status = await pollStatus();

      if (status && status.progress >= 100) {
        clearInterval(interval);
        trainBtn.disabled = false;
        alert("Training completed");
      }
    }, 1500);
  });

  // -------------------------------
  // Attendance Chart
  // -------------------------------
  async function updateChart() {
    const res = await fetch("/attendance_stats");
    const data = await res.json();

    const ctx = document
      .getElementById("attendanceChart")
      .getContext("2d");

    if (!chart) {
      chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: data.dates,
          datasets: [
            {
              label: "Attendance",
              data: data.counts,
              backgroundColor: "rgba(54, 162, 235, 0.6)",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    } else {
      chart.data.labels = data.dates;
      chart.data.datasets[0].data = data.counts;
      chart.update();
    }
  }

  updateChart();
  setInterval(updateChart, 10000);
});
