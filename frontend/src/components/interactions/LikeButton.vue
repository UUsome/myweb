<template>
  <div class="like-button" :class="{ liked: isLiked }">
    <el-button
      :size="size"
      :type="isLiked ? 'primary' : 'default'"
      :loading="loading"
      circle
      @click="handleToggle"
    >
      <el-icon><ThumbsUp /></el-icon>
    </el-button>
    <span class="like-count">{{ likeCount }}</span>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { interactionsApi } from '@/api/modules/interactions'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  targetType: string
  targetId: number
  size?: 'small' | 'default' | 'large'
}>()

const userStore = useUserStore()
const isLiked = ref(false)
const likeCount = ref(0)
const loading = ref(false)

const handleToggle = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }

  loading.value = true
  try {
    const result = await interactionsApi.toggleLike(props.targetType, props.targetId)
    isLiked.value = result.is_liked
    likeCount.value = result.like_count
  } catch {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const result = await interactionsApi.getLikeCount(props.targetType, props.targetId)
    likeCount.value = result.like_count

    if (userStore.isLoggedIn) {
      const status = await interactionsApi.getLikeStatus(props.targetType, props.targetId)
      isLiked.value = status.is_liked
    }
  } catch {
    // ignore
  }
})
</script>

<style scoped>
.like-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.like-button.liked .el-button {
  color: #fff;
}

.like-count {
  font-size: 13px;
  color: #888880;
}
</style>
