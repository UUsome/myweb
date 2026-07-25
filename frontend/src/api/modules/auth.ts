import apiClient from '../client'
import type { LoginParams, LoginResponse, UserInfo } from '../types/models'


export const authApi = {
  login: (params: LoginParams) =>
    apiClient.post<LoginResponse>('/auth/login', params),

  refresh: (refreshToken: string) =>
    apiClient.post<{ access_token: string; refresh_token: string; token_type: string }>(
      '/auth/refresh',
      { refresh_token: refreshToken }
    ),

  logout: () => apiClient.post('/auth/logout'),

  getMe: () => apiClient.get<UserInfo>('/users/me'),
}

export type * from '../types/models'