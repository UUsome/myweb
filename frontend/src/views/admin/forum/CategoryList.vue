<template>
  <div class="admin-category-list">
    <div class="header">
      <h2>板块管理</h2>
    <el-button type="primary" @click="handleCreate">
        创建板块
    </el-button>


    </div>

    <el-table :data="categories" v-loading="loading" stripe row-key="id">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="slug" label="标识" />
      <el-table-column prop="sort_order" label="排序" width="80" />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Create/Edit Dialog -->
    <el-dialog v-model="showDialog" :title="editId ? '编辑板块' : '创建板块'" width="500px">
      <el-form :model="categoryForm" label-position="top">
        <el-form-item label="名称" required>
          <el-input v-model="categoryForm.name" />
        </el-form-item>
        <el-form-item label="标识" required>
          <el-input v-model="categoryForm.slug" placeholder="如：frontend" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="categoryForm.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="categoryForm.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSaveCategory">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminApi } from '@/api/modules/admin'
import { forumApi } from '@/api/modules/forum'

const handleCreate = () => {
  editId.value = null
  Object.assign(categoryForm, { name: '', slug: '', description: '', sort_order: 0 })
  showDialog.value = true
}


const categories = ref<any[]>([])
const loading = ref(false)
const showDialog = ref(false)
const editId = ref<number | null>(null)
const saving = ref(false)
const categoryForm = reactive({
  name: '',
  slug: '',
  description: '',
  sort_order: 0,
})

const fetchCategories = async () => {
  loading.value = true
  try {
    const cats = await forumApi.getCategories()
    categories.value = cats
  } finally {
    loading.value = false
  }
}

const handleEdit = (row: any) => {
  editId.value = row.id
  categoryForm.name = row.name
  categoryForm.slug = row.slug
  categoryForm.description = row.description || ''
  categoryForm.sort_order = row.sort_order || 0
  showDialog.value = true
}

const handleSaveCategory = async () => {
  saving.value = true
  try {
    const data = { ...categoryForm }
    if (editId.value) {
      await adminApi.updateCategory(editId.value, data)
      ElMessage.success('更新成功')
    } else {
      await adminApi.createCategory(data)
      ElMessage.success('创建成功')
    }
    showDialog.value = false
    fetchCategories()
  } catch {
    // handled
  } finally {
    saving.value = false
  }
}

const handleDelete = async (id: number) => {
  await ElMessageBox.confirm('确定要删除该板块吗？', '警告', { type: 'warning' })
  try {
    await adminApi.deleteCategory(id)
    ElMessage.success('删除成功')
    fetchCategories()
  } catch {
    // handled
  }
}

onMounted(fetchCategories)
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
