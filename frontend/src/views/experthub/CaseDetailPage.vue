<template>
  <div class="case-detail-page page-container">
    <div class="back-link">
      <el-button text @click="router.back()">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>
    </div>

    <LoadingSpinner v-if="loading" />

    <div v-else-if="caseData" class="case-detail card">
      <h1>{{ caseData.name }}</h1>
      <p v-if="caseData.summary" class="case-summary">{{ caseData.summary }}</p>
      <div v-if="caseData.content" class="case-content markdown-body" v-html="renderedContent" />
    </div>

    <div v-else>
      <EmptyState message="案例不存在" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import { experthubApi } from '@/api/modules/experthub'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const route = useRoute()
const router = useRouter()

const caseData = ref<any>(null)
const loading = ref(true)

const renderedContent = computed(() => {
  if (!caseData.value?.content) return ''
  return marked.parse(caseData.value.content, { async: false }) as string
})

onMounted(async () => {
  try {
    caseData.value = await experthubApi.getCase(Number(route.params.id))
  } catch {
    caseData.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.back-link {
  margin-bottom: 16px;
}

.case-detail {
  padding: 32px;
}

.case-detail h1 {
  margin: 0 0 16px;
  font-size: 24px;
}

.case-summary {
  color: #4A4A4A;
  font-size: 15px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #E8E2D8;
}

.case-content {
  line-height: 1.8;
  font-size: 15px;
}
</style>
