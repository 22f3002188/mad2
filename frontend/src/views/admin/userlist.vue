<template>
  <div class="userlist-page">
    <navbar />

    <div class="container my-5">
      <div class="card shadow border-0">
        <div class="card-header bg-primary text-white text-center fs-4 fw-bold">
          Registered Users
        </div>

        <div class="card-body p-0">
          <table class="table table-bordered text-center mb-0 align-middle">
            <thead class="table-light">
              <tr>
                <th>Email</th>
                <th>Full Name</th>
                <th>Qualification</th>
                <th>Date of Birth</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.email }}</td>
                <td>{{ user.full_name }}</td>
                <td>{{ user.qualification || '-' }}</td>
                <td>{{ user.dob || '-' }}</td>
                <td>
                  <span class="badge bg-success">Active</span>
                </td>
              </tr>

              <tr v-if="users.length === 0">
                <td colspan="5" class="text-muted py-4">No users found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navbar from './navbar.vue';
import { getAllUsers, logoutUser } from '@/services/authService';

export default {
  name: 'UserList',
  components: { navbar },
  data() {
    return {
      users: [],
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await getAllUsers();
        this.users = response.users;
      } catch (error) {
        console.error('Error loading users:', error);
        alert('Failed to fetch users.');
      }
    },
    async logout() {
      try {
        await logoutUser();
      } catch (error) {
        console.error('Logout failed:', error);
      }
      this.$router.push('/login');
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.userlist-page {
  background-color: #ffe6f0; /* soft pink full screen */
  min-height: 100vh;
  padding-top: 30px;
}

.card {
  background-color: #fff0f5; /* lighter pink card */
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-radius: 16px 16px 0 0;
  background-color: #147efb !important; /* same bold blue as dashboard */
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.card-body {
  background-color: #fff0f5;
}

.table th,
.table td {
  vertical-align: middle;
  font-size: 0.95rem;
}

.table thead {
  background-color: #ffeaf4; /* soft pink table head */
}

.table-striped > tbody > tr:nth-of-type(odd) {
  background-color: #fff8fc;
}

.btn-danger {
  font-size: 0.85rem;
  padding: 6px 12px;
  border-radius: 8px;
  background-color: #dc3545;
  border: none;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.badge {
  font-size: 0.9rem;
  border-radius: 8px;
  padding: 4px 10px;
}
</style>
