import apiClient from '../client'
import type { UserInfo, UserPublic } from '../types/models'

export const usersApi = {
  updateMe: (data: Partial<Pick<UserInfo, 'nickname' | 'avatar_url' | 'email'>>) =>
    apiClient.put<UserInfo>('/users/me', data),

  getUser: (id: number) => apiClient.get<UserPublic>(`/users/${id}`),
}
