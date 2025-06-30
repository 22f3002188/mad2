<template>
  <div class="edit-question-page">
    <div class="container mt-5">
      <div class="card shadow border-0 mx-auto" style="max-width: 700px">
        <div class="card-header bg-warning text-white text-center fs-4 fw-bold">
          ✏️ Edit Question
        </div>
        <div class="card-body">
          <form @submit.prevent="updateQuestion">
            <div class="mb-3">
              <label class="form-label">Question Statement</label>
              <textarea v-model="question.question_statement" class="form-control" required></textarea>
            </div>

            <div v-for="n in 4" :key="n" class="mb-3">
              <label class="form-label">Option {{ n }}</label>
              <input
                v-model="question[`option${n}`]"
                type="text"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Correct Answer</label>
              <select v-model="question.correct_answer" class="form-select" required>
                <option disabled value="">-- Select Correct Answer --</option>
                <option :value="question.option1" :disabled="!question.option1">Option 1: {{ question.option1 }}</option>
                <option :value="question.option2" :disabled="!question.option2">Option 2: {{ question.option2 }}</option>
                <option :value="question.option3" :disabled="!question.option3">Option 3: {{ question.option3 }}</option>
                <option :value="question.option4" :disabled="!question.option4">Option 4: {{ question.option4 }}</option>
              </select>
            </div>

            <div class="text-center d-flex justify-content-center gap-3">
              <button type="submit" class="btn btn-warning">Update Question</button>
              <button type="button" class="btn btn-secondary" @click="cancel">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getQuestionsByQuiz, updateQuestion } from '@/services/authService';

export default {
  name: 'EditQuestion',
  data() {
    return {
      question: {
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_answer: ''
      }
    };
  },
  computed: {
    quizId() {
      return this.$route.params.quizId;
    },
    questionId() {
      return parseInt(this.$route.params.questionId);
    }
  },
  methods: {
    async loadQuestion() {
      try {
        const res = await getQuestionsByQuiz(this.quizId);
        const found = res.questions.find(q => q.id === this.questionId);
        if (!found) {
          alert("Question not found");
          this.$router.push(`/admin/quizzes/${this.quizId}/questions`);
        } else {
          this.question = { ...found };
        }
      } catch (err) {
        console.error("Error loading question:", err.message);
      }
    },
    async updateQuestion() {
      try {
        await updateQuestion(this.quizId, this.questionId, this.question);
        this.$router.push(`/admin/quizzes/${this.quizId}/questions`);
      } catch (err) {
        console.error("Failed to update question:", err.message);
        alert("Update failed");
      }
    },
    cancel() {
      this.$router.push(`/admin/quizzes/${this.quizId}/questions`);
    }
  },
  mounted() {
    this.loadQuestion();
  }
};
</script>

<style scoped>
.edit-question-page {
  background-color: #fffbe6;
  min-height: 100vh;
  padding-top: 2rem;
  padding-bottom: 2rem;
}
</style>
