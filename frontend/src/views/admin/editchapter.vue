<template>
  <div class="edit-chapter-page">
    <div class="container my-5">
      <div class="card shadow border-0 mx-auto" style="max-width: 600px">
        <div class="card-header bg-warning text-white text-center fs-4 fw-bold">
           Edit Chapter
        </div>
        <div class="card-body">
          <form @submit.prevent="updateChapter">
            <div class="mb-3">
              <label class="form-label fw-bold">Chapter Name</label>
              <input v-model="name" class="form-control" required />
            </div>

            <div class="mb-3">
              <label class="form-label fw-bold">Chapter Description</label>
              <textarea v-model="description" rows="4" class="form-control" required></textarea>
            </div>

            <div class="d-flex justify-content-center gap-3">
              <button class="btn btn-success px-4" type="submit">Save</button>
              <button class="btn btn-secondary px-4" @click="cancel">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { updateChapter, getChaptersBySubject } from '@/services/authService';

export default {
  data() {
    return {
      name: '',
      description: '',
    };
  },
  async mounted() {
    const chapterId = this.$route.params.chapterId;
    const subjectId = this.$route.params.subjectId;
    const res = await getChaptersBySubject(subjectId);
    const chapter = res.chapters.find(c => c.id == chapterId);
    if (chapter) {
      this.name = chapter.name;
      this.description = chapter.description;
    }
  },
  methods: {
    async updateChapter() {
      const chapterId = this.$route.params.chapterId;
      const subjectId = this.$route.params.subjectId;
      await updateChapter(chapterId, {
        name: this.name.trim(),
        description: this.description.trim(),
      });
      this.$router.push(`/admin/viewchapter/${subjectId}`);
    },
    cancel() {
      const subjectId = this.$route.params.subjectId;
      this.$router.push(`/admin/viewchapter/${subjectId}`);
    },
  },
};
</script>

<style scoped>
.edit-chapter-page {
  background-color: #fff0f5;
  min-height: 100vh;
  padding-top: 30px;
}
</style>
