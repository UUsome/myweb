import type { Router } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

// 免登录公开路由
const PUBLIC_ROUTES = new Set([
  'Login', 'Logout',
  'Home', 'Forum', 'Category', 'PostDetail',
  'Experts', 'ExpertDetail', 'CaseDetail',
  'Jobs', 'JobDetail',
])

export function setupRouterGuards(router: Router) {
  router.beforeEach(async (to, _from, next) => {
    const userStore = useUserStore()

    // 公开路由 → 直接放行，不检查登录
    if (to.meta.requiresAuth === false || PUBLIC_ROUTES.has(to.name as string)) {
      return next()
    }

    // 需登录路由 → 检查登录状态
    if (!userStore.isLoggedIn) {
      ElMessage.warning('请先登录')
      return next('/login')
    }

    // 自动获取用户信息（登录后首次进入）
    if (!userStore.userInfo) {
      await userStore.fetchUserInfo()
    }

    // 管理员权限检查
    if (to.meta.requiresAdmin && !userStore.isAdmin) {
      ElMessage.error('您没有权限访问此页面')
      return next('/')
    }

    next()
  })
}
