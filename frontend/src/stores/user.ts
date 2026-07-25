import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type UserInfo } from '@/api/modules/auth'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const userInfo = ref<UserInfo | null>(null)

  const isLoggedIn = computed(() => !!accessToken.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')

  const setToken = (access: string, refresh: string) => {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  const clearToken = () => {
    accessToken.value = null
    refreshToken.value = null
    userInfo.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  const fetchUserInfo = async () => {
    if (!accessToken.value) return
    try {
      userInfo.value = await authApi.getMe()
    } catch {
      clearToken()
    }
  }

  const login = async (username: string, password: string) => {
    const res = await authApi.login({ username, password })
    setToken(res.access_token, res.refresh_token)
    await fetchUserInfo()
    return res
  }

  const logout = async () => {
    try {
      await authApi.logout()
    } catch {
      // ignore
    }
    clearToken()
    router.push('/login')
  }

  return {
    accessToken,
    refreshToken,
    userInfo,
    isLoggedIn,
    isAdmin,
    setToken,
    clearToken,
    fetchUserInfo,
    login,
    logout,
  }
})
