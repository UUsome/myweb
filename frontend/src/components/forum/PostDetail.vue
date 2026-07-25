<template>
  <div v-if="post" class="post-detail">
    <div class="post-header">
      <h1 class="post-title">{{ post.title }}</h1>
      <div class="post-meta">
        <span>作者：{{ post.nickname || post.username }}</span>
        <span>板块：{{ post.category_name }}</span>
        <span>发布于：{{ formatDate(post.created_at) }}</span>
        <span v-if="post.status === 'pinned'" class="badge pinned">置顶</span>
        <span v-if="post.status === 'essence'" class="badge essence">精华</span>
      </div>
    </div>

    <div class="post-content markdown-body" v-html="renderedContent" />

    <div class="post-actions">
      <LikeButton target-type="post" :target-id="post.id" />
    </div>

    <CommentSection target-type="post" :target-id="post.id" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import type { PostDetail as PostDetailType } from '@/api/types/models'
import { formatDate } from '@/utils/format'
import LikeButton from '@/components/interactions/LikeButton.vue'
import CommentSection from '@/components/interactions/CommentSection.vue'

const props = defineProps<{
  post: PostDetailType | null
}>()

const renderedContent = computed(() => {
  if (!props.post?.content) return ''
  return marked.parse(props.post.content, { async: false }) as string
})
</script>

<style scoped>
.post-detail {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  border: 1px solid #E8E2D8;
}

.post-header {
  margin-bottom: 24px;
}

.post-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 12px;
}

.post-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #888880;
  flex-wrap: wrap;
  align-items: center;
}

.badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.badge.pinned {
  background: rgba(194, 107, 107, 0.1);
  color: #C26B6B;
}

.badge.essence {
  background: rgba(196, 151, 62, 0.1);
  color: #C4973E;
}

.post-content {
  line-height: 1.8;
  font-size: 15px;
  color: #2C2C2C;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #E8E2D8;
}

.post-actions {
  margin-bottom: 32px;
}
</style>
