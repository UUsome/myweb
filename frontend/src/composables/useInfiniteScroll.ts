import { ref, onMounted, onUnmounted, type Ref } from 'vue'

export function useInfiniteScroll(
  loadMore: () => Promise<void>,
  hasMore: Ref<boolean>,
  loading: Ref<boolean>
) {
  const sentinel = ref<HTMLElement | null>(null)
  let observer: IntersectionObserver | null = null

  onMounted(() => {
    observer = new IntersectionObserver(
      async (entries) => {
        if (entries[0].isIntersecting && hasMore.value && !loading.value) {
          await loadMore()
        }
      },
      { rootMargin: '100px' }
    )

    if (sentinel.value) {
      observer.observe(sentinel.value)
    }
  })

  onUnmounted(() => {
    observer?.disconnect()
  })

  return { sentinel }
}
