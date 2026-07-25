// ── 用户 & 认证 ──

export interface LoginParams {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface UserInfo {
  id: number
  username: string
  email: string
  nickname: string | null
  avatar_url: string | null
  role: 'admin' | 'moderator' | 'member'
  status: 'active' | 'frozen'
  created_at?: string
  updated_at?: string
}

export interface UserPublic {
  id: number
  username: string
  nickname: string | null
  avatar_url: string | null
  role: 'admin' | 'moderator' | 'member'
}

// ── 论坛 ──

export interface Category {
  id: number
  name: string
  slug: string
  parent_id: number | null
  description: string | null
  sort_order: number
  children: Category[]
}

export interface Post {
  id: number
  title: string
  category_id: number
  user_id: number
  status: 'draft' | 'published' | 'pinned' | 'essence'
  like_count: number
  comment_count: number
  username: string
  nickname: string | null
  category_name: string
  created_at: string
  updated_at: string
}

export interface PostDetail {
  id: number
  title: string
  content: string
  category_id: number
  user_id: number
  status: 'draft' | 'published' | 'pinned' | 'essence'
  like_count: number
  comment_count: number
  attachments: Record<string, any> | null
  username: string
  nickname: string | null
  category_name: string
  created_at: string
  updated_at: string
}

export interface Reply {
  id: number
  post_id: number
  user_id: number
  content: string
  like_count: number
  comment_count: number
  username: string
  nickname: string | null
  created_at: string
  updated_at: string
}

// ── 专家卡片 ──

export interface Tag {
  id: number
  name: string
  slug: string
  description?: string
  sort_order?: number
}

export interface Service {
  id: number
  name: string
  slug: string
  description?: string
  sort_order?: number
}

export interface Platform {
  id: number
  expert_id: number
  platform_type: string
  platform_name: string
  icon: string | null
  blogger_name: string
  profile: string | null
  url: string | null
  sort_order: number
}

export interface CaseItem {
  id: number
  expert_id: number
  name: string
  summary: string | null
  content?: string | null
  cover_image: string | null
  sort_order: number
}

export interface Expert {
  id: number
  name: string
  title: string | null
  summary: string
  avatar_url: string | null
  tags: Tag[]
  services: Service[]
  platform_count: number
  case_count: number
  is_published: boolean
  sort_order: number
  created_at?: string
  updated_at?: string
}

export interface ExpertDetail extends Expert {
  contact_email: string | null
  contact_phone: string | null
  contact_wechat: string | null
  platforms: Platform[]
  cases: CaseItem[]
}

export interface ExpertHover {
  id: number
  name: string
  title: string | null
  summary: string
  avatar_url: string | null
  platform_count: number
  case_count: number
  platforms: Platform[]
  cases: CaseItem[]
  tags: Tag[]
}

// ── 职位 ──

export interface JobTag {
  type: 'internal' | 'urgent' | 'expert'
  label: string
  color: string
}

export interface Job {
  id: number
  title: string
  company_name: string
  company_logo: string | null
  salary_text: string
  city: string
  industry: string
  job_type: string
  tags: JobTag[]
  is_active: boolean
  is_featured: boolean
  view_count: number
  contact_name: string
  contact_expert_id: number | null
  created_at?: string
  updated_at?: string
}

export interface JobDetail extends Job {
  description: string | null
  requirements: string | null
  benefits: string[] | null
  expires_at: string | null
  contact_expert: {
    id: number
    name: string
    title: string | null
    avatar_url: string | null
    summary: string
  } | null
}

export interface JobFilterOptions {
  cities: string[]
  industries: string[]
  job_types: string[]
}

// ── 互动（点赞/评论） ──

export interface LikeStatus {
  is_liked: boolean
  like_count: number
}

export interface CommentItem {
  id: number
  user_id: number
  target_type: string
  target_id: number
  parent_id: number | null
  content: string
  depth: number
  username: string
  nickname: string | null
  avatar_url: string | null
  children: CommentItem[]
  created_at: string
  updated_at: string
}
