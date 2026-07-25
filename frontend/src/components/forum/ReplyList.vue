<template>
  <div class="reply-list">
    <h3 class="reply-title">回复 ({{ replies.length }})</h3>

    <div v-for="reply in replies" :key="reply.id" class="reply-item">
      <div class="reply-header">
        <el-avatar :size="28">{{ reply.nickname?.charAt(0) || reply.username.charAt(0) }}</el-avatar>
        <span class="reply-author">{{ reply.nickname || reply.username }}</span>
        <span class="reply-time">{{ formatDate(reply.created_at) }}</span>
      </div>
      <div class="reply-content">{{ reply.content }}</div>
      <div class="reply-actions">
        <LikeButton target-type="reply" :target-id="reply.id" size="small" />
      </div>
    </div>

    <EmptyState v-if="!replies.length" message="暂无回复" />
  </div>
</template>

<script setup lang="ts">
import type { Reply } from '@/api/types/models'
import { formatDate } from '@/utils/format'
import LikeButton from '@/components/interactions/LikeButton.vue'
import EmptyState from '@/components/common/EmptyState.vue'

defineProps<{
  replies: Reply[]
}>()
</script>

<style scoped>
.reply-list {
  margin-top: 24px;
}

.reply-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #E8E2D8;
}

.reply-item {
  padding: 16px 0;
  border-bottom: 1px solid #E8E2D8;
}

.reply-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.reply-author {
  font-size: 14px;
  font-weight: 500;
}

.reply-time {
  font-size: 12px;
  color: #888880;
}

.reply-content {
  font-size: 14px;
  line-height: 1.6;
  color: #2C2C2C;
  margin-bottom: 8px;
}

.reply-actions {
  display: flex;
  gap: 12px;
}
</style>
