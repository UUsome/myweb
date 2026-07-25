import apiClient, { type CursorPageResponse } from '../client'
import type { Category, Post, PostDetail, Reply } from '../types/models'

export interface CreatePostParams {
  title: string
  content: string
  category_id: number
  status?: 'draft' | 'published'
}

export interface PostListParams {
  category_id?: number
  status?: string
  cursor?: string
  limit?: number
}

export const forumApi = {
  getCategories: () => apiClient.get<Category[]>('/categories'),

  getPosts: (params: PostListParams) =>
    apiClient.get<CursorPageResponse<Post>>('/posts', { params }),

  getPost: (id: number) => apiClient.get<PostDetail>(`/posts/${id}`),

  createPost: (data: CreatePostParams) =>
    apiClient.post<PostDetail>('/posts', data),

  updatePost: (id: number, data: Partial<CreatePostParams>) =>
    apiClient.put<PostDetail>(`/posts/${id}`, data),

  deletePost: (id: number) => apiClient.delete(`/posts/${id}`),

  getReplies: (postId: number, params: { cursor?: string; limit?: number }) =>
    apiClient.get<CursorPageResponse<Reply>>(`/posts/${postId}/replies`, { params }),

  createReply: (postId: number, content: string) =>
    apiClient.post<Reply>(`/posts/${postId}/replies`, { content }),
}

export type * from '../types/models'
