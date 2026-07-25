import apiClient, { type CursorPageResponse } from '../client'
import type { Job, JobDetail, JobFilterOptions, JobTag } from '../types/models'

export interface JobListParams {
  city?: string
  industry?: string
  job_type?: string
  tag_type?: string
  keyword?: string
  cursor?: string
  limit?: number
}

export const jobApi = {
  getJobs: (params: JobListParams) =>
    apiClient.get<CursorPageResponse<Job>>('/jobs', { params }),

  getJob: (id: number) =>
    apiClient.get<JobDetail>(`/jobs/${id}`),

  getFilterOptions: () =>
    apiClient.get<JobFilterOptions>('/jobs/filters/options'),

  getAvailableTags: () =>
    apiClient.get<JobTag[]>('/jobs/tags/available'),
}

export type * from '../types/models'