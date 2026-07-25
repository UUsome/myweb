import apiClient from '../client'

export interface ContactContent {
  content: string
  updated_at?: string
}

export const contactApi = {
  getContact: () => apiClient.get<ContactContent>('/contact'),
  updateContact: (data: ContactContent) => apiClient.put<ContactContent>('/contact', data),
}

export type { ContactContent }
