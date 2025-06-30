<template>
  <div>
    <navbar />

    <div class="container mt-4 text-center">
      <h3>Quiz Statistics</h3>
      <div class="row justify-content-center mt-4">
        <div class="col-md-6">
          <h5>Subject-wise Quizzes</h5>
          <div class="chart-container">
            <canvas ref="subjectChart"></canvas>
          </div>
        </div>
        <div class="col-md-6">
          <h5>Month-wise Quiz Attempts</h5>
          <div class="chart-container">
            <canvas ref="monthChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import navbar from "./navbar.vue";  // Adjust the path as needed
import { getUserSummary } from "@/services/authService";

export default {
  name: "UserSummary",
  components: { navbar },
  setup() {
    const subjectChart = ref(null);
    const monthChart = ref(null);
    let subjectChartInstance = null;
    let monthChartInstance = null;

    const fetchData = async () => {
      try {
        const data = await getUserSummary();
        if (!data) throw new Error("No data from server");

        if (subjectChartInstance) subjectChartInstance.destroy();
        if (monthChartInstance) monthChartInstance.destroy();

        // Subject-wise Bar Chart
        subjectChartInstance = new Chart(subjectChart.value, {
          type: "bar",
          data: {
            labels: data.subject_chart_data.labels,
            datasets: [
              {
                label: "Number of Quizzes",
                data: data.subject_chart_data.quizzes,
                backgroundColor: "rgba(54, 162, 235, 0.7)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                ticks: { precision: 0 },
              },
            },
          },
        });

        // Month-wise Pie Chart
        monthChartInstance = new Chart(monthChart.value, {
          type: "pie",
          data: {
            labels: data.month_chart_data.labels,
            datasets: [
              {
                label: "Quiz Attempts",
                data: data.month_chart_data.attempts,
                backgroundColor: data.month_chart_data.labels.map(
                  () => "rgba(75, 192, 192, 0.7)"
                ),
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          },
        });
      } catch (error) {
        console.error("Failed to load summary data:", error);
      }
    };

    onMounted(() => {
      fetchData();
    });

    return { subjectChart, monthChart };
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
}
</style>
