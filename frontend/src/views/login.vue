<template>
  <div class="login-wrapper d-flex flex-column min-vh-100">
    <!-- Navbar -->
    <nav class="navbar navbar-dark bg-transparent px-4 pt-3">
      <span class="navbar-brand mb-0 h1 fw-bold display-6 gradient-text">Quiz Nation</span>
    </nav>

    <!-- Login Form Centered -->
    <div class="flex-grow-1 d-flex align-items-center justify-content-center">
      <div class="glass-card p-4 rounded-4 shadow-lg">
        <div class="text-center mb-4">
          <h1 class="fw-bold text-primary">Quiz Master</h1>
          <p class="text-light">Welcome back! Please login</p>
        </div>

        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label for="email" class="form-label text-white">Email Address</label>
            <input
              type="email"
              class="form-control rounded-3 bg-light bg-opacity-75"
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
              class="form-control rounded-3 bg-light bg-opacity-75"
              id="password"
              v-model="password"
              placeholder="Enter password"
              required
            />
          </div>

          <div class="d-grid mt-4">
            <button type="submit" class="btn btn-primary btn-lg rounded-3">Login</button>
          </div>
        </form>

        <div v-if="flashMessages.length" class="alert alert-danger mt-3 text-center rounded-3">
          <ul class="mb-0 list-unstyled">
            <li v-for="(message, index) in flashMessages" :key="index">{{ message }}</li>
          </ul>
        </div>

        <div class="text-center mt-4 text-white">
          <span>New here ? </span>
          <router-link to="/signup" class="fw-bold text-warning text-decoration-none"> Create an account</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { loginUser } from '@/services/authService';

export default {
  data() {
    return {
      email: '',
      password: '',
      flashMessages: [],
    };
  },
  methods: {
    async handleLogin() {
      this.flashMessages = [];
      try {
        const user = await loginUser(this.email, this.password);
        if (user.role === 'admin') {
          this.$router.push('/admin/admindashboard');
        } else if (user.role === 'user') {
          this.$router.push('/users/userdashboard');
        } else {
          this.flashMessages = ['Unknown role: access denied'];
        }
      } catch (error) {
        this.flashMessages = [error.message || 'Login failed'];
      }
    },
  },
};
</script>

<style scoped>
.login-wrapper {
  background: url("@/assets/images/19629.jpg") no-repeat center center fixed;
  background-size: cover;
  overflow: hidden;
}

.glass-card {
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  width: 100%;
  max-width: 420px;
}
.gradient-text {
  background: linear-gradient(45deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
