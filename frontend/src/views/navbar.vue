<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">
      <div class="container">
        <router-link to="/" class="navbar-brand fw-bold text-white">Quiz Portal</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link to="/admin-dashboard" class="nav-link fw-bold text-white">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/users" class="nav-link fw-bold text-white">Users</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/top-scorers" class="nav-link fw-bold text-white">Summary</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/logout" class="nav-link fw-bold text-danger">Logout</router-link>
            </li>
          </ul>

          <!-- Search Form -->
          <form @submit.prevent="handleSearch" class="mb-3">
            <div class="input-group">
              <input v-model="searchQuery" type="text" name="q" class="form-control" placeholder="Search users, subjects, chapters, quizzes">
              <button class="btn btn-primary" type="submit">Search</button>
            </div>
          </form>

          <span class="navbar-text text-white fw-bold ms-3">Welcome Admin</span>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <div class="container my-5">
      <slot></slot> <!-- Content will be injected here by child components -->
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: ''
    };
  },
  methods: {
    handleSearch() {
      // Handle the search logic here, e.g., redirect to the search results page
     this.$router.push({ name: 'searchresult', query: { q: this.searchQuery } });
    }
  }
};
</script>

<style scoped>
/* Optional: You can add custom styles here */
</style>