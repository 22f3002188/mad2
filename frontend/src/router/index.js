import { createRouter, createWebHistory } from 'vue-router'

const routes = [
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
    path: '/admin/admindashboard',
    name: 'admindashboard',
    component: () => import('../views/admin/admindashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/users/userdashboard',
    name: 'userdashboard',
    component: () => import('../views/users/userdashboard.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/admin/navbar',
    name: 'navbar',
    component: () => import('../views/admin/navbar.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/users/navbar',
    name: 'navbar',
    component: () => import('../views/users/navbar.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
  path: '/admin/addsubject',
  name: 'addsubject',
  component: () => import('@/views/admin/addsubject.vue'),
  meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/editsubject/:id',
    name: 'editsubject',
    component: () => import('@/views/admin/editsubject.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
  path: '/admin/viewchapter/:subjectId',
  name: 'viewchapter',
  component: () => import('@/views/admin/viewchapter.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/userlist',
  name: 'userlist',
  component: () => import('@/views/admin/userlist.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/subjects/:subjectId/addchapter',
  name: 'addchapter',
  component: () => import('@/views/admin/addchapter.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/subjects/:subjectId/editchapter/:chapterId',
  name: 'editchapter',
  component: () => import('@/views/admin/editchapter.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/chapters/:chapterId/viewquiz',
  name: 'viewquiz',
  component: () => import('@/views/admin/viewquiz.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/chapters/:chapterId/addquiz',
  name: 'addquiz',
  component: () => import('@/views/admin/addquiz.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/chapters/:chapterId/quizzes/:quizId/edit',
  name: 'editquiz',
  component: () => import('@/views/admin/editquiz.vue'),
  meta: { requiresAuth: true, role: 'admin' }
  
},
{
  path: '/admin/quizzes/:quizId/questions',
  name: 'viewquestion',
  component: () => import('@/views/admin/viewquestion.vue'),
  meta: { requiresAuth: true, role: 'admin' }
}




]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user'))

  if (to.meta.requiresAuth) {
    if (!token) return next('/login')

    if (to.meta.role && user?.role !== to.meta.role) {
      return next('/unauthorized')
    }
  }

  next()
})

export default router
