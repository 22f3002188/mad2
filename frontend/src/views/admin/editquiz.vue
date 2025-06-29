<template>
  <div class="edit-quiz-page">
    <navbar />
    <div class="container my-5">
      <div class="card shadow border-0 mx-auto" style="max-width: 600px">
        <div class="card-header bg-warning text-white text-center fs-4 fw-bold">
          ✏️ Edit Quiz
        </div>
        <div class="card-body">
          <form @submit.prevent="updateQuiz">
            <div class="mb-3">
              <label class="form-label fw-bold">Quiz Name</label>
              <input v-model="quiz.quiz_name" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Date of Quiz</label>
              <input v-model="quiz.date_of_quiz" type="date" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Time Duration</label>
              <input v-model="quiz.time_duration" type="text" class="form-control" required />
            </div>
            <div class="text-center">
              <button type="submit" class="btn btn-primary px-4">Update Quiz</button>
              <router-link :to="`/admin/chapters/${this.chapterId}/viewquiz`" class="btn btn-secondary ms-2">Cancel</router-link>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navbar from './navbar.vue';
import { getQuizzesByChapter, updateQuiz } from '@/services/authService';

export default {
  components: { navbar },
  data() {
    return {
      chapterId: this.$route.params.chapterId,
      quizId: parseInt(this.$route.params.quizId),
      quiz: {
        quiz_name: '',
        date_of_quiz: '',
        time_duration: ''
      }
    };
  },
  methods: {
    async fetchQuizFromChapter() {
      try {
        const res = await getQuizzesByChapter(this.chapterId);
        const quizList = res.quizzes;
        const foundQuiz = quizList.find(q => q.id === this.quizId);

        if (foundQuiz) {
          this.quiz = {
            quiz_name: foundQuiz.quiz_name,
            date_of_quiz: foundQuiz.date_of_quiz,
            time_duration: foundQuiz.time_duration
          };
        } else {
          alert("Quiz not found!");
        }
      } catch (err) {
        console.error("Failed to load quiz:", err.message);
      }
    },
    async updateQuiz() {
      try {
        await updateQuiz(this.chapterId, this.quizId, this.quiz);
        this.$router.push(`/admin/chapters/${this.chapterId}/viewquiz`);
      } catch (err) {
        console.error("Failed to update quiz:", err.message);
        alert("Update failed!");
      }
    }
  },
  mounted() {
    this.fetchQuizFromChapter();
  }
};
</script>

<style scoped>
.edit-quiz-page {
  background-color: #ffe6f0;
  min-height: 100vh;
}
.card-header {
  background-color: #f0ad4e !important;
  color: white;
}
</style>
