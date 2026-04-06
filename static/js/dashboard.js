// static/js/dashboard.js

document.addEventListener("DOMContentLoaded", () => {
  const trainBtn = document.getElementById("trainBtn");
  const trainProgress = document.getElementById("trainProgress");
  const trainMsg = document.getElementById("trainMsg");

  let chart = null;

  // ===============================
  // TRAINING STATUS POLL
  // ===============================
  async function pollStatus() {
    try {
      const res = await fetch("/train_status");

      if (!res.ok) {
        trainMsg.innerText = "Error fetching training status";
        return null;
      }

      const data = await res.json();

      // Smooth progress update
      trainProgress.style.width = data.progress + "%";
      trainProgress.innerText = data.progress + "%";

      trainMsg.innerText = data.message || "Processing...";

      return data;
    } catch (err) {
      console.error("Polling error:", err);
      trainMsg.innerText = "Server error during training";
      return null;
    }
  }

  // ===============================
  // START TRAINING
  // ===============================
  if (trainBtn) {
    trainBtn.addEventListener("click", async () => {
      trainBtn.disabled = true;
      trainMsg.innerText = "Training started...";

      try {
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
            trainMsg.innerText = "Training completed successfully ✅";
          }
        }, 1200);
      } catch (err) {
        console.error(err);
        alert("Server error");
        trainBtn.disabled = false;
      }
    });
  }

  // ===============================
  // ATTENDANCE CHART
  // ===============================
  async function updateChart() {
    try {
      const res = await fetch("/attendance_stats");

      // ⚠️ if route missing → don't crash
      if (!res.ok) {
        console.warn("attendance_stats route not found");
        return;
      }

      const data = await res.json();

      const canvas = document.getElementById("attendanceChart");
      if (!canvas) return;

      const ctx = canvas.getContext("2d");

      if (!chart) {
        chart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: data.dates || [],
            datasets: [
              {
                label: "Attendance",
                data: data.counts || [],
                backgroundColor: "rgba(59, 130, 246, 0.7)",
                borderRadius: 8,
                barThickness: 20,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
              legend: {
                display: true,
              },
            },

            scales: {
              x: {
                grid: {
                  display: false,
                },
              },
              y: {
                beginAtZero: true,
                ticks: {
                  precision: 0,
                },
              },
            },
          },
        });
      } else {
        // Update existing chart
        chart.data.labels = data.dates || [];
        chart.data.datasets[0].data = data.counts || [];
        chart.update();
      }
    } catch (err) {
      console.error("Chart error:", err);
    }
  }

  // ===============================
  // INITIAL LOAD
  // ===============================
  updateChart();

  // Auto refresh chart every 10 sec
  setInterval(updateChart, 10000);
});