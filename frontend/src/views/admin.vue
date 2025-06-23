<template>
  <div class="container mt-4">
    <!-- Title Section -->
    <div class="card-header bg-primary text-white text-center fs-4 fw-bold">
      Subjects
    </div>
    
    <!-- Table Section -->
    <div class="card shadow-sm">
      <div class="card-body">
        <table class="table table-striped text-center align-middle">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Subject Name</th>
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
                <div class="d-flex justify-content-center gap-2">
                  <router-link :to="'/view-chapters/' + subject.id" class="btn btn-info btn-sm text-white">
                    View Chapter
                  </router-link>
                  <router-link :to="'/edit-subject/' + subject.id" class="btn btn-warning btn-sm">
                    Edit
                  </router-link>
                  <button @click="deleteSubject(subject.id)" class="btn btn-danger btn-sm">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Add New Subject Button -->
      <div class="text-center mt-4">
        <router-link to="/manage-subjects" class="btn btn-success">Add New Subject</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      subjects: [] // Array to store subject data
    };
  },
  created() {
    // Fetch subjects from the server when the component is created
    this.fetchSubjects();
  },
  methods: {
    fetchSubjects() {
      // Replace this with actual API call to fetch subjects from the server
      fetch('/api/subjects')
        .then(response => response.json())
        .then(data => {
          this.subjects = data; // Populate subjects data
        })
        .catch(error => console.error('Error fetching subjects:', error));
    },
    deleteSubject(subjectId) {
      // Ask for confirmation before deleting the subject
      if (confirm('Are you sure you want to delete this subject?')) {
        // Call API to delete the subject
        fetch(`/api/subjects/${subjectId}`, {
          method: 'DELETE',
        })
          .then(() => {
            this.subjects = this.subjects.filter(subject => subject.id !== subjectId); // Remove from UI
          })
          .catch(error => console.error('Error deleting subject:', error));
      }
    }
  }
};
</script>

<style scoped>
/* You can add your custom styles here */
</style>
