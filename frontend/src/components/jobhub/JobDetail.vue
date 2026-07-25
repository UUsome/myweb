<template>
  <div v-if="job" class="job-detail">
    <div class="job-header card">
      <div class="header-top">
        <div class="company-info">
          <el-avatar :size="56" :src="job.company_logo || undefined">
            {{ job.company_name.charAt(0) }}
          </el-avatar>
          <div>
            <h1>{{ job.title }}</h1>
            <p class="company">{{ job.company_name }}</p>
          </div>
        </div>
        <div class="salary">{{ job.salary_text }}</div>
      </div>

      <div class="job-tags">
        <el-tag v-for="tag in job.tags" :key="tag.type" size="small" :style="{
          backgroundColor: tag.color + '20',
          color: tag.color,
          borderColor: tag.color + '40'
        }">{{ tag.label }}</el-tag>
      </div>

      <div class="job-info">
        <span><el-icon><Location /></el-icon> {{ job.city }}</span>
        <span><el-icon><DataBoard /></el-icon> {{ job.industry }}</span>
        <span><el-icon><Clock /></el-icon> {{ job.job_type }}</span>
        <span>👁️ {{ job.view_count }} 次浏览</span>
      </div>
    </div>

    <div v-if="job.description" class="job-section card">
      <h3>职位描述</h3>
      <div class="job-content" v-html="job.description" />
    </div>

    <div v-if="job.requirements" class="job-section card">
      <h3>任职要求</h3>
      <div class="job-content" v-html="job.requirements" />
    </div>

    <div v-if="job.benefits?.length" class="job-section card">
      <h3>福利待遇</h3>
      <div class="benefits">
        <el-tag v-for="b in job.benefits" :key="b" type="success" effect="plain">{{ b }}</el-tag>
      </div>
    </div>

    <!-- Contact Expert -->
    <div v-if="job.contact_expert" class="job-section card contact-card" @click="router.push(`/expert-hub/${job.contact_expert?.id}`)">
      <h3>联系人</h3>
      <div class="contact-info">
        <el-avatar :size="48" :src="job.contact_expert.avatar_url || undefined">
          {{ job.contact_expert.name.charAt(0) }}
        </el-avatar>
        <div>
          <p class="contact-name">{{ job.contact_expert.name }}</p>
          <p class="contact-title">{{ job.contact_expert.title || '专家' }}</p>
        </div>
        <el-button type="primary" size="small">查看专家主页</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { JobDetail } from '@/api/types/models'

defineProps<{
  job: JobDetail | null
}>()

const router = useRouter()
</script>

<style scoped>
.job-header {
  margin-bottom: 20px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.company-info {
  display: flex;
  gap: 16px;
}

.company-info h1 {
  margin: 0 0 4px;
  font-size: 22px;
}

.company {
  margin: 0;
  color: #888880;
}

.salary {
  font-size: 20px;
  font-weight: 700;
  color: #C26B6B;
  white-space: nowrap;
}

.job-tags {
  display: flex;
  gap: 6px;
  margin-bottom: 8px;
}

.job-info {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #4A4A4A;
}

.job-section {
  margin-bottom: 20px;
}

.job-section h3 {
  margin-top: 0;
  padding-bottom: 12px;
  border-bottom: 1px solid #E8E2D8;
}

.job-content {
  line-height: 1.8;
  font-size: 15px;
}

.benefits {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.contact-card {
  cursor: pointer;
}

.contact-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.contact-name {
  margin: 0;
  font-weight: 600;
}

.contact-title {
  margin: 2px 0 0;
  font-size: 13px;
  color: #909399;
}
</style>
