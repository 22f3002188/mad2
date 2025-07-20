<template>
  <nav class="navbar navbar-expand-lg navbar-dark quiz-navbar shadow-sm py-3">
    <div class="container">
      <!-- Brand -->
      <router-link class="navbar-brand fw-bold fs-3 gradient-brand" to="/">
        Quiz Nation
      </router-link>

      <!-- Toggle -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Nav Links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto d-flex gap-2">
          <li class="nav-item">
            <router-link class="nav-link nav-tab" to="/users/userdashboard">
              <i class="bi bi-house-door-fill me-1"></i> Home
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link nav-tab" to="/users/userscores">
              <i class="bi bi-graph-up-arrow me-1"></i> Scores
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link nav-tab" to="/users/usersummary">
              <i class="bi bi-journal-text me-1"></i> Summary
            </router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link nav-tab" href="#" @click="logout">
              <i class="bi bi-box-arrow-right me-1"></i> Logout
            </a>
          </li>
        </ul>

        <!-- User name -->
        <span class="navbar-text text-white fw-semibold ms-3 d-none d-lg-block">
          Welcome, {{ fullName }}
        </span>
      </div>
    </div>
  </nav>
</template>

<script>
import { logoutUser } from '@/services/authService';

export default {
  data() {
    return { query: '', fullName: '' };
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem('user'));
    this.fullName = user?.full_name || '';
  },
  methods: {
    async logout() {
      try {
        await logoutUser();
      } catch (error) {
        console.error('Logout failed:', error.message);
      }
      this.$router.push('/login');
    },
  }
};
</script>

<style scoped>
/* Gradient navbar background */
.quiz-navbar {
  background: linear-gradient(to right, #9333ea, #ec4899);
  border-bottom: 2px solid #fbcfe8;
}

/* Brand with gradient text */
.gradient-brand {
  background: linear-gradient(45deg, #f472b6, #e879f9);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Unified nav-tab style */
.nav-tab {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 1.5rem;
  font-weight: 500;
  color: white !important;
  transition: all 0.2s ease-in-out;
}
.nav-tab:hover,
.router-link-exact-active.nav-tab {
  background-color: rgba(255, 255, 255, 0.25);
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.3);
}
</style>
