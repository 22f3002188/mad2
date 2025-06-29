<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">
    <div class="container">
      <a class="navbar-brand fw-bold text-white" href="#">Quiz Portal</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item"><router-link class="nav-link fw-bold text-white" to="/userdashboard">Home</router-link></li>
          <li class="nav-item"><router-link class="nav-link fw-bold text-white" to="/userscores">Scores</router-link></li>
          <li class="nav-item"><router-link class="nav-link fw-bold text-white" to="/summary">Summary</router-link></li>
          <li class="nav-item"><a class="nav-link fw-bold text-danger" href="#" @click="logout">Logout</a></li>
        </ul>
        <form class="mb-3" @submit.prevent="search">
          <div class="input-group">
            <input v-model="query" class="form-control" placeholder="Search by quiz or subject name..." />
            <button class="btn btn-primary" type="submit">Search</button>
          </div>
        </form>
        <span class="navbar-text text-white ms-3">Welcome, {{ fullName }}</span>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      fullName: ''
    };
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem('user'));
    this.fullName = user?.full_name || '';
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/login');
    },
    search() {
      this.$router.push({ path: '/usersearch', query: { q: this.query } });
    }
  }
};
</script>
