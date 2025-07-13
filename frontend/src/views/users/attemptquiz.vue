<template>
  <div class="light-yellow-bg">
    <div class="container mt-5">
      <h2 class="text-center">Quiz Attempt - {{ quiz.quiz_name || 'Loading...' }}</h2>

      <h5 class="text-center text-muted" v-if="quiz.chapter">
        Subject: {{ quiz.chapter.subject_name }} | Chapter: {{ quiz.chapter.name }}
      </h5>

      <h6 class="text-center text-primary" v-if="quiz.date_of_quiz">
        Date of Quiz: {{ formatDate(quiz.date_of_quiz) }}
      </h6>

      <!-- Timer -->
      <div v-if="timeLeft !== null && !submitted" class="text-center my-3">
        <h4>Time Left: {{ formattedTimeLeft }}</h4>
      </div>

      <!-- Quiz Form -->
      <form v-if="questions.length > 0 && !submitted" @submit.prevent="submitQuiz">
        <div
          v-for="(question, index) in questions"
          :key="question.id"
          class="card mt-3"
        >
          <div class="card-body">
            <h5 class="card-title">Q{{ index + 1 }}: {{ question.question_statement }}</h5>
            <div
              class="form-check"
              v-for="opt in questionOptions(question)"
              :key="opt"
            >
              <input
                class="form-check-input"
                type="radio"
                :name="'q' + question.id"
                :value="opt"
                v-model="answers[question.id]"
                required
              />
              <label class="form-check-label">{{ opt }}</label>
            </div>
          </div>
        </div>

        <div class="text-center mt-4">
          <button type="submit" class="btn btn-success">Submit Quiz</button>
        </div>
      </form>

      <!-- Loading -->
      <div v-else-if="!submitted" class="text-center mt-4">
        Loading questions...
      </div>

      <!-- Quiz Result -->
      <div v-if="submitted" class="text-center mt-4">
        <h3>
          Your Score: {{ computedCorrectAnswers }} / {{ totalQuestions }} ({{ score }}%)
        </h3>
        <p>{{ resultMessage }}</p>
        <button class="btn btn-primary" @click="goToDashboard">Back to Dashboard</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter, useRoute } from 'vue-router';
import { onMounted, onBeforeUnmount, reactive, ref, computed } from 'vue';
import api from '@/services/api'; // Adjust as per your actual API file

export default {
  name: 'AttemptQuiz',
  setup() {
    const router = useRouter();
    const route = useRoute();

    const quiz = reactive({});
    const questions = ref([]);
    const answers = reactive({});
    const timeLeft = ref(null);
    const timerInterval = ref(null);
    const submitted = ref(false);
    const score = ref(0); // percentage score
    const totalQuestions = ref(0);
    const resultMessage = ref('');

    const formattedTimeLeft = computed(() => {
      if (timeLeft.value === null) return '';
      const minutes = Math.floor(timeLeft.value / 60);
      const seconds = timeLeft.value % 60;
      return `${minutes.toString().padStart(2, '0')}:${seconds
        .toString()
        .padStart(2, '0')}`;
    });

    const computedCorrectAnswers = computed(() => {
      return Math.round((score.value / 100) * totalQuestions.value);
    });

    const formatDate = (dateStr) => {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      if (isNaN(date.getTime())) {
        console.warn('Invalid date:', dateStr);
        return '';
      }
      return date.toISOString().split('T')[0];
    };

    const questionOptions = (question) => {
      return [
        question.option1,
        question.option2,
        question.option3,
        question.option4,
      ].filter((opt) => opt && opt.trim() !== '');
    };

    const parseDurationToSeconds = (durationStr) => {
      if (!durationStr) return 900;
      if (!durationStr.includes(':')) {
        const minutes = Number(durationStr);
        return isNaN(minutes) ? 900 : minutes * 60;
      }
      const parts = durationStr.split(':').map(Number);
      if (parts.length === 2) return parts[0] * 60 + parts[1];
      if (parts.length === 3)
        return parts[0] * 3600 + parts[1] * 60 + parts[2];
      return 900;
    };

    const startTimer = (seconds) => {
      timeLeft.value = seconds;
      timerInterval.value = setInterval(() => {
        if (timeLeft.value > 0) {
          timeLeft.value--;
        } else {
          clearInterval(timerInterval.value);
          alert('Time is up! Submitting quiz...');
          submitQuiz();
        }
      }, 1000);
    };

    const fetchQuizData = async () => {
      try {
        const quizId = route.params.quizId;
        const response = await api.get(`/api/user/quiz/${quizId}`, true);
        Object.assign(quiz, response.quiz);
        questions.value = response.questions;
        totalQuestions.value = questions.value.length;
        startTimer(parseDurationToSeconds(quiz.time_duration));
      } catch (error) {
        console.error('Failed to load quiz data:', error.message);
      }
    };

    const submitQuiz = async () => {
      clearInterval(timerInterval.value);
      try {
        const quizId = route.params.quizId;
        const payload = { answers };
        const response = await api.post(
          `/api/user/quiz/${quizId}/submit`,
          payload,
          true
        );
        score.value = response.score;
        totalQuestions.value = response.total || totalQuestions.value;
        resultMessage.value =
          response.message || 'Quiz submitted successfully!';
        submitted.value = true;
      } catch (error) {
        console.error('Failed to submit quiz:', error.message);
        alert('Failed to submit quiz. Please try again.');
      }
    };

    const goToDashboard = () => {
      router.push({ name: 'userdashboard' });
    };

    onMounted(() => {
      fetchQuizData();
    });

    onBeforeUnmount(() => {
      clearInterval(timerInterval.value);
    });

    return {
      quiz,
      questions,
      answers,
      timeLeft,
      submitted,
      score,
      totalQuestions,
      resultMessage,
      formattedTimeLeft,
      computedCorrectAnswers,
      formatDate,
      questionOptions,
      goToDashboard,
      submitQuiz,
    };
  },
};
</script>

<style scoped>
.light-yellow-bg {
  background-color: #fff9c4;
  min-height: 100vh;
  padding-top: 20px;
  padding-bottom: 20px;
}
.card-title {
  font-weight: bold;
}
</style>
