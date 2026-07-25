import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const globalLoading = ref(false)
  const sidebarCollapsed = ref(false)

  const setLoading = (val: boolean) => {
    globalLoading.value = val
  }

  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  return {
    globalLoading,
    sidebarCollapsed,
    setLoading,
    toggleSidebar,
  }
})
