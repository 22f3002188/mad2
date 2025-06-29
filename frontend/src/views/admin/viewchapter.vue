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
                      <button class="btn btn-info btn-sm text-white">View Quiz</button>
                      <button class="btn btn-warning btn-sm">Edit</button>
                      <button class="btn btn-danger btn-sm" @click="deleteChapter(chapter.id)">Delete</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="text-center mt-4">
            <button class="btn btn-success btn-lg px-4 shadow" @click="addChapter">
              ➕ Add Chapter
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
    deleteChapter(chapterId) {
      console.log(`Delete chapter ${chapterId}`);
    },
  },
  mounted() {
    this.fetchChapters();
  },
};
</script>

<style scoped>
.chapters-page {
  background-color: #f0f2f5;
  min-height: 100vh;
  padding-top: 30px;
}
.table th,
.table td {
  vertical-align: middle;
}
</style>
