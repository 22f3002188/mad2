<template>
  <div class="auth-background d-flex align-items-center justify-content-center min-vh-100">
    <div class="glass-card p-4 shadow-lg rounded-4">
      <div class="text-center">
        <h1 class="fw-bold text-danger">Quiz Master</h1>
        <h3 class="mt-3">Signup</h3>
      </div>
      <form @submit.prevent="handleSignup">
        <div class="mb-3">
          <label for="email" class="form-label">User Name (E-mail)</label>
          <input type="email" class="form-control" id="email" v-model="email" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" v-model="password" required>
        </div>
        <div class="mb-3">
          <label for="full_name" class="form-label">Full Name</label>
          <input type="text" class="form-control" id="full_name" v-model="fullName" required>
        </div>
        <div class="mb-3">
          <label for="qualification" class="form-label">Qualification</label>
          <input type="text" class="form-control" id="qualification" v-model="qualification" required>
        </div>
        <div class="mb-3">
          <label for="dob" class="form-label">Date of Birth</label>
          <input type="date" class="form-control" id="dob" v-model="dob" required>
        </div>
        <div class="d-grid">
          <button type="submit" class="btn btn-danger">Signup</button>
        </div>
        <div class="text-center mt-3">
          Already have an account? <router-link to="/login">Login</router-link>
        </div>
      </form>

      <div v-if="flashMessages.length" class="alert alert-danger text-center mt-3" role="alert">
        <ul>
          <li v-for="(message, index) in flashMessages" :key="index">{{ message }}</li>
        </ul>
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
  background: url("@/assets/images/sb.png") no-repeat center center fixed;
  background-size: cover;
  min-height: 100vh;
}

.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  width: 100%;
  max-width: 500px;
}
</style>
