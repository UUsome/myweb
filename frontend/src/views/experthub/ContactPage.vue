<template>
  <div class="contact-page page-container">
    <div class="contact-card">
      <h1 class="page-title">联系我们</h1>
      <div v-if="loading" class="loading-wrap">
        <LoadingSpinner />
      </div>
      <div v-else-if="content" class="markdown-body" v-html="renderedContent" />
      <EmptyState v-else message="暂无内容" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { marked } from 'marked'
import { contactApi } from '@/api/modules/contact'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const content = ref('')
const loading = ref(true)

const renderedContent = computed(() => {
  if (!content.value) return ''
  return marked.parse(content.value, { breaks: true })
})

onMounted(async () => {
  try {
    const data = await contactApi.getContact()
    content.value = data.content || ''
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.contact-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.contact-card {
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1B2A4A;
  margin-bottom: 24px;
  text-align: center;
}

.loading-wrap {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.markdown-body {
  line-height: 1.8;
  color: #333;
}

.markdown-body :deep(h2) {
  font-size: 20px;
  color: #1B2A4A;
  margin-top: 24px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.markdown-body :deep(p) {
  margin-bottom: 16px;
}

.markdown-body :deep(ul) {
  padding-left: 20px;
  margin-bottom: 16px;
}

.markdown-body :deep(li) {
  margin-bottom: 8px;
}

.markdown-body :deep(a) {
  color: #409EFF;
  text-decoration: none;
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

.markdown-body :deep(strong) {
  color: #1B2A4A;
}
</style>
