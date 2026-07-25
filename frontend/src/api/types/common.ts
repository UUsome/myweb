// === 通用 API 响应类型 ===
export interface APIResponse<T = any> {
  code: number
  message: string
  data: T
  timestamp: number
}

// === 偏移分页（管理后台） ===
export interface PageResponse<T = any> {
  list: T[]
  total: number
  page: number
  page_size: number
  has_next: boolean
}

// === 游标分页（列表页） ===
export interface CursorPageResponse<T = any> {
  list: T[]
  cursor: string | null
  has_next: boolean
}
