<template>
  <div class="job-detail-page page-container">
    <div class="back-link">
      <el-button text @click="router.back()">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>
    </div>

    <LoadingSpinner v-if="loading" />
    <JobDetailView v-else-if="job" :job="job" />
    <div v-else>
      <EmptyState message="职位不存" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { jobApi } from '@/api/modules/jobhub'
import type { JobDetail } from '@/api/types/models'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import JobDetailView from '@/components/jobhub/JobDetail.vue'

const route = useRoute()
const router = useRouter()

const job = ref<JobDetail | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    job.value = await jobApi.getJob(Number(route.params.id))
  } catch {
    job.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.back-link {
  margin-bottom: 16px;
}
</style>
