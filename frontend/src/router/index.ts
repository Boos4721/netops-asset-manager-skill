import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: () => import('@/views/LoginView.vue'), meta: { public: true } },
    {
      path: '/',
      component: () => import('@/components/layout/AppLayout.vue'),
      children: [
        { path: '', redirect: '/dashboard' },
        { path: 'dashboard', component: () => import('@/views/DashboardView.vue') },
        { path: 'inventory', component: () => import('@/views/InventoryView.vue') },
        { path: 'topology', component: () => import('@/views/TopologyView.vue') },
        { path: 'jobs', component: () => import('@/views/JobsView.vue') },
        { path: 'deploy', component: () => import('@/views/DeployView.vue') },
        { path: 'models', component: () => import('@/views/ModelsView.vue') },
        { path: 'chat', component: () => import('@/views/ChatView.vue') },
        { path: 'settings', component: () => import('@/views/SettingsView.vue') },
      ],
    },
    { path: '/:pathMatch(.*)*', redirect: '/dashboard' },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (!to.meta.public && !auth.isLoggedIn()) {
    return '/login'
  }
  if (to.path === '/login' && auth.isLoggedIn()) {
    return '/dashboard'
  }
})

export default router
