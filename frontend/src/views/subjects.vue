<template>
  <div class="bg-light d-flex justify-content-center align-items-center vh-100">
    <div class="container">
      <div class="card shadow-lg p-4 border-0">
        <h2 class="text-center mb-4">New Subject</h2>

        <form @submit.prevent="submitForm" class="mb-4">
          <div class="mb-3">
            <input
              type="text"
              v-model="subject.name"
              class="form-control"
              placeholder="Subject Name"
              required
            />
          </div>
          <div class="mb-3">
            <textarea
              v-model="subject.description"
              class="form-control"
              rows="3"
              placeholder="Subject Description"
              required
            ></textarea>
          </div>
          <div class="d-flex justify-content-center gap-3">
            <button type="submit" class="btn btn-primary">Save</button>
            <router-link to="/admin" class="btn btn-secondary">Cancel</router-link>
          </div>
        </form>

        <div v-if="message" class="alert alert-success text-center" role="alert">
          {{ message }}
        </div>
        <div v-if="error" class="alert alert-danger text-center" role="alert">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      subject: {
        name: '',
        description: ''
      },
      message: '',
      error: ''
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('/api/subjects', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.subject)
        });

        if (!response.ok) throw new Error('Failed to save subject');

        const data = await response.json();
        this.message = 'Subject added successfully!';
        this.subject.name = '';
        this.subject.description = '';

        // Optional: redirect after a delay
        setTimeout(() => {
          this.$router.push('/admin');
        }, 1000);
      } catch (err) {
        this.error = err.message;
      }
    }
  }
};
</script>

<style scoped>
/* Add any custom scoped styles if needed */
</style>
