<template>
  <div class="userscores-page">
    <navbar />

    <div class="container my-5">
      <div class="card shadow border-0">
        <div class="card-header bg-primary text-white text-center fs-4 fw-bold">
          User Scores
        </div>

        <div class="card-body p-0">
          <table class="table table-bordered text-center mb-0 align-middle">
            <thead class="table-light">
              <tr>
                <th>Quiz Name</th>
                <th>Chapter Name</th>
                <th>Subject Name</th>
                <th>Date Attempted</th>
                <th>Score Percentage</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="score in scores" :key="score.id">
                <td>{{ score.quiz_name }}</td>
                <td>{{ score.chapter_name }}</td>
                <td>{{ score.subject_name }}</td>
                <td>{{ formatDate(score.date_attempt) }}</td>
                <td>{{ score.score }}</td>
              </tr>

              <tr v-if="scores.length === 0">
                <td colspan="5" class="text-muted py-4">No scores found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navbar from './navbar.vue'; // adjust path if needed
import { getUserScores } from '@/services/authService';

export default {
  name: 'UserScores',
  components: { navbar },
  data() {
    return {
      scores: [],
    };
  },
  methods: {
    async fetchScores() {
      try {
        const data = await getUserScores();
        // data is { scores: [...] }
        this.scores = data.scores.map(s => ({
          id: s.id,
          score: s.score,
          date_attempt: s.date_attempt,
          quiz_name: s.quiz_name,
          chapter_name: s.chapter,
          subject_name: s.subject,
        }));
      } catch (error) {
        console.error('Error loading scores:', error);
        this.scores = [];
      }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString();
    },
  },
  mounted() {
    this.fetchScores();
  },
};
</script>

<style scoped>
.userscores-page {
  background-color: #ffe6f0; /* soft pink full screen */
  min-height: 100vh;
  padding-top: 30px;
}

.card {
  background-color: #fff0f5; /* lighter pink card */
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-radius: 16px 16px 0 0;
  background-color: #147efb !important; /* same bold blue as dashboard */
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.card-body {
  background-color: #fff0f5;
}

.table th,
.table td {
  vertical-align: middle;
  font-size: 0.95rem;
}

.table thead {
  background-color: #ffeaf4; /* soft pink table head */
}

.table-striped > tbody > tr:nth-of-type(odd) {
  background-color: #fff8fc;
}

.text-muted {
  font-style: italic;
  font-weight: 500;
  font-size: 1.1rem;
}
</style>
