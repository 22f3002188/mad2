<template>
  <nav class="navbar navbar-expand-lg navbar-dark quiz-navbar shadow-sm py-3">
    <div class="container">
      <!-- Brand -->
      <router-link class="navbar-brand fw-bold fs-3 gradient-brand" to="/">
        Quiz Nation
      </router-link>

      <!-- Toggle -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Nav links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0 d-flex gap-2">
          <li class="nav-item">
            <router-link class="nav-link nav-tab" to="/admin/admindashboard">
              <i class="bi bi-house-door-fill me-1"></i> Home
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link nav-tab" to="/admin/userlist">
              <i class="bi bi-people-fill me-1"></i> Users
            </router-link>

          </li>
          <li class="nav-item">
            <router-link class="nav-link nav-tab" to="/admin/adminsummary">
              <i class="bi bi-clipboard-data-fill me-1"></i> Summary
            </router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link nav-tab" href="#" @click="logout">
              <i class="bi bi-box-arrow-right me-1"></i> Logout
            </a>
          </li>
        </ul>

        <!-- Search bar -->
        <form class="d-flex" @submit.prevent="search">
          <div class="input-group search-box">
            <input
              v-model="query"
              class="form-control border-0"
              placeholder="🔍 Search users, subjects..."
            />
            <button class="btn btn-outline-light px-3" type="submit">Go</button>
          </div>
        </form>

        <!-- Admin Text -->
        <span class="navbar-text text-white fw-semibold ms-3 d-none d-lg-block">
          Welcome Admin
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
    search() {
      this.$router.push({ path: '/adminsearch', query: { q: this.query } });
    }
  }
};
</script>

<style scoped>
/* Navbar background */
.quiz-navbar {
  background: linear-gradient(to right, #7f1d9c, #d946ef); /* dark pink gradient */
  border-bottom: 2px solid #f3c1e8;
}

/* Brand gradient text */
.gradient-brand {
  background: linear-gradient(45deg, #f472b6, #e879f9);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Nav tab consistent styling */
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

/* Search box styling */
.search-box {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2rem;
  overflow: hidden;
}
.search-box input {
  background: transparent;
  color: white;
  padding-left: 1rem;
}
.search-box input::placeholder {
  color: #e0d7ec;
}
.search-box input:focus {
  box-shadow: none;
}
</style>
