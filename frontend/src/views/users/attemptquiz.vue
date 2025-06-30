<template>
  <div class="container mt-5">
    <h2 class="text-center">Quiz Attempt - {{ quiz.quiz_name || 'Loading...' }}</h2>
    <h5 class="text-center text-muted" v-if="quiz.chapter">
      Subject: {{ quiz.chapter.subject_name }} | Chapter: {{ quiz.chapter.name }}
    </h5>
    <h6 class="text-center text-primary" v-if="quiz.date_of_quiz">
      Date of Quiz: {{ formatDate(quiz.date_of_quiz) }}
    </h6>

    <div v-if="timeLeft !== null" class="text-center my-3">
      <h4>Time Left: {{ formattedTimeLeft }}</h4>
    </div>

    <form @submit.prevent="submitQuiz" v-if="questions.length > 0">
      <div v-for="(question, index) in questions" :key="question.id" class="card mt-3">
        <div class="card-body">
          <h5 class="card-title">Q{{ index + 1 }}: {{ question.question_statement }}</h5>
          <div class="form-check" v-for="opt in questionOptions(question)" :key="opt">
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

    <div v-else class="text-center mt-4">
      Loading questions...
    </div>
  </div>
</template>

<script>
import api from '@/services/api'; // Your axios or fetch wrapper

export default {
  name: 'AttemptQuiz',
  data() {
    return {
      quiz: {},
      questions: [],
      answers: {},   // To store user answers keyed by question.id
      timeLeft: null, // in seconds
      timerInterval: null,
    };
  },
  computed: {
    formattedTimeLeft() {
      if (this.timeLeft === null) return '';
      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      if (isNaN(date.getTime())) {
        console.warn('Invalid date:', dateStr);
        return '';
      }
      return date.toISOString().split('T')[0];
    },

    questionOptions(question) {
      // Return options filtering out null or empty strings
      return [question.option1, question.option2, question.option3, question.option4].filter(
        opt => opt && opt.trim() !== ''
      );
    },

    async fetchQuizData() {
      try {
        const quizId = this.$route.params.quizId;
        const response = await api.get(`/api/user/quiz/${quizId}`, true);
        this.quiz = response.quiz;
        this.questions = response.questions;

        // Start timer in seconds, convert from e.g. '15:00' (mm:ss) or '00:15:00' (hh:mm:ss)
        this.startTimer(this.parseDurationToSeconds(this.quiz.time_duration));
      } catch (error) {
        console.error('Failed to load quiz data:', error.message);
      }
    },

    parseDurationToSeconds(durationStr) {
    if (!durationStr) return 900; // default 15 min

    // If duration is a simple number (no colon), treat as minutes
    if (!durationStr.includes(':')) {
        const minutes = Number(durationStr);
        if (!isNaN(minutes)) {
        return minutes * 60;
        }
        return 900; // fallback
    }

    // If duration includes colon, parse hh:mm:ss or mm:ss
    const parts = durationStr.split(':').map(Number);
    if (parts.length === 2) {
        // mm:ss
        return parts[0] * 60 + parts[1];
    } else if (parts.length === 3) {
        // hh:mm:ss
        return parts[0] * 3600 + parts[1] * 60 + parts[2];
    }

    return 900; // fallback 15 minutes
    },


    startTimer(seconds) {
      this.timeLeft = seconds;

      this.timerInterval = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
        } else {
          clearInterval(this.timerInterval);
          alert('Time is up! Submitting quiz...');
          this.submitQuiz();
        }
      }, 1000);
    },

    submitQuiz() {
      clearInterval(this.timerInterval);

      // Here you can process answers and submit to backend
      // For demo just log answers and redirect or show message

      console.log('User answers:', this.answers);
      alert('Quiz submitted! (You can now implement actual submission.)');

      // Optionally redirect user back or show results
      this.$router.push({ name: 'UserDashboard' });
    }
  },
  mounted() {
    this.fetchQuizData();
  },
  beforeUnmount() {
    clearInterval(this.timerInterval);
  }
};
</script>

<style scoped>
.card {
  font-size: 0.95rem;
}
</style>
