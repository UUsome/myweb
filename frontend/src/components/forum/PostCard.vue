<template>
  <div class="post-card card" @click="router.push(`/forum/post/${post.id}`)">
    <div class="post-header">
      <h3 class="post-title">{{ post.title }}</h3>
      <el-tag v-if="post.status === 'pinned'" size="small" type="danger">置顶</el-tag>
      <el-tag v-else-if="post.status === 'essence'" size="small" type="warning">精华</el-tag>
    </div>

    <div class="post-meta">
      <span class="meta-item">{{ post.nickname || post.username }}</span>
      <span class="meta-divider">·</span>
      <span class="meta-item">{{ post.category_name }}</span>
      <span class="meta-divider">·</span>
      <span class="meta-item">{{ formatDate(post.created_at) }}</span>
    </div>

    <div class="post-stats">
      <span><el-icon><ChatDotSquare /></el-icon> {{ post.comment_count }}</span>
      <span><el-icon><ThumbsUp /></el-icon> {{ post.like_count }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Post } from '@/api/types/models'
import { formatDate } from '@/utils/format'

defineProps<{
  post: Post
}>()

const router = useRouter()
</script>

<style scoped>
.post-card {
  cursor: pointer;
  margin-bottom: 12px;
  padding: 16px 20px;
}

.post-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.post-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #2C2C2C;
}

.post-meta {
  font-size: 13px;
  color: #888880;
  margin-bottom: 8px;
}

.meta-divider {
  margin: 0 6px;
}

.post-stats {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #888880;
}

.post-stats .el-icon {
  margin-right: 4px;
  vertical-align: middle;
}
</style>
