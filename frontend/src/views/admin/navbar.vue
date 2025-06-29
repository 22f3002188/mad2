<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">
    <div class="container">
      <a class="navbar-brand fw-bold text-white" href="#">Quiz Portal</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item"><router-link class="nav-link fw-bold text-white" to="/admindashboard">Home</router-link></li>
          <li class="nav-item"><router-link class="nav-link fw-bold text-white" to="/users">Users</router-link></li>
          <li class="nav-item"><router-link class="nav-link fw-bold text-white" to="/summary">Summary</router-link></li>
          <li class="nav-item"><a class="nav-link fw-bold text-danger" href="#" @click="logout">Logout</a></li>
        </ul>
        <form class="mb-3" @submit.prevent="search">
          <div class="input-group">
            <input v-model="query" class="form-control" placeholder="Search users, subjects, chapters, quizzes" />
            <button class="btn btn-primary" type="submit">Search</button>
          </div>
        </form>
        <span class="navbar-text text-white fw-bold ms-3">Welcome Admin</span>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return { query: '' };
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/login');
    },
    search() {
      this.$router.push({ path: '/adminsearch', query: { q: this.query } });
    }
  }
};
</script>
