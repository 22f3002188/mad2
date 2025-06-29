<template>
  <div class="welcome-page text-white">
    <!-- Top Welcome Section -->
    <div class="vh-100 d-flex align-items-center justify-content-center">
      <div class="p-5 bg-dark bg-opacity-75 rounded-4 text-center shadow-lg w-100" style="max-width: 650px;">
        <!-- Moving Heading Inside Bounded Box -->
        <div class="overflow-hidden position-relative">
          <h1 class="display-5 fw-bold text-nowrap move-heading">
            Welcome to <span class="text-warning">Quiz Nation</span>
          </h1>
        </div>
        <p class="lead mt-3">
          Challenge yourself with exciting quizzes and test your knowledge across various subjects!
        </p>
        <p class="fw-semibold">Ready to begin ? Log in to start your quiz adventure.</p>
        <router-link to="/login" class="btn btn-primary btn-lg mt-2">Log In</router-link>
      </div>
    </div>

    <!-- Why Quiz Nation Section -->
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-10 bg-dark bg-opacity-75 p-4 rounded shadow text-center fade-in-section">
          <h2 class="fw-bold mb-3 text-warning">Why Quiz Nation ?</h2>
          <p class="fs-5 text-light">
            Quiz Nation is your smart companion for academic excellence. With subject-wise quizzes, instant result,
            timed challenges, and performance analytics, it’s designed to help students learn, revise, and succeed.
          </p>
          <p class="fs-6 text-secondary">
            Whether you're preparing for exams or just love testing your knowledge, Quiz Nation is the place for you.
          </p>
        </div>
      </div>
    </div>

    <!-- Developer Info Section -->
    <div class="container pb-5">
      <div class="row justify-content-center">
        <div class="col-md-8 bg-secondary bg-opacity-75 text-white p-4 rounded shadow text-center fade-in-section">
          <h4 class="fw-bold mb-3 text-white">Developer Information</h4>
          <ul class="list-unstyled fs-6">
            <li><strong>Name:</strong> Harsh Jayswal</li>
            <li><strong>Roll No:</strong> 22F3002188</li>
            <li><strong>Email:</strong> harsh.jayswal.iitm@gmail.com</li>
            <li><strong>Contact:</strong> xxxxxxxxxx</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-dark text-center text-white py-3 border-top border-secondary">
      <small>&copy; 2025 Quiz Nation. All rights reserved.</small>
    </footer>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  mounted() {
    const reveal = () => {
      const sections = document.querySelectorAll('.fade-in-section');
      const triggerBottom = window.innerHeight * 0.85;
      sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top;
        if (sectionTop < triggerBottom) {
          section.classList.add('visible');
        }
      });
    };
    window.addEventListener('scroll', reveal);
    reveal();
  }
};
</script>

<style scoped>
.welcome-page {
  background: url("@/assets/images/background.jpg") no-repeat center center fixed;
  background-size: cover;
  overflow-x: hidden;
}

/* Moving Heading Confined Inside Block */
.move-heading {
  display: inline-block;
  white-space: nowrap;
  animation: slideInside 6s linear infinite;
  position: relative;
}

@keyframes slideInside {
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(10%);
  }
  100% {
    transform: translateX(-100%);
  }
}

/* Scroll-in reveal effect */
.fade-in-section {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 1s ease-out, transform 1s ease-out;
}

.fade-in-section.visible {
  opacity: 1;
  transform: translateY(0);
}
</style>
