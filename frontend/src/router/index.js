import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/home.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/login.vue'),
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/signup.vue'),
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/admin.vue'),
    },
    {
      path: '/searchresult',
      name: 'searchresult',
      component: () => import('../views/searchresult.vue'),
    }
  ],
})

export default router
