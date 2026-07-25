<template>
  <div class="case-preview" @click="router.push(`/expert-hub/case/${caseItem.id}`)">
    <div v-if="caseItem.cover_image" class="case-cover">
      <img :src="caseItem.cover_image" :alt="caseItem.name" />
    </div>
    <div class="case-info">
      <h4>{{ caseItem.name }}</h4>
      <p v-if="caseItem.summary">{{ caseItem.summary }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { CaseItem } from '@/api/types/models'

defineProps<{
  caseItem: CaseItem
}>()

const router = useRouter()
</script>

<style scoped>
.case-preview {
  cursor: pointer;
  padding: 8px 0;
}

.case-cover img {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 8px;
}

.case-info h4 {
  margin: 0 0 4px;
  font-size: 14px;
}

.case-info p {
  margin: 0;
  font-size: 13px;
  color: #888880;
}
</style>
