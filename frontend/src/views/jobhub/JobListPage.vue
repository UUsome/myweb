<template>
  <div class="job-list-page page-container">
    <JobFilter :options="filterOptions" @change="onFilterChange" />

    <JobCard v-for="job in pagination.items.value" :key="job.id" :job="job" />

    <div ref="sentinel" v-if="pagination.hasMore.value" class="loading-trigger">
      <el-icon v-if="pagination.loading.value" class="is-loading"><Loading /></el-icon>
      <span v-else>加载更多</span>
    </div>

    <EmptyState
      v-if="pagination.initialized.value && !pagination.items.value.length"
      message="暂无职位信息"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { jobApi } from '@/api/modules/jobhub'
import type { JobFilterOptions } from '@/api/types/models'
import { usePagination } from '@/composables/usePagination'
import { useInfiniteScroll } from '@/composables/useInfiniteScroll'
import JobCard from '@/components/jobhub/JobCard.vue'
import JobFilter from '@/components/jobhub/JobFilter.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const filterOptions = ref<JobFilterOptions>({
  cities: [],
  industries: [],
  job_types: [],
})

const pagination = usePagination({
  fetchFn: (p) => jobApi.getJobs(p),
  initialParams: { limit: 20 },
})

const { sentinel } = useInfiniteScroll(pagination.loadMore, pagination.hasMore, pagination.loading)

const onFilterChange = (filters: any) => {
  Object.assign(pagination.params, filters)
  pagination.refresh()
}

onMounted(async () => {
  const [options] = await Promise.all([
    jobApi.getFilterOptions(),
    pagination.refresh(),
  ])
  filterOptions.value = options
})
</script>
