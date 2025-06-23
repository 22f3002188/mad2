<template>
  <div class="container mt-4">
    <h2>Search Results for "{{ query }}"</h2>

    <template v-if="hasResults">
      <!-- Users Section -->
      <div v-if="users.length">
        <h4>Users</h4>
        <ul class="list-group">
          <li class="list-group-item" v-for="user in users" :key="user.id">
            <router-link :to="`/users/${user.id}`" class="text-decoration-none">
              {{ user.email }}
            </router-link>
          </li>
        </ul>
      </div>

      <!-- Subjects Section -->
      <div v-if="subjects.length">
        <h4>Subjects</h4>
        <ul class="list-group">
          <li class="list-group-item" v-for="subject in subjects" :key="subject.id">
            <router-link to="/admin" class="text-decoration-none">
              {{ subject.name }}
            </router-link>
          </li>
        </ul>
      </div>

      <!-- Chapters Section -->
      <div v-if="chapters.length">
        <h4>Chapters</h4>
        <ul class="list-group">
          <li class="list-group-item" v-for="chapter in chapters" :key="chapter.id">
            <router-link :to="`/subject/${chapter.subject_id}/chapters`" class="text-decoration-none">
              {{ chapter.name }}
            </router-link>
          </li>
        </ul>
      </div>

      <!-- Quizzes Section -->
      <div v-if="quizzes.length">
        <h4>Quizzes</h4>
        <ul class="list-group">
          <li class="list-group-item" v-for="quiz in quizzes" :key="quiz.id">
            <router-link :to="`/chapter/${quiz.chapter_id}/quizzes`" class="text-decoration-none">
              {{ quiz.quiz_name }}
            </router-link>
          </li>
        </ul>
      </div>
    </template>

    <p v-else class="text-danger">No results found.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

// Props or data from API
const route = useRoute();
const query = route.query.q || '';

// Sample props or data; replace with real API data or props
const users = []; // from API or parent
const subjects = [];
const chapters = [];
const quizzes = [];

// Computed property to check for any results
const hasResults = computed(() =>
  users.length || subjects.length || chapters.length || quizzes.length
);
</script>

<style scoped>
.text-danger {
  color: red;
}
</style>
