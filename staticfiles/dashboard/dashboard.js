let monthlyChart = null;
let clientChart = null;

async function loadMonthly() {
    const res = await fetch("/api/analytics/monthly-performance/");
    const data = await res.json();

    if (monthlyChart) monthlyChart.destroy();

    monthlyChart = new Chart(document.getElementById("monthlyChart"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Évolution",
                data: data.values,
                fill: true,
                tension: 0.4
            }]
        }
    });
}

async function loadTopClients() {
    const res = await fetch("/api/analytics/top-clients/");
    const data = await res.json();

    if (clientChart) clientChart.destroy();

    clientChart = new Chart(document.getElementById("clientsChart"), {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Clients",
                data: data.values
            }]
        }
    });
}

function refreshDashboard() {
    loadKPIs();
    loadMonthlyPerformance();
    loadTopClients();
}

document.addEventListener("DOMContentLoaded", () => {
    loadMonthly();
    loadTopClients();
});
