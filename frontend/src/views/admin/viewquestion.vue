<template>
  <div class="question-page">
    <navbar />
    <div class="container mt-5">
      <div class="card shadow-lg border-0">
        <div class="card-header text-white text-center fs-4 fw-bold">
          Questions for Quiz {{ quizId }}
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover table-bordered text-center">
              <thead class="table-dark">
                <tr>
                  <th>ID</th>
                  <th>Question</th>
                  <th>Option 1</th>
                  <th>Option 2</th>
                  <th>Option 3</th>
                  <th>Option 4</th>
                  <th>Correct Answer</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody class="align-middle">
                <tr v-for="question in questions" :key="question.id" class="table-light">
                  <td class="fw-bold">{{ question.id }}</td>
                  <td>{{ question.question_statement }}</td>
                  <td>{{ question.option1 }}</td>
                  <td>{{ question.option2 }}</td>
                  <td>{{ question.option3 }}</td>
                  <td>{{ question.option4 }}</td>
                  <td class="fw-bold">{{ question.correct_answer }}</td>
                  <td>
                    <div class="d-flex justify-content-center gap-2">
                      <button @click="$router.push(`/admin/quizzes/${quizId}/questions/${question.id}/edit`)" class="btn glass-btn btn-sm text-warning">
                         Edit
                      </button>
                      <button @click="handleDelete(question.id)" class="btn glass-btn btn-sm text-danger">
                         Delete
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="text-center my-3">
            <router-link :to="`/admin/quizzes/${quizId}/questions/add`" class="btn btn-success btn-lg shadow">
              Add Question
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navbar from './navbar.vue';
import { getQuestionsByQuiz, deleteQuestion } from '@/services/authService';

export default {
  components: { navbar },
  data() {
    return {
      quizId: this.$route.params.quizId,
      questions: []
    };
  },
  methods: {
    async fetchQuestions() {
      try {
        const res = await getQuestionsByQuiz(this.quizId);
        this.questions = res.questions;
      } catch (err) {
        console.error("Failed to fetch questions:", err.message);
      }
    },
    async handleDelete(questionId) {
      if (confirm("Are you sure you want to delete this question?")) {
        try {
          await deleteQuestion(this.quizId, questionId);
          await this.fetchQuestions(); // Refresh
        } catch (err) {
          console.error("Failed to delete question:", err.message);
          alert("Delete failed");
        }
      }
    }
  },
  mounted() {
    this.fetchQuestions();
  }
};
</script>

<style scoped>
.question-page {
  background-color: #ffe6f0;
  min-height: 100vh;
}

.card-header {
  background-color: #147efb !important;
}

.glass-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: inherit;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  font-weight: 600;
}

.glass-btn:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}
</style>
