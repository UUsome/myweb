import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'

// === 统一响应类型 ===
export interface APIResponse<T = any> {
  code: number
  message: string
  data: T
  timestamp: number
}

// === 分页响应类型（偏移分页 - 管理后台） ===
export interface PageResponse<T = any> {
  list: T[]
  total: number
  page: number
  page_size: number
  has_next: boolean
}

// === 游标分页响应类型 ===
export interface CursorPageResponse<T = any> {
  list: T[]
  cursor: string | null
  has_next: boolean
}

// === 错误码映射 ===
const ERROR_MESSAGES: Record<number, string> = {
  10001: '请先登录',
  10002: '登录已过期，请重新登录',
  10003: '您没有权限执行此操作',
  20001: '请完善表单信息',
  20002: '数据格式错误',
  30001: '数据不存在',
  30002: '操作重复，请勿重复提交',
  50100: '功能开发中，敬请期待',
}

// === Axios 实例 ===
const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// === 请求拦截器 ===
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const userStore = useUserStore()
    if (userStore.accessToken) {
      config.headers.Authorization = `Bearer ${userStore.accessToken}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// === 响应拦截器 ===
apiClient.interceptors.response.use(
  (response: AxiosResponse<APIResponse>) => {
    const { code, message, data } = response.data

    // 业务成功（code === 0）
    if (code === 0) {
      return data as any
    }

    // 业务错误
    const errorMsg = ERROR_MESSAGES[code] || message || '系统繁忙，请稍后重试'

    // 认证错误 → 跳转登录
    if (code === 10001 || code === 10002) {
      const userStore = useUserStore()
      userStore.clearToken()
      router.push('/login')
      ElMessage.error(errorMsg)
      return Promise.reject(new Error(errorMsg))
    }

    ElMessage.error(errorMsg)
    return Promise.reject(new Error(errorMsg))
  },
  (error) => {
    if (error.response) {
      const { status } = error.response
      if (status === 401) {
        const userStore = useUserStore()
        userStore.clearToken()
        router.push('/login')
        ElMessage.error('登录已过期，请重新登录')
      } else if (status === 403) {
        ElMessage.error('您没有权限执行此操作')
      } else if (status === 404) {
        ElMessage.error('请求的资源不存在')
      } else if (status >= 500) {
        ElMessage.error('服务器内部错误，请稍后重试')
      }
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请检查网络连接')
    } else {
      ElMessage.error('网络异常，请检查网络连接')
    }
    return Promise.reject(error)
  }
)

export default apiClient
