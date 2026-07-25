<template>
  <div class="post-detail-page page-container">
    <div class="back-link">
      <el-button text @click="router.back()">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>
    </div>

    <LoadingSpinner v-if="loading" />


<PostDetailCard v-else-if="post" :post="post" />
    <div v-else-if="!loading && !post">
      <EmptyState message="帖子不存在" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { forumApi } from '@/api/modules/forum'
import type { PostDetail } from '@/api/types/models'
import PostDetailCard from '@/components/forum/PostDetail.vue'  

import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const route = useRoute()
const router = useRouter()

const post = ref<PostDetail | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    post.value = await forumApi.getPost(Number(route.params.id))
  } catch {
    post.value = null
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
