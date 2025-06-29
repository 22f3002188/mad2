<template>
  <div>
    <navbar /> 

    <div class="container mt-5">
      <h2 class="text-center">All Quizzes</h2>
      <table class="table table-striped">
        <thead class="table-dark">
          <tr>
            <th>Quiz Name</th>
            <th>Chapter</th>
            <th>Subject</th>
            <th>Duration</th>
            <th>Start Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="quiz in quizzes" :key="quiz.id">
            <td>{{ quiz.quiz_name }}</td>
            <td>{{ quiz.chapter }}</td>
            <td>{{ quiz.subject }}</td>
            <td>{{ quiz.time_duration }}</td>
            <td>{{ formatDate(quiz.date_of_quiz) }}</td>
            <td>
              <button
                v-if="isToday(quiz.date_of_quiz)"
                class="btn btn-primary"
                @click="startQuiz(quiz.id)"
              >
                Start Quiz
              </button>
              <button v-else-if="isUpcoming(quiz.date_of_quiz)" class="btn btn-warning" disabled>
                Upcoming
              </button>
              <button v-else class="btn btn-secondary" disabled>
                Expired
              </button>
            </td>
          </tr>
          <tr v-if="quizzes.length === 0">
            <td colspan="6" class="text-center">No quizzes available</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import navbar from './navbar.vue'; 

export default {
  name: 'UserDashboard',
  components: {
    navbar,
  },
  data() {
    return {
      quizzes: [],
    };
  },
  created() {
    this.fetchQuizzes();
  },
  methods: {
    async fetchQuizzes() {
      try {
        const response = await api.get('/api/user/quizzes', true); // ⬅️ uses token
        this.quizzes = response.quizzes;
      } catch (error) {
        console.error('Failed to load quizzes:', error.message);
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toISOString().split('T')[0];
    },
    isToday(dateStr) {
      const today = new Date().toISOString().split('T')[0];
      return this.formatDate(dateStr) === today;
    },
    isUpcoming(dateStr) {
      const today = new Date().toISOString().split('T')[0];
      return this.formatDate(dateStr) > today;
    },
    startQuiz(quizId) {
      this.$router.push({ name: 'AttemptQuiz', params: { quizId } }); // 👈 assumes named route exists
    },
  },
};
</script>

<style scoped>
.table {
  font-size: 0.95rem;
}
</style>
