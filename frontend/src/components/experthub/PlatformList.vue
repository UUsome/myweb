<template>
  <div class="platform-list">
    <div v-for="platform in platforms" :key="platform.id" class="platform-item">
      <div class="platform-header">
        <span class="platform-type">{{ platform.platform_name }}</span>
        <span class="platform-type-badge">{{ platform.platform_type }}</span>
      </div>
      <a :href="platform.url || undefined" target="_blank" class="blogger-link">
        {{ platform.blogger_name }}
      </a>
      <p v-if="platform.profile" class="platform-profile">{{ platform.profile }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Platform } from '@/api/types/models'

defineProps<{
  platforms: Platform[]
}>()
</script>

<style scoped>
.platform-item {
  padding: 12px 0;
  border-bottom: 1px solid #E8E2D8;
}

.platform-item:last-child {
  border-bottom: none;
}

.platform-header {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 4px;
}

.platform-type {
  font-weight: 600;
  font-size: 14px;
}

.platform-type-badge {
  font-size: 11px;
  color: #888880;
  background: #F5F0E8;
  padding: 1px 6px;
  border-radius: 4px;
}

.blogger-link {
  font-size: 14px;
  color: #2C406E;
}

.platform-profile {
  font-size: 13px;
  color: #4A4A4A;
  margin: 4px 0 0;
}
</style>
