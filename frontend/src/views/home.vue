<template>
  <div class="d-flex align-items-center justify-content-center vh-100 text-white welcome-page">
    <div class="p-5 bg-dark bg-opacity-75 rounded text-center">
      <h1>Welcome to QuizMaster</h1>
      <p>
        Challenge yourself with our exciting quizzes and test your knowledge across various subjects!
      </p>
      <p>Ready to begin? Log in to start your quiz adventure.</p>
      <router-link to="/login" class="btn btn-primary btn-lg">Log In</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<style scoped>
.welcome-page {
  background: url("@/assets/images/background.jpg") no-repeat center center fixed;
  background-size: cover;
}
</style>

<!-- Bootstrap JS is typically included globally in main.js or index.html -->
