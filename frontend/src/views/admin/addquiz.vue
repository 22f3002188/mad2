<template>
  <div class="add-quiz-page d-flex justify-content-center align-items-center min-vh-100">
    <div class="container">
      <div class="card shadow p-4">
        <div class="card-header bg-success text-white text-center">
          <h3 class="mb-0">Add New Quiz</h3>
        </div>
        <form @submit.prevent="submitQuiz" class="card-body bg-white">
          <div class="mb-3">
            <label class="form-label fw-bold">Quiz Name</label>
            <input v-model="quiz_name" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label fw-bold">Date</label>
            <input v-model="date_of_quiz" type="date" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label fw-bold">Duration (e.g. 30 mins)</label>
            <input v-model="time_duration" type="text" class="form-control" required />
          </div>
          <div class="d-flex justify-content-center gap-3">
            <button type="submit" class="btn btn-success">Save</button>
            <button @click="cancel" type="button" class="btn btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { addQuiz } from '@/services/authService';

export default {
  data() {
    return {
      quiz_name: '',
      date_of_quiz: '',
      time_duration: ''
    };
  },
  methods: {
    async submitQuiz() {
      const chapterId = this.$route.params.chapterId;
      try {
        await addQuiz(chapterId, {
          quiz_name: this.quiz_name,
          date_of_quiz: this.date_of_quiz,
          time_duration: this.time_duration
        });
        this.$router.push(`/admin/chapters/${chapterId}/viewquiz`);
      } catch (err) {
        alert('Failed to add quiz');
        console.error(err);
      }
    },
    cancel() {
      const chapterId = this.$route.params.chapterId;
      this.$router.push(`/admin/chapters/${chapterId}/viewquiz`);
    }
  }
};
</script>

<style scoped>
.add-quiz-page {
  background-color: #ffe6f0;
  padding: 40px 0;
  min-height: 100vh;
}
.card-header {
  border-radius: 16px 16px 0 0;
}
</style>
