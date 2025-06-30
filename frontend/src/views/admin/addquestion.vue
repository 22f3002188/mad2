<template>
  <div class="add-question-page">
    <div class="container mt-5">
      <div class="card shadow border-0 mx-auto" style="max-width: 700px">
        <div class="card-header bg-success text-white text-center fs-4 fw-bold">
          ➕ Add Question
        </div>
        <div class="card-body">
          <form @submit.prevent="addQuestion">
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
                <option :value="question.option1" :disabled="!question.option1">
                  Option 1: {{ question.option1 }}
                </option>
                <option :value="question.option2" :disabled="!question.option2">
                  Option 2: {{ question.option2 }}
                </option>
                <option :value="question.option3" :disabled="!question.option3">
                  Option 3: {{ question.option3 }}
                </option>
                <option :value="question.option4" :disabled="!question.option4">
                  Option 4: {{ question.option4 }}
                </option>
              </select>
            </div>

            <div class="text-center">
              <button type="submit" class="btn btn-success">Add Question</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { addQuestionToQuiz } from '@/services/authService';

export default {
  name: 'AddQuestion',
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
    }
  },
  methods: {
    async addQuestion() {
      try {
        await addQuestionToQuiz(this.quizId, this.question);
        this.$router.push(`/admin/quizzes/${this.quizId}/questions`);
      } catch (error) {
        console.error('Failed to add question:', error.message);
        alert('Failed to add question');
      }
    }
  }
};
</script>

<style scoped>
.add-question-page {
  background-color: #f8f9fa;
  min-height: 100vh;
}
</style>
