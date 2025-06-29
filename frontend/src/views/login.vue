<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card p-4">
          <div class="text-center">
            <h1 class="fw-bold text-primary">Quiz Master</h1>
            <h3 class="mt-3">Login</h3>
          </div>
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="email" class="form-label">User Name (E-mail)</label>
              <input type="email" class="form-control" id="email" v-model="email" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <div class="d-grid">
              <button type="submit" class="btn btn-primary">Login</button>
            </div>
            <div class="text-center mt-3">
              New user? <router-link to="/signup">Signup</router-link>
            </div>
          </form>

          <!-- Flash messages -->
          <div v-if="flashMessages.length" class="alert alert-danger text-center mt-3" role="alert">
            <ul>
              <li v-for="(message, index) in flashMessages" :key="index">{{ message }}</li>
            </ul>
          </div>
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
      const user = await loginUser(this.email, this.password); // `user` includes role
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
  }
}
};
</script>


<style scoped>
body {
  background-color: #f8f9fa;
}
</style>
