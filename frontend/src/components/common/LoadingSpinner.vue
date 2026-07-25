<template>
  <div class="loading-spinner" :class="{ fullscreen }">
    <el-icon class="is-loading" :size="size">
      <Loading />
    </el-icon>
    <p v-if="text" class="loading-text">{{ text }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text?: string
  size?: number
  fullscreen?: boolean
}>()
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #888880;
}

.loading-spinner.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(247, 244, 240, 0.85);
  z-index: 999;
}

.loading-text {
  margin-top: 12px;
  font-size: 14px;
  color: #888880;
}
</style>
