<template>
  <div class="quiz-page">
    <navbar />
    <div class="container mt-5">
      <div class="card shadow border-0">
        <div class="card-header bg-primary text-white text-center fs-4 fw-bold">
          Quizzes for {{ chapterName }}
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover table-bordered text-center">
              <thead class="table-dark">
                <tr>
                  <th>ID</th>
                  <th>Quiz Name</th>
                  <th>Date</th>
                  <th>Duration</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="quiz in quizzes" :key="quiz.id">
                  <td class="fw-bold">{{ quiz.id }}</td>
                  <td>{{ quiz.quiz_name }}</td>
                  <td>{{ formatDate(quiz.date_of_quiz) }}</td>
                  <td>{{ quiz.time_duration }}</td>
                  <td>
                    <div class="d-flex justify-content-center gap-2">
                      <button class="btn btn-outline-info btn-sm" @click="$router.push(`/admin/quizzes/${quiz.id}/questions`)">View Questions</button>
                      <button class="btn btn-outline-warning btn-sm" @click="$router.push(`/admin/chapters/${$route.params.chapterId}/quizzes/${quiz.id}/edit`)">Edit</button>
                      <button class="btn btn-outline-danger btn-sm" @click="handleDeleteQuiz(quiz.id)">Delete</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="text-center my-3"><router-link :to="`/admin/chapters/${$route.params.chapterId}/addquiz`" class="btn btn-success btn-lg shadow"> Add Quiz</router-link>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navbar from './navbar.vue';
import { getQuizzesByChapter } from '@/services/authService';
import { deleteQuiz } from '@/services/authService';

export default {
  components: { navbar },
  data() {
    return {
      chapterName: '',
      quizzes: []
    };
  },
  methods: {
    async fetchQuizzes() {
      const chapterId = this.$route.params.chapterId;
      try {
        const res = await getQuizzesByChapter(chapterId);
        this.quizzes = res.quizzes;
        this.chapterName = res.chapter_name;
      } catch (err) {
        console.error("Failed to fetch quizzes:", err.message);
      }
    },
    async handleDeleteQuiz(quizId) {
      const chapterId = this.$route.params.chapterId;
      if (confirm("Are you sure you want to delete this quiz?")) {
        try {
          await deleteQuiz(chapterId, quizId);
          await this.fetchQuizzes(); // Refresh list
        } catch (err) {
          console.error("Delete failed:", err.message);
          alert("Failed to delete quiz");
        }
      }
    },
    formatDate(dateStr) {
      const d = new Date(dateStr);
      return d.toISOString().split('T')[0];
    }
  },
  mounted() {
    this.fetchQuizzes();
  }
};
</script>

<style scoped>
.quiz-page {
  background-color: #ffe6f0;
  min-height: 100vh;
}
.card-header {
  background-color: #147efb !important;
  color: white;
}
</style>
