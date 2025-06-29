<template>
  <div class="dashboard-page">
    <navbar />
    <div class="container mt-5">
      <div class="card shadow-lg border-0">
        <div class="card-header bg-primary text-white text-center">
          <h3 class="mb-0">Subject Modules</h3>
        </div>
        <div class="card-body bg-white">
          <table class="table table-hover table-striped text-center">
            <thead class="table-light">
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
                  <div class="d-flex justify-content-center flex-wrap gap-2">
                    <button @click="viewChapters(subject.id)" class="btn btn-outline-info btn-sm">
                      📂 View Chapters
                    </button>
                    <button @click="editSubject(subject.id)" class="btn btn-outline-warning btn-sm">
                      ✏️ Edit
                    </button>
                    <button @click="deleteSubject(subject.id)" class="btn btn-outline-danger btn-sm">
                      🗑️ Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <div class="text-center mt-4">
            <button @click="goToAdd" class="btn btn-success px-4 py-2">
              Add New Subject
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navbar from './navbar.vue';
import { getSubjects } from '@/services/authService';
import {deleteSubject} from '@/services/authService';
import { getChaptersBySubject } from '@/services/authService';

export default {
  components: { navbar },
  data() {
    return {
      subjects: [],
    };
  },
  methods: {
    async fetchSubjects() {
      try {
        const res = await getSubjects();
        this.subjects = res.subjects;
      } catch (err) {
        console.error('Failed to fetch subjects:', err.message);
      }
    },
    goToAdd() {
      this.$router.push('/admin/addsubject');
    },
    editSubject(id) {
      this.$router.push(`/admin/editsubject/${id}`);
    },
    async deleteSubject(id) {
      try {
        await deleteSubject(id);
        this.fetchSubjects();
      } catch (err) {
        console.error('Delete failed:', err.message || err);
      }
    },
    viewChapters(subjectId) {
      this.$router.push(`/admin/viewchapter/${subjectId}`);
    },
  },
  mounted() {
    this.fetchSubjects();
  },
};
</script>


<style scoped>
.dashboard-page {
  background-color: #ffe6f0; /* light pink page background */
  min-height: 100vh;
  padding-top: 30px;
}

.card {
  background-color: #fff0f5; /* light pink card */
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-radius: 16px 16px 0 0;
  background-color: #147efb !important;
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
}

/* Button styles with light backgrounds */
.btn-outline-info {
  background-color: #e0f7fa;
  border-color: #0dcaf0;
  color: #0dcaf0;
}
.btn-outline-info:hover {
  background-color: #0dcaf0;
  color: #fff;
}

.btn-outline-warning {
  background-color: #fff3cd;
  border-color: #ffc107;
  color: #ffc107;
}
.btn-outline-warning:hover {
  background-color: #ffc107;
  color: #fff;
}

.btn-outline-danger {
  background-color: #f8d7da;
  border-color: #dc3545;
  color: #dc3545;
}
.btn-outline-danger:hover {
  background-color: #dc3545;
  color: #fff;
}
</style>


