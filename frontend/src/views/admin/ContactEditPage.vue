<template>
  <div class="contact-edit-page">
    <h2 class="page-title">编辑联系我们</h2>

    <el-form label-position="top">
      <el-form-item label="页面内容 (支持 Markdown)">
        <el-input
          v-model="content"
          type="textarea"
          :rows="20"
          placeholder="# 联系我们

## 公司地址
北京市朝阳区...

## 联系方式
- 电话: 010-12345678
- 邮箱: contact@myweb.com

## 商务合作
..."
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" :loading="saving" @click="handleSave">
          保存
        </el-button>
        <el-button @click="router.push('/contact')">
          预览
        </el-button>
      </el-form-item>
    </el-form>

    <div class="preview-section">
      <h3>实时预览</h3>
      <div class="preview-card markdown-body" v-html="renderedContent" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { marked } from 'marked'
import { ElMessage } from 'element-plus'
import { contactApi } from '@/api/modules/contact'

const router = useRouter()
const content = ref('')
const saving = ref(false)

const renderedContent = computed(() => {
  if (!content.value) return '<p style="color:#999">输入 Markdown 内容查看预览...</p>'
  return marked.parse(content.value, { breaks: true })
})

onMounted(async () => {
  try {
    const data = await contactApi.getContact()
    content.value = data.content || ''
  } catch {
    // ignore
  }
})

const handleSave = async () => {
  saving.value = true
  try {
    await contactApi.updateContact({ content: content.value })
    ElMessage.success('保存成功')
  } catch (err: any) {
    ElMessage.error(err.message || '保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.contact-edit-page {
  max-width: 1000px;
  padding: 20px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #1B2A4A;
  margin-bottom: 24px;
}

.preview-section {
  margin-top: 32px;
}

.preview-section h3 {
  font-size: 16px;
  color: #666;
  margin-bottom: 12px;
}

.preview-card {
  background: #f8f8f8;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 24px;
  max-height: 500px;
  overflow-y: auto;
}

.markdown-body {
  line-height: 1.8;
  color: #333;
}

.markdown-body :deep(h2) {
  font-size: 20px;
  color: #1B2A4A;
  margin-top: 20px;
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
}

.markdown-body :deep(strong) {
  color: #1B2A4A;
}
</style>
