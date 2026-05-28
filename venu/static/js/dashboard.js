// static/js/dashboard.js

let chart = null;

// =============================================
// TRAIN MODEL  (called from onclick in HTML)
// =============================================
async function trainModel() {
  const btn      = document.getElementById("trainBtn");
  const progress = document.getElementById("trainProgress");
  const msg      = document.getElementById("trainMsg");

  if (!btn) return;
  btn.disabled = true;
  msg.innerText = "INITIATING_TRAINING ...";

  try {
    const start = await fetch("/train_model");
    if (!start.ok) {
      msg.innerText = "ERROR: Failed to start training";
      btn.disabled = false;
      return;
    }

    const interval = setInterval(async () => {
      try {
        const res  = await fetch("/train_status");
        const data = await res.json();

        progress.style.width = (data.progress || 0) + "%";
        msg.innerText = data.message || "PROCESSING ...";

        if (data.progress >= 100 || !data.running) {
          clearInterval(interval);
          btn.disabled = false;
          msg.innerText = data.message || "TRAINING_COMPLETE ✅";
          progress.style.width = "100%";
        }
      } catch (e) {
        clearInterval(interval);
        btn.disabled = false;
        msg.innerText = "ERROR: Lost connection to server";
      }
    }, 1200);

  } catch (err) {
    console.error(err);
    msg.innerText = "ERROR: Server unreachable";
    btn.disabled = false;
  }
}

// =============================================
// DASHBOARD STATS  (counters + activity feed)
// =============================================
async function updateDashboardStats() {
  try {
    const res  = await fetch("/dashboard_stats");
    if (!res.ok) return;
    const data = await res.json();

    const el = id => document.getElementById(id);

    // FIX: match keys returned by /dashboard_stats route
    if (el("totalStudents"))   el("totalStudents").innerText   = data.total   ?? 0;
    if (el("attendanceToday")) el("attendanceToday").innerText = data.today   ?? 0;
    if (el("totalClasses"))    el("totalClasses").innerText    = data.classes ?? 0;

    // Recent activity list
    const list = el("recentActivityList");
    if (list) {
      if (!data.recent_activity || data.recent_activity.length === 0) {
        list.innerHTML = '<p style="color:#3a4060;font-size:12px;font-family:\'JetBrains Mono\',monospace;">NO_RECENT_ACTIVITY</p>';
      } else {
        list.innerHTML = data.recent_activity.map(act => {
          const letter = (act.name || "?")[0].toUpperCase();
          const time   = new Date(act.time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
          return `
            <div class="activity-row">
              <div style="display:flex;align-items:center;gap:10px;">
                <div class="activity-avatar">${letter}</div>
                <div>
                  <div style="font-size:13px;font-weight:600;color:#c8d0e0;">${act.name}</div>
                  <div style="font-size:11px;color:#3a4060;font-family:'JetBrains Mono',monospace;">${time}</div>
                </div>
              </div>
              <span class="badge-id">IDENTIFIED</span>
            </div>`;
        }).join("");
      }
    }

  } catch (err) {
    console.error("Dashboard stats error:", err);
  }
}

// =============================================
// ATTENDANCE CHART
// =============================================
async function updateChart() {
  try {
    const res = await fetch("/attendance_stats");
    if (!res.ok) return;
    const data = await res.json();

    const canvas = document.getElementById("attendanceChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    if (!chart) {
      chart = new Chart(ctx, {
        type: "line",
        data: {
          labels: data.dates || [],
          datasets: [{
            label: "Daily Attendance",
            data: data.counts || [],
            borderColor: "#22d3ee",
            backgroundColor: "rgba(34,211,238,0.08)",
            borderWidth: 2,
            tension: 0.35,
            fill: true,
            pointBackgroundColor: "#22d3ee",
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: "#181b26",
              titleColor: "#c8d0e0",
              bodyColor: "#4a5270",
              borderColor: "rgba(255,255,255,0.08)",
              borderWidth: 1
            }
          },
          scales: {
            x: {
              grid: { color: "rgba(255,255,255,0.04)" },
              ticks: { color: "#3a4060", font: { family: "'JetBrains Mono'" } }
            },
            y: {
              beginAtZero: true,
              grid: { color: "rgba(255,255,255,0.04)" },
              ticks: { precision: 0, color: "#3a4060", font: { family: "'JetBrains Mono'" } }
            }
          }
        }
      });
    } else {
      chart.data.labels           = data.dates  || [];
      chart.data.datasets[0].data = data.counts || [];
      chart.update();
    }
  } catch (err) {
    console.error("Chart error:", err);
  }
}

// =============================================
// INIT
// =============================================
document.addEventListener("DOMContentLoaded", () => {
  updateDashboardStats();
  updateChart();

  // Auto-refresh every 10 s
  setInterval(() => {
    updateDashboardStats();
    updateChart();
  }, 10000);
});