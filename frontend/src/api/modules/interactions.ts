import apiClient from '../client'
import type { LikeStatus, CommentItem } from '../types/models'

export const interactionsApi = {
  toggleLike: (targetType: string, targetId: number) =>
    apiClient.post<LikeStatus>(`/like/${targetType}/${targetId}`),

  getLikeStatus: (targetType: string, targetId: number) =>
    apiClient.get<LikeStatus>(`/like/${targetType}/${targetId}/status`),

  getLikeCount: (targetType: string, targetId: number) =>
    apiClient.get<{ target_type: string; target_id: number; like_count: number }>(
      `/like/${targetType}/${targetId}/count`
    ),

  getComments: (targetType: string, targetId: number) =>
    apiClient.get<CommentItem[]>(`/comments/${targetType}/${targetId}`),

  createComment: (targetType: string, targetId: number, content: string, parentId?: number) =>
    apiClient.post<CommentItem>(`/comments/${targetType}/${targetId}`, {
      content,
      parent_id: parentId,
    }),

  deleteComment: (commentId: number) =>
    apiClient.delete(`/comments/${commentId}`),
}

export type * from '../types/models'