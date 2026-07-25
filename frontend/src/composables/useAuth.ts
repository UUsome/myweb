import { useUserStore } from '@/stores/user'
import router from '@/router'

export function useAuth() {
  const userStore = useUserStore()

  const requireAuth = () => {
    if (!userStore.isLoggedIn) {
      router.push('/login')
      return false
    }
    return true
  }

  const requireAdmin = () => {
    if (!requireAuth()) return false
    if (!userStore.isAdmin) {
      router.push('/')
      return false
    }
    return true
  }

  return {
    ...userStore,
    requireAuth,
    requireAdmin,
  }
}
