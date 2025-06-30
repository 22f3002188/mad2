<template>
  <div>
    <navbar />

    <div class="container mt-4 text-center">
      <h3>Top Scorers & User Attempts</h3>

      <div class="row justify-content-center">
        <!-- Top Scorers Chart -->
        <div class="col-md-6 d-flex justify-content-center align-items-center">
          <div class="chart-container">
            <canvas ref="topScorersChart"></canvas>
          </div>
        </div>

        <!-- User Attempts Chart -->
        <div class="col-md-6 d-flex justify-content-center align-items-center">
          <div class="chart-container">
            <canvas ref="attemptsPieChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import navbar from './navbar.vue'; 
import { getAdminSummary } from '@/services/authService';

export default {
  name: "AdminSummary",
  components: { navbar },
  setup() {
    const topScorersChart = ref(null);
    const attemptsPieChart = ref(null);
    let topScorersChartInstance = null;
    let attemptsPieChartInstance = null;

    function createOrUpdateChart(chartRef, chartInstance, config) {
      if (chartInstance) {
        chartInstance.destroy();
      }
      chartInstance = new Chart(chartRef.value.getContext("2d"), config);
      return chartInstance;
    }

    onMounted(async () => {
      try {
        const data = await getAdminSummary();
        if (!data) return;

        const { chart_data, attempt_chart_data } = data;

        // Top Scorers Bar Chart
        topScorersChartInstance = createOrUpdateChart(topScorersChart, topScorersChartInstance, {
          type: "bar",
          data: {
            labels: chart_data.labels,
            datasets: [
              {
                label: "Highest Score",
                data: chart_data.scores,
                backgroundColor: "rgba(54, 162, 235, 0.7)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true } },
            plugins: {
              tooltip: {
                callbacks: {
                  label: (ctx) =>
                    `Highest Score: ${ctx.raw} | ${chart_data.scorers[ctx.dataIndex]}`,
                },
              },
            },
          },
        });

        // User Attempts Pie Chart
        const totalAttempts = attempt_chart_data.attempts.reduce((a, b) => a + b, 0);

        attemptsPieChartInstance = createOrUpdateChart(attemptsPieChart, attemptsPieChartInstance, {
          type: "pie",
          data: {
            labels: attempt_chart_data.labels,
            datasets: [
              {
                data: attempt_chart_data.attempts,
                backgroundColor: [
                  "#FF6384",
                  "#36A2EB",
                  "#FFCE56",
                  "#4BC0C0",
                  "#9966FF",
                  "#FF9F40",
                ],
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              tooltip: {
                callbacks: {
                  label: (ctx) => {
                    const attempts = ctx.raw;
                    const percent = ((attempts / totalAttempts) * 100).toFixed(1);
                    return `Attempts: ${attempts} (${percent}%)`;
                  },
                },
              },
              datalabels: {
                formatter: (value) => {
                  return ((value / totalAttempts) * 100).toFixed(1) + "%";
                },
                color: "#fff",
                font: { weight: "bold" },
              },
            },
          },
          plugins: [ChartDataLabels],
        });
      } catch (error) {
        console.error("Error loading admin summary:", error);
      }
    });

    return { topScorersChart, attemptsPieChart };
  },
};
</script>

<style scoped>
.chart-container {
  width: 90vw;
  height: 70vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
