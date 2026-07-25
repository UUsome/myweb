<template>
  <div class="expert-list-page page-container">
    <!-- Filter Bar -->
    <div class="filter-bar">
      <el-select
        v-model="selectedTagSlugs"
        multiple
        placeholder="擅长领域"
        clearable
        collapse-tags
        style="width: 220px"
        @change="onFilterChange"
      >
        <el-option v-for="tag in store.tags" :key="tag.id" :label="tag.name" :value="tag.slug" />
      </el-select>

      <el-select
        v-model="selectedServiceSlugs"
        multiple
        placeholder="服务形式"
        clearable
        collapse-tags
        style="width: 220px"
        @change="onFilterChange"
      >
        <el-option v-for="svc in store.services" :key="svc.id" :label="svc.name" :value="svc.slug" />
      </el-select>

      <el-input
        v-model="keyword"
        placeholder="搜索专家姓名/简介"
        clearable
        style="width: 240px"
        @input="onFilterChange"
      />
    </div>

    <!-- Expert Grid -->
    <div class="grid-auto">
      <ExpertCard
        v-for="expert in pagination.items.value"
        :key="expert.id"
        :expert="expert"
      />
    </div>

    <!-- Load More -->
    <div ref="sentinel" v-if="pagination.hasMore.value" class="loading-trigger">
      <el-icon v-if="pagination.loading.value" class="is-loading"><Loading /></el-icon>
      <span v-else>加载更多</span>
    </div>

    <EmptyState
      v-if="pagination.initialized.value && !pagination.items.value.length"
      message="暂无专家数据"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { experthubApi } from '@/api/modules/experthub'
import { useExpertHubStore } from '@/stores/experthub'
import { usePagination } from '@/composables/usePagination'
import { useInfiniteScroll } from '@/composables/useInfiniteScroll'
import ExpertCard from '@/components/experthub/ExpertCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const store = useExpertHubStore()

const selectedTagSlugs = ref<string[]>([])
const selectedServiceSlugs = ref<string[]>([])
const keyword = ref('')

const pagination = usePagination({
  fetchFn: (p) => experthubApi.getExperts(p),
  initialParams: { limit: 20 },
})

const { sentinel } = useInfiniteScroll(pagination.loadMore, pagination.hasMore, pagination.loading)

const onFilterChange = () => {
  pagination.params.tag = selectedTagSlugs.value.length ? selectedTagSlugs.value : undefined
  pagination.params.service = selectedServiceSlugs.value.length ? selectedServiceSlugs.value : undefined
  pagination.params.keyword = keyword.value || undefined
  pagination.refresh()
}

onMounted(async () => {
  await Promise.all([
    store.fetchTags(),
    store.fetchServices(),
    pagination.refresh(),
  ])
})
</script>
