import apiClient, { type CursorPageResponse } from '../client'
import type { Tag, Service, Expert, ExpertDetail, ExpertHover, Platform, CaseItem } from '../types/models'

export interface ExpertListParams {
  tag?: string[]
  service?: string[]
  keyword?: string
  cursor?: string
  limit?: number
}

export const experthubApi = {
  getTags: () => apiClient.get<Tag[]>('/tags'),

  getServices: () => apiClient.get<Service[]>('/services'),

  getExperts: (params: ExpertListParams) =>
    apiClient.get<CursorPageResponse<Expert>>('/experts', { params }),

  getExpert: (id: number) =>
    apiClient.get<ExpertDetail>(`/experts/${id}`),

  getExpertHover: (id: number) =>
    apiClient.get<ExpertHover>(`/experts/${id}/hover`),

  getExpertPlatforms: (id: number) =>
    apiClient.get<Platform[]>(`/experts/${id}/platforms`),

  getExpertCases: (id: number) =>
    apiClient.get<CaseItem[]>(`/experts/${id}/cases`),

  getCase: (caseId: number) =>
    apiClient.get<CaseItem & { content: string | null }>(`/experts/cases/${caseId}`),
}

export type * from '../types/models'