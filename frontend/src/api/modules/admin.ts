import apiClient, { type PageResponse } from '../client'
import type { UserInfo } from '../types/models'

// ── 用户管理 ──

export const adminApi = {
  getUsers: (params: { page?: number; page_size?: number; keyword?: string }) =>
    apiClient.get<PageResponse<UserInfo>>('/admin/users', { params }),

  createUser: (data: { username: string; email: string; password: string; role?: string }) =>
    apiClient.post<UserInfo>('/admin/users', data),

  updateUser: (id: number, data: Record<string, any>) =>
    apiClient.put<UserInfo>(`/admin/users/${id}`, data),

  deleteUser: (id: number) => apiClient.delete(`/admin/users/${id}`),

  freezeUser: (id: number) => apiClient.post(`/admin/users/${id}/freeze`),

  unfreezeUser: (id: number) => apiClient.post(`/admin/users/${id}/unfreeze`),

  // ── 帖子管理 ──

  getPosts: (params: { page?: number; page_size?: number; status?: string }) =>
    apiClient.get<PageResponse<any>>('/admin/forum_posts', { params }),

  updatePost: (id: number, data: Record<string, any>) =>
    apiClient.put<any>(`/admin/forum_posts/${id}`, data),

  deletePost: (id: number) => apiClient.delete(`/admin/forum_posts/${id}`),

  // ── 板块管理 ──

  getCategories: () => apiClient.get<any[]>('/admin/forum_categories'),

  createCategory: (data: Record<string, any>) =>
    apiClient.post<any>('/admin/forum_categories', data),

  updateCategory: (id: number, data: Record<string, any>) =>
    apiClient.put<any>(`/admin/forum_categories/${id}`, data),

  deleteCategory: (id: number) => apiClient.delete(`/admin/forum_categories/${id}`),

  // ── 专家管理 ──

  getExperts: (params: { page?: number; page_size?: number; keyword?: string }) =>
    apiClient.get<PageResponse<any>>('/admin/experts', { params }),

  createExpert: (data: Record<string, any>) =>
    apiClient.post<any>('/admin/experts', data),

  updateExpert: (id: number, data: Record<string, any>) =>
    apiClient.put<any>(`/admin/experts/${id}`, data),

  deleteExpert: (id: number) => apiClient.delete(`/admin/experts/${id}`),

  // ── 职位管理 ──

  getJobs: (params: { page?: number; page_size?: number }) =>
    apiClient.get<PageResponse<any>>('/admin/jobs', { params }),

  createJob: (data: Record<string, any>) =>
    apiClient.post<any>('/admin/jobs', data),

  updateJob: (id: number, data: Record<string, any>) =>
    apiClient.put<any>(`/admin/jobs/${id}`, data),

  deleteJob: (id: number) => apiClient.delete(`/admin/jobs/${id}`),

  toggleFeatured: (id: number) => apiClient.post(`/admin/jobs/${id}/toggle-featured`),

  // ── 专家平台管理 ──

  getExpertPlatforms: (expertId: number) =>
    apiClient.get<any[]>(`/admin/expert_platforms?expert_id=${expertId}`),

  createPlatform: (data: Record<string, any>) =>
    apiClient.post<any>('/admin/expert_platforms', data),

  updatePlatform: (id: number, data: Record<string, any>) =>
    apiClient.put<any>(`/admin/expert_platforms/${id}`, data),

  deletePlatform: (id: number) => apiClient.delete(`/admin/expert_platforms/${id}`),

  // ── 专家案例管理 ──

  getExpertCases: (expertId: number) =>
    apiClient.get<any[]>(`/admin/expert_cases?expert_id=${expertId}`),

  createCase: (data: Record<string, any>) =>
    apiClient.post<any>('/admin/expert_cases', data),

  updateCase: (id: number, data: Record<string, any>) =>
    apiClient.put<any>(`/admin/expert_cases/${id}`, data),

  deleteCase: (id: number) => apiClient.delete(`/admin/expert_cases/${id}`),
}

export type * from '../types/models'