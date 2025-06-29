<template>
  <div class="edit-subject-page bg-light d-flex justify-content-center align-items-center min-vh-100">
    <div class="container">
      <div class="card shadow-lg border-0 p-4">
        <div class="card-header bg-warning text-white text-center rounded-top">
          <h3>Edit Subject</h3>
        </div>
        <form @submit.prevent="handleSubmit" class="card-body bg-white">
          <div class="mb-3">
            <label class="form-label fw-bold">Subject Name</label>
            <input v-model="name" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label fw-bold">Subject Description</label>
            <textarea v-model="description" rows="4" class="form-control" required></textarea>
          </div>
          <div class="d-flex justify-content-center gap-3">
            <button type="submit" class="btn btn-warning">Save</button>
            <button class="btn btn-secondary" @click="$router.push('/admin/admindashboard')">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { updateSubject, getSubjects } from '@/services/authService';

export default {
  data() {
    return {
      name: '',
      description: '',
      id: this.$route.params.id,
    };
  },
  async mounted() {
    try {
      const res = await getSubjects();
      const subject = res.subjects.find(s => s.id == this.id);
      if (subject) {
        this.name = subject.name;
        this.description = subject.description;
      }
    } catch (err) {
      console.error('Failed to load subject:', err.message);
    }
  },
  methods: {
    async handleSubmit() {
      try {
        const payload = {
          name: this.name,
          description: this.description,
        };
        await updateSubject(this.id, payload);
        this.$router.push('/admin/admindashboard');
      } catch (err) {
        console.error('Update failed:', err.message);
      }
    },
  },
};
</script>

<style scoped>
.add-subject-page {
  background-color: #ffe6f0; /* Light pink background */
  padding: 40px 0;
  min-height: 100vh;
}

.card {
  background-color: #fff0f5; /* Light pink card */
  max-width: 600px;
  margin: auto;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-radius: 16px 16px 0 0;
  background-color: #147efb;
  color: white;
  text-align: center;
}

.card-body {
  background-color: #fff0f5;
}

.btn-success {
  background-color: #28a745;
  border-color: #28a745;
  color: white;
}
.btn-success:hover {
  background-color: #218838;
  border-color: #1e7e34;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
  color: white;
}
.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}
</style>

