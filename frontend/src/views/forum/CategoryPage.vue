<template>
  <div class="category-page page-container">
    <h2>{{ categoryName }}</h2>
    <PostCard v-for="post in pagination.items.value" :key="post.id" :post="post" />

    <div ref="sentinel" v-if="pagination.hasMore.value" class="loading-trigger">
      <el-icon v-if="pagination.loading.value" class="is-loading"><Loading /></el-icon>
    </div>

    <EmptyState v-if="pagination.initialized.value && !pagination.items.value.length" message="该板块暂无帖子" />
  </div>
</template>

<script setup lang="ts">
import { computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { forumApi } from '@/api/modules/forum'
import { useForumStore } from '@/stores/forum'
import { usePagination } from '@/composables/usePagination'
import { useInfiniteScroll } from '@/composables/useInfiniteScroll'
import PostCard from '@/components/forum/PostCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const route = useRoute()
const forumStore = useForumStore()

const categoryId = computed(() => Number(route.params.id))
const categoryName = computed(() => {
  const findCat = (cats: any[]): string => {
    for (const c of cats) {
      if (c.id === categoryId.value) return c.name
      if (c.children) {
        const found = findCat(c.children)
        if (found) return found
      }
    }
    return '帖子列表'
  }
  return findCat(forumStore.categories)
})

const pagination = usePagination({
  fetchFn: (p) => forumApi.getPosts(p),
  initialParams: { limit: 20 },
})

const { sentinel } = useInfiniteScroll(pagination.loadMore, pagination.hasMore, pagination.loading)

watch(categoryId, () => {
  pagination.params.category_id = categoryId.value
  pagination.refresh()
})

onMounted(() => {
  forumStore.fetchCategories()
  pagination.params.category_id = categoryId.value
  pagination.refresh()
})
</script>
