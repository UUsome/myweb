import { defineStore } from 'pinia'
import { ref } from 'vue'
import { experthubApi, type Tag, type Service } from '@/api/modules/experthub'

export const useExpertHubStore = defineStore('experthub', () => {
  const tags = ref<Tag[]>([])
  const services = ref<Service[]>([])
  const tagsLoaded = ref(false)
  const servicesLoaded = ref(false)
  const lastFetchTime = ref<number>(0)
  const CACHE_TTL = 60 * 60 * 1000 // 1 hour

  const fetchTags = async (force = false) => {
    const now = Date.now()
    if (!force && tagsLoaded.value && (now - lastFetchTime.value) < CACHE_TTL) {
      return tags.value
    }
    tags.value = await experthubApi.getTags()
    tagsLoaded.value = true
    lastFetchTime.value = now
    return tags.value
  }

  const fetchServices = async (force = false) => {
    const now = Date.now()
    if (!force && servicesLoaded.value && (now - lastFetchTime.value) < CACHE_TTL) {
      return services.value
    }
    services.value = await experthubApi.getServices()
    servicesLoaded.value = true
    lastFetchTime.value = now
    return services.value
  }

  const clearCache = () => {
    tagsLoaded.value = false
    servicesLoaded.value = false
    tags.value = []
    services.value = []
  }

  return {
    tags,
    services,
    tagsLoaded,
    servicesLoaded,
    fetchTags,
    fetchServices,
    clearCache,
  }
})
