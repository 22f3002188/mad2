<template>
  <div class="auth-background d-flex flex-column min-vh-100">
    <!-- Navbar / Title -->
    <nav class="navbar navbar-dark bg-transparent px-4 pt-3">
      <span class="navbar-brand mb-0 h1 fw-bold display-6 gradient-text">Quiz Nation</span>
    </nav>

    <!-- Signup Form -->
    <div class="flex-grow-1 d-flex align-items-center justify-content-center">
      <div class="glass-card p-4 shadow-lg rounded-4">
        <div class="text-center mb-3">
          <h1 class="fw-bold text-danger">Quiz Master</h1>
          <h3 class="mt-2 text-white">Signup</h3>
        </div>

        <form @submit.prevent="handleSignup">
          <div class="mb-3">
            <label for="email" class="form-label text-white">User Name (E-mail)</label>
            <input
              type="email"
              class="form-control bg-light bg-opacity-75"
              id="email"
              v-model="email"
              placeholder="you@example.com"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label text-white">Password</label>
            <input
              type="password"
              class="form-control bg-light bg-opacity-75"
              id="password"
              v-model="password"
              placeholder="Enter password"
              required
            />
          </div>
          <div class="mb-3">
            <label for="full_name" class="form-label text-white">Full Name</label>
            <input
              type="text"
              class="form-control bg-light bg-opacity-75"
              id="full_name"
              v-model="fullName"
              placeholder="John Doe"
              required
            />
          </div>
          <div class="mb-3">
            <label for="qualification" class="form-label text-white">Qualification</label>
            <input
              type="text"
              class="form-control bg-light bg-opacity-75"
              id="qualification"
              v-model="qualification"
              placeholder="e.g. B.Tech in CSE"
              required
            />
          </div>
          <div class="mb-3">
            <label for="dob" class="form-label text-white">Date of Birth</label>
            <input
              type="date"
              class="form-control bg-light bg-opacity-75"
              id="dob"
              v-model="dob"
              required
            />
          </div>
          <div class="d-grid mt-3">
            <button type="submit" class="btn btn-danger btn-lg rounded-3">Signup</button>
          </div>
        </form>

        <!-- Flash messages -->
        <div v-if="flashMessages.length" class="alert alert-danger mt-3 text-center rounded-3">
          <ul class="mb-0 list-unstyled">
            <li v-for="(message, index) in flashMessages" :key="index">{{ message }}</li>
          </ul>
        </div>

        <div class="text-center mt-4 text-white">
          Already have an account ?
          <router-link to="/login" class="fw-bold text-warning text-decoration-none">Login</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { registerUser } from '@/services/authService';

export default {
  data() {
    return {
      email: '',
      password: '',
      fullName: '',
      qualification: '',
      dob: '',
      flashMessages: [],
    };
  },
  methods: {
    async handleSignup() {
      this.flashMessages = [];
      try {
        await registerUser({
          email: this.email,
          password: this.password,
          full_name: this.fullName,
          qualification: this.qualification,
          dob: this.dob,
        });
        alert('Signup successful! Please log in.');
        this.$router.push('/login');
      } catch (error) {
        this.flashMessages = [error.message || 'Signup failed. Please try again.'];
      }
    },
  },
};
</script>

<style scoped>
.auth-background {
  background: url("@/assets/images/19629.jpg") no-repeat center center fixed;
  background-size: cover;
  overflow: hidden;
}

.glass-card {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  width: 100%;
  max-width: 500px;
}

.gradient-text {
  background: linear-gradient(45deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
