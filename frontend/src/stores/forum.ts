import { defineStore } from 'pinia'
import { ref } from 'vue'
import { forumApi, type Category } from '@/api/modules/forum'

export const useForumStore = defineStore('forum', () => {
  const categories = ref<Category[]>([])
  const categoriesLoaded = ref(false)

  const fetchCategories = async (force = false) => {
    if (!force && categoriesLoaded.value) return categories.value
    categories.value = await forumApi.getCategories()
    categoriesLoaded.value = true
    return categories.value
  }

  const clearCache = () => {
    categoriesLoaded.value = false
    categories.value = []
  }

  return {
    categories,
    categoriesLoaded,
    fetchCategories,
    clearCache,
  }
})
