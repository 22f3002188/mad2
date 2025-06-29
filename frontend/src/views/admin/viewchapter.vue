<template>
  <div class="chapters-page">
    <navbar />
    <div class="container my-5">
      <div class="card shadow border-0">
        <div class="card-header bg-primary text-white text-center fs-4 fw-bold">
          Chapters of {{ subjectName }}
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-striped table-bordered text-center">
              <thead class="table-dark">
                <tr>
                  <th>ID</th>
                  <th>Chapter Name</th>
                  <th>Description</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="chapter in chapters" :key="chapter.id">
                  <td class="fw-bold">{{ chapter.id }}</td>
                  <td>{{ chapter.name }}</td>
                  <td>{{ chapter.description }}</td>
                  <td>
                    <div class="d-flex justify-content-center gap-2 flex-wrap">
                      <button class="btn btn-outline-info btn-sm">📁 View Quiz </button>
                      <button class="btn btn-outline-warning btn-sm">✏️ Edit</button>
                      <button class="btn btn-outline-danger btn-sm" @click="deleteChapter(chapter.id)">🗑️ Delete</button>

                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="text-center mt-4">
            <button class="btn btn-success btn-lg px-4 shadow" @click="addChapter">
              Add Chapter
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navbar from './navbar.vue';
import { getChaptersBySubject } from '@/services/authService';
import {deleteChapter} from '@/services/authService';

export default {
  components: { navbar },
  data() {
    return {
      chapters: [],
      subjectName: '',
    };
  },
  methods: {
    async fetchChapters() {
    const subjectId = this.$route.params.subjectId;
    try {
        const res = await getChaptersBySubject(subjectId);
        this.chapters = res.chapters;
        this.subjectName = res.subject_name || 'Subject';  
    } catch (err) {
        console.error('Failed to load chapters:', err.message);
    }
    },
    addChapter() {
    const subjectId = this.$route.params.subjectId;
    this.$router.push(`/admin/subjects/${subjectId}/addchapter`);
    },


    async deleteChapter(chapterId) {
    if (confirm("Are you sure you want to delete this chapter?")) {
        try {
        await deleteChapter(chapterId);
        // Refresh list after deletion
        await this.fetchChapters();
        } catch (err) {
        console.error("Delete failed:", err.message);
        alert("Failed to delete chapter.");
        }
    }
    }
  },
  mounted() {
    this.fetchChapters();
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
