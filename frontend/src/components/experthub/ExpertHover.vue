<template>
  <div class="expert-hover" v-if="data">
    <div class="hover-header">
      <el-avatar :size="40" :src="data.avatar_url || undefined">{{ data.name.charAt(0) }}</el-avatar>
      <div>
        <h4>{{ data.name }}</h4>
        <p>{{ data.title || '专家' }}</p>
      </div>
    </div>
    <p class="hover-summary">{{ data.summary }}</p>
    <div class="hover-tags">
      <el-tag v-for="tag in data.tags" :key="tag.id" size="small">{{ tag.name }}</el-tag>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ExpertHover as ExpertHoverType } from '@/api/types/models'

defineProps<{
  data: ExpertHoverType | null
}>()
</script>

<style scoped>
.expert-hover {
  padding: 8px;
}

.hover-header {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 8px;
}

.hover-header h4 {
  margin: 0;
  font-size: 15px;
}

.hover-header p {
  margin: 2px 0 0;
  font-size: 13px;
  color: #888880;
}

.hover-summary {
  font-size: 13px;
  color: #4A4A4A;
  margin-bottom: 8px;
}

.hover-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
</style>
