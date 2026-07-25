import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export function useRequest<T, P extends any[] = any[]>(
  fn: (...args: P) => Promise<T>,
  options?: {
    onSuccess?: (data: T) => void
    onError?: (error: Error) => void
    showError?: boolean
  }
) {
  const loading = ref(false)
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)

  const execute = async (...args: P): Promise<T | undefined> => {
    loading.value = true
    error.value = null

    try {
      const result = await fn(...args)
      data.value = result
      options?.onSuccess?.(result)
      return result
    } catch (err) {
      error.value = err as Error
      if (options?.showError !== false) {
        ElMessage.error((err as Error).message || '请求失败')
      }
      options?.onError?.(error.value)
      return undefined
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    data.value = null
    error.value = null
  }

  return {
    loading,
    data,
    error,
    execute,
    reset,
  }
}
