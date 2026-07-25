import { ref, reactive } from 'vue'

export interface UsePaginationOptions<T> {
  fetchFn: (params: any) => Promise<{ list: T[]; cursor: string | null; has_next: boolean }>
  initialParams?: Record<string, any>
  limit?: number
}

export function usePagination<T>(options: UsePaginationOptions<T>) {
  const { fetchFn, initialParams = {}, limit = 20 } = options

  const items = ref<T[]>([])
  const cursor = ref<string | null>(null)
  const hasMore = ref(true)
  const loading = ref(false)
  const initialized = ref(false)

  const params = reactive({ ...initialParams, limit })

  const reset = () => {
    items.value = []
    cursor.value = null
    hasMore.value = true
    initialized.value = false
    Object.assign(params, initialParams, { limit })
  }

  const fetch = async (append = true) => {
    if (loading.value) return
    if (!append) {
      items.value = []
      cursor.value = null
      hasMore.value = true
    }
    if (!hasMore.value) return

    loading.value = true
    try {
      const result = await fetchFn({
        ...params,
        cursor: append ? cursor.value : undefined,
      })

      if (append) {
        items.value.push(...result.list)
      } else {
        items.value = result.list
      }

      cursor.value = result.cursor
      hasMore.value = result.has_next
      initialized.value = true
    } finally {
      loading.value = false
    }
  }

  const loadMore = () => fetch(true)
  const refresh = () => fetch(false)

  return {
    items,
    loading,
    hasMore,
    initialized,
    params,
    fetch,
    loadMore,
    refresh,
    reset,
  }
}
