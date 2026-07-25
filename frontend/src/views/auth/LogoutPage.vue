<template>
  <div class="logout-page">
    <LoadingSpinner text="正在退出..." />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const router = useRouter()
const userStore = useUserStore()

onMounted(async () => {
  await userStore.logout()
  router.push('/login')
})
</script>
