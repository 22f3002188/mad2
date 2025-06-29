<template>
  <div class="add-subject-page bg-light d-flex justify-content-center align-items-center min-vh-100">
    <div class="container">
      <div class="card shadow-lg border-0 p-4">
        <div class="card-header bg-primary text-white text-center rounded-top">
          <h3 class="mb-0">Add New Subject</h3>
        </div>

        <form @submit.prevent="handleSubmit" class="card-body bg-white">
          <div class="mb-3">
            <label class="form-label fw-bold">Subject Name</label>
            <input
              v-model="name"
              type="text"
              class="form-control"
              placeholder="Enter subject name"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label fw-bold">Subject Description</label>
            <textarea
              v-model="description"
              class="form-control"
              rows="4"
              placeholder="Enter subject description"
              required
            ></textarea>
          </div>

          <div class="d-flex justify-content-center gap-3">
            <button type="submit" class="btn btn-success px-4">Save</button>
            <button type="button" class="btn btn-secondary px-4" @click="cancel">Cancel</button>
          </div>

          <div v-if="message" class="alert alert-success mt-4 text-center">{{ message }}</div>
          <div v-if="error" class="alert alert-danger mt-4 text-center">{{ error }}</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { addSubject } from '@/services/authService';

export default {
  data() {
    return {
      name: '',
      description: '',
      message: '',
      error: '',
    };
  },
  methods: {
    async handleSubmit() {
      this.message = '';
      this.error = '';
      try {
        const payload = {
          name: this.name,
          description: this.description,
        };
        const res = await addSubject(payload);
        this.message = res.message;
        this.name = '';
        this.description = '';
        this.$router.push('/admin/admindashboard');
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to add subject.';
      }
    },
    cancel() {
      this.$router.push('/admin/admindashboard');
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

