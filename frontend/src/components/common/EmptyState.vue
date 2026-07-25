<template>
  <div class="empty-state">
    <el-icon :size="48" color="#B0ADA5"><FolderOpened /></el-icon>
    <p class="empty-text">{{ message }}</p>
    <el-button v-if="actionText" type="primary" @click="$emit('action')">
      {{ actionText }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message?: string
  actionText?: string
}>()

defineEmits<{
  action: []
}>()
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.empty-text {
  margin-top: 16px;
  font-size: 14px;
  color: #888880;
}
</style>
