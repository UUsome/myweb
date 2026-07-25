export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  // Within 1 minute
  if (diff < 60000) return '刚刚'
  // Within 1 hour
  if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`
  // Within 1 day
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小时前`
  // Within 7 days
  if (diff < 604800000) return `${Math.floor(diff / 86400000)} 天前`

  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

export function truncate(text: string, maxLen = 100): string {
  if (text.length <= maxLen) return text
  return text.slice(0, maxLen) + '...'
}
