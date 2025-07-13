<template>
  <div class="edit-subject-page d-flex justify-content-center align-items-center min-vh-100">
    <div class="container">
      <div class="card shadow-lg border-0 p-4 mx-auto" style="max-width: 600px;">
        <div class="card-header bg-warning text-white text-center rounded-top">
          <h3 class="mb-0">Edit Subject</h3>
        </div>
        <form @submit.prevent="handleSubmit" class="card-body">
          <div class="mb-3">
            <label class="form-label fw-bold">Subject Name</label>
            <input v-model="name" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label fw-bold">Subject Description</label>
            <textarea v-model="description" rows="4" class="form-control" required></textarea>
          </div>
          <div class="d-flex justify-content-center gap-3">
            <button type="submit" class="btn btn-warning px-4">Save</button>
            <button class="btn btn-secondary px-4" @click="$router.push('/admin/admindashboard')">Cancel</button>
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
      id: this.$route.params.id,
      name: '',
      description: '',
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
        await updateSubject(this.id, {
          name: this.name.trim(),
          description: this.description.trim(),
        });
        this.$router.push('/admin/admindashboard');
      } catch (err) {
        console.error('Update failed:', err.message);
      }
    },
  },
};
</script>

<style scoped>
.edit-subject-page {
  background-color: #ffe6f0; /* light pink page background */
  min-height: 100vh;
  padding: 40px 0;
}

/* Ensure the card remains white */
.edit-subject-page .card,
.edit-subject-page .card-body {
  background-color: #fff !important;
  border-radius: 16px;
}
</style>
