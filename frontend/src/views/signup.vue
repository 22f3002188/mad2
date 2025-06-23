<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card p-4">
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
      try {
        const response = await fetch('http://127.0.0.1:5000/api/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            full_name: this.fullName,
            qualification: this.qualification,
            dob: this.dob,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          alert("Signup successful! Please log in.");
          this.$router.push('/login'); // Navigate to login page
        } else {
          const errorData = await response.json();
          this.flashMessages = [errorData.error || "Signup failed. Please try again."];
        }
      } catch (error) {
        this.flashMessages = ['Network error. Please try again later.'];
      }
    },
  },
};
</script>

<style scoped>
body {
  background-color: #f8f9fa;
}
</style>
