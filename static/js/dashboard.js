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
      if (!res.ok) { trainMsg.innerText = "Error fetching training status"; return null; }
      const data = await res.json();
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
        if (!start.ok) { alert("Failed to start training"); trainBtn.disabled = false; return; }
        const interval = setInterval(async () => {
          const status = await pollStatus();
          if (status && status.progress >= 100) {
            clearInterval(interval);
            trainBtn.disabled = false;
            trainMsg.innerText = "Training completed successfully ✅";
            loadStats();
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
  // LOAD STATS + ACTIVITY FEED
  // ===============================
  async function loadStats() {
    try {
      const res = await fetch("/attendance_stats");
      const data = await res.json();

      const el1 = document.getElementById("totalStudents");
      const el2 = document.getElementById("attendanceToday");
      const el3 = document.getElementById("totalClasses");
      const feed = document.getElementById("recentActivityList");

      if (el1) el1.innerText = data.total_students ?? 0;
      if (el2) el2.innerText = data.present_today  ?? 0;
      if (el3) el3.innerText = data.active_classes ?? 0;

      if (feed) {
        if (data.recent_logs && data.recent_logs.length > 0) {
          feed.innerHTML = data.recent_logs.map(r => `
            <div class="activity-row">
              <div style="display:flex;align-items:center;gap:10px;">
                <div class="activity-avatar">${r.name ? r.name[0] : '?'}</div>
                <div>
                  <div style="font-size:13px;font-weight:600;color:#c8d0e0;">${r.name}</div>
                  <div style="font-size:11px;color:#3a4060;font-family:'JetBrains Mono',monospace;">
                    ${r.timestamp ? r.timestamp.slice(0,10) : ''} · ${r.timestamp ? r.timestamp.slice(11,19) : ''}
                  </div>
                </div>
              </div>
              <span class="badge-id">IDENTIFIED</span>
            </div>
          `).join('');
        } else {
          feed.innerHTML = '<p style="color:#3a4060;font-size:12px;font-family:\'JetBrains Mono\',monospace;">NO_RECENT_ACTIVITY</p>';
        }
      }
    } catch(e) {
      console.error("Stats error:", e);
    }
  }

  // ===============================
  // ATTENDANCE CHART
  // ===============================
  async function updateChart() {
    try {
      const res = await fetch("/attendance_stats");
      if (!res.ok) { console.warn("attendance_stats route not found"); return; }
      const data = await res.json();

      const canvas = document.getElementById("attendanceChart");
      if (!canvas) return;

      const ctx = canvas.getContext("2d");
      const gradient = ctx.createLinearGradient(0, 0, 0, 220);
      gradient.addColorStop(0, "rgba(34, 211, 238, 0.4)");
      gradient.addColorStop(1, "rgba(34, 211, 238, 0.0)");

      if (!chart) {
        chart = new Chart(ctx, {
          type: "line",
          data: {
            labels: data.dates || [],
            datasets: [{
              label: "Attendance",
              data: data.counts || [],
              borderColor: "#22d3ee",
              backgroundColor: gradient,
              borderWidth: 2,
              pointBackgroundColor: "#22d3ee",
              pointBorderColor: "#12141c",
              pointBorderWidth: 2,
              pointRadius: 4,
              fill: true,
              tension: 0.1
            }],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              x: {
                grid: { color: "rgba(255, 255, 255, 0.05)" },
                ticks: { color: "#5a6480", font: { family: "'JetBrains Mono', monospace", size: 10 } }
              },
              y: {
                beginAtZero: true,
                grid: { color: "rgba(255, 255, 255, 0.05)" },
                ticks: { color: "#5a6480", precision: 0, stepSize: 1, font: { family: "'JetBrains Mono', monospace", size: 10 } },
              },
            },
          },
        });
      } else {
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
  loadStats();
  updateChart();

  // Auto refresh every 10 sec
  setInterval(loadStats, 10000);
  setInterval(updateChart, 10000);

}); // end DOMContentLoaded