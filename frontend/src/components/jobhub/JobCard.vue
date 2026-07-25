<template>
  <div class="job-card card" @click="router.push(`/jobs/${job.id}`)">
    <div class="job-header">
      <div class="company-info">
        <el-avatar :size="40" :src="job.company_logo || undefined">
          {{ job.company_name.charAt(0) }}
        </el-avatar>
        <div>
          <h3 class="job-title">{{ job.title }}</h3>
          <p class="company-name">{{ job.company_name }}</p>
        </div>
      </div>
      <div class="salary">{{ job.salary_text }}</div>
    </div>

    <div class="job-tags">
      <el-tag
        v-for="tag in job.tags"
        :key="tag.type"
        size="small"
        :style="{ backgroundColor: tag.color + '20', color: tag.color, borderColor: tag.color + '40' }"
      >
        {{ tag.label }}
      </el-tag>
      <el-tag v-if="job.is_featured" size="small" type="warning">置顶</el-tag>
    </div>

    <div class="job-meta">
      <span>{{ job.city }}</span>
      <span>{{ job.industry }}</span>
      <span>{{ job.job_type }}</span>
    </div>

    <div class="job-footer">
      <span class="contact">联系人：{{ job.contact_name }}</span>
      <span class="views">👁️ {{ job.view_count }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Job } from '@/api/types/models'

defineProps<{
  job: Job
}>()

const router = useRouter()
</script>

<style scoped>
.job-card {
  cursor: pointer;
  margin-bottom: 16px;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.company-info {
  display: flex;
  gap: 12px;
}

.job-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px;
}

.company-name {
  font-size: 13px;
  color: #888880;
  margin: 0;
}

.salary {
  font-size: 16px;
  font-weight: 700;
  color: #C26B6B;
  white-space: nowrap;
}

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.job-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #888880;
  margin-bottom: 8px;
}

.job-footer {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #888880;
  padding-top: 8px;
  border-top: 1px solid #E8E2D8;
}
</style>
