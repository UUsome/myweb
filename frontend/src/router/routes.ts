import type { RouteRecordRaw } from 'vue-router'

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/forum',
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginPage.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import('@/views/auth/LogoutPage.vue'),
  },
  {
    path: '/',
    component: () => import('@/components/layout/DefaultLayout.vue'),
    children: [
      // Home
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/home/HomePage.vue'),
        meta: { requiresAuth: false },
      },
      // Forum
      {
        path: 'forum',
        name: 'Forum',
        component: () => import('@/views/forum/ForumPage.vue'),
        meta: { requiresAuth: false },
      },
      {
        path: 'forum/category/:id',
        name: 'Category',
        component: () => import('@/views/forum/CategoryPage.vue'),
        meta: { requiresAuth: false },
      },
      {
        path: 'forum/post/:id',
        name: 'PostDetail',
        component: () => import('@/views/forum/PostDetailPage.vue'),
        meta: { requiresAuth: false },
      },
      // ExpertHub
      {
        path: 'experts',
        name: 'Experts',
        component: () => import('@/views/experthub/ExpertListPage.vue'),
        meta: { requiresAuth: false },
      },
      {
        path: 'expert-hub/:id',
        name: 'ExpertDetail',
        component: () => import('@/views/experthub/ExpertDetailPage.vue'),
        meta: { requiresAuth: false },
      },
      {
        path: 'expert-hub/case/:id',
        name: 'CaseDetail',
        component: () => import('@/views/experthub/CaseDetailPage.vue'),
        meta: { requiresAuth: false },
      },
      // JobHub
      {
        path: 'jobs',
        name: 'Jobs',
        component: () => import('@/views/jobhub/JobListPage.vue'),
        meta: { requiresAuth: false },
      },
      {
        path: 'jobs/:id',
        name: 'JobDetail',
        component: () => import('@/views/jobhub/JobDetailPage.vue'),
        meta: { requiresAuth: false },
      },
      // Contact
      {
        path: 'contact',
        name: 'Contact',
        component: () => import('@/views/experthub/ContactPage.vue'),
        meta: { title: '联系我们', requiresAuth: false },
      },
    ],
  },
  // Admin
  {
    path: '/admin',
    component: () => import('@/components/layout/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/AdminDashboard.vue'),
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/users/UserList.vue'),
      },
      {
        path: 'users/create',
        name: 'AdminUserCreate',
        component: () => import('@/views/admin/users/UserForm.vue'),
      },
      {
        path: 'users/:id/edit',
        name: 'AdminUserEdit',
        component: () => import('@/views/admin/users/UserForm.vue'),
      },
      {
        path: 'experts',
        name: 'AdminExperts',
        component: () => import('@/views/admin/experts/ExpertList.vue'),
      },
      {
        path: 'experts/create',
        name: 'AdminExpertCreate',
        component: () => import('@/views/admin/experts/ExpertForm.vue'),
      },
      {
        path: 'experts/:id/edit',
        name: 'AdminExpertEdit',
        component: () => import('@/views/admin/experts/ExpertForm.vue'),
      },
      {
        path: 'jobs',
        name: 'AdminJobs',
        component: () => import('@/views/admin/jobs/JobList.vue'),
      },
      {
        path: 'jobs/create',
        name: 'AdminJobCreate',
        component: () => import('@/views/admin/jobs/JobForm.vue'),
      },
      {
        path: 'jobs/:id/edit',
        name: 'AdminJobEdit',
        component: () => import('@/views/admin/jobs/JobForm.vue'),
      },
      {
        path: 'posts',
        name: 'AdminPosts',
        component: () => import('@/views/admin/forum/PostList.vue'),
      },
      {
        path: 'categories',
        name: 'AdminCategories',
        component: () => import('@/views/admin/forum/CategoryList.vue'),
      },
      {
        path: 'contact',
        name: 'ContactEdit',
        component: () => import('@/views/admin/ContactEditPage.vue'),
        meta: { title: '编辑联系我们', requiresAdmin: true },
      },
    ],
  },
]
