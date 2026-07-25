<template>
  <div class="admin-expert-list">
    <div class="header">
      <h2>专家管理</h2>
      <el-button type="primary" @click="router.push('/admin/experts/create')">创建专家</el-button>
    </div>

    <el-input
      v-model="keyword"
      placeholder="搜索专家名称"
      style="width: 240px; margin-bottom: 16px;"
      clearable
      @input="fetchData"
    />

    <el-table :data="tableData" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="title" label="头衔" />
      <el-table-column prop="summary" label="简介" show-overflow-tooltip />
      <el-table-column prop="is_published" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_published ? 'success' : 'danger'" size="small">
            {{ row.is_published ? '发布' : '下架' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" @click="router.push(`/admin/experts/${row.id}/edit`)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="page"
      v-model:page-size="pageSize"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="fetchData"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminApi } from '@/api/modules/admin'

const router = useRouter()

const tableData = ref<any[]>([])
const loading = ref(false)
const keyword = ref('')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const fetchData = async () => {
  loading.value = true
  try {
    const res = await adminApi.getExperts({
      keyword: keyword.value || undefined,
      page: page.value,
      page_size: pageSize.value,
    })
    tableData.value = res.list
    total.value = res.total
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id: number) => {
  await ElMessageBox.confirm('确定要删除该专家吗？', '警告', { type: 'warning' })
  try {
    await adminApi.deleteExpert(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch {
    // handled
  }
}

onMounted(fetchData)
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
