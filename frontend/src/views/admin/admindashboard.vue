<!-- AdminDashboard.vue -->

<template>
  <div>
    <navbar /> 
    <div class="container mt-4">
      <h3 class="text-center bg-primary text-white p-2">Subjects</h3>
      <table class="table table-bordered text-center">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="subject in subjects" :key="subject.id">
            <td>{{ subject.id }}</td>
            <td>{{ subject.name }}</td>
            <td>{{ subject.description }}</td>
            <td>
              <button @click="editSubject(subject.id)" class="btn btn-warning btn-sm">Edit</button>
              <button @click="deleteSubject(subject.id)" class="btn btn-danger btn-sm">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="goToAdd" class="btn btn-success">Add Subject</button>
    </div>
  </div>
</template>

<script>
import navbar from './navbar.vue'; 

export default {
  components: {
    navbar 
  },
  data() {
    return {
      subjects: []
    };
  },
  methods: {
    fetchSubjects() {
      const token = localStorage.getItem("token");
      fetch('http://localhost:5000/api/admin/subjects', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(res => res.json())
        .then(data => this.subjects = data.subjects)
        .catch(err => console.error('Failed to load subjects:', err));
    },
    editSubject(id) {
      this.$router.push(`/admin/subjects/${id}/edit`);
    },
    deleteSubject(id) {
      if (!confirm('Are you sure?')) return;
      const token = localStorage.getItem("token");
      fetch(`http://localhost:5000/api/subjects/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(() => this.fetchSubjects())
        .catch(err => console.error('Delete failed:', err));
    },
    goToAdd() {
      this.$router.push('/admin/subjects/new');
    }
  },
  mounted() {
    this.fetchSubjects();
  }
};
</script>
