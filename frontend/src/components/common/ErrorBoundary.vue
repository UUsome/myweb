<template>
  <div v-if="hasError" class="error-boundary">
    <el-icon :size="48" color="#f56c6c"><WarningFilled /></el-icon>
    <h3>出错了</h3>
    <p>{{ errorMessage }}</p>
    <el-button type="primary" @click="handleRetry">重试</el-button>
  </div>
  <slot v-else />
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  errorMessage?: string
}>()

const emit = defineEmits<{
  retry: []
}>()

const hasError = ref(false)

const handleRetry = () => {
  hasError.value = false
  emit('retry')
}
</script>

<style scoped>
.error-boundary {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.error-boundary h3 {
  margin: 16px 0 8px;
  color: #2C2C2C;
}

.error-boundary p {
  color: #888880;
  margin-bottom: 16px;
}
</style>
