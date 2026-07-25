<template>
  <div class="admin-job-list">
    <div class="header">
      <h2>职位管理</h2>
      <el-button type="primary" @click="router.push('/admin/jobs/create')">创建职位</el-button>
    </div>

    <el-table :data="tableData" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="职位名称" min-width="200" />
      <el-table-column prop="company_name" label="公司" />
      <el-table-column prop="city" label="城市" width="100" />
      <el-table-column prop="job_type" label="类型" width="80" />
      <el-table-column prop="is_active" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
            {{ row.is_active ? '上架' : '下架' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_featured" label="置顶" width="60">
        <template #default="{ row }">
          <el-tag v-if="row.is_featured" type="warning" size="small">置顶</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="view_count" label="浏览" width="70" />
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button size="small" @click="router.push(`/admin/jobs/${row.id}/edit`)">编辑</el-button>
          <el-button size="small" :type="row.is_featured ? 'warning' : 'default'" @click="handleToggleFeatured(row)">
            {{ row.is_featured ? '取消置顶' : '置顶' }}
          </el-button>
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
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const fetchData = async () => {
  loading.value = true
  try {
    const res = await adminApi.getJobs({ page: page.value, page_size: pageSize.value })
    tableData.value = res.list
    total.value = res.total
  } finally {
    loading.value = false
  }
}

const handleToggleFeatured = async (row: any) => {
  try {
    await adminApi.updateJob(row.id, { is_featured: !row.is_featured })
    ElMessage.success(row.is_featured ? '已取消置顶' : '已置顶')
    fetchData()
  } catch {
    // handled
  }
}

const handleDelete = async (id: number) => {
  await ElMessageBox.confirm('确定要删除该职位吗？', '警告', { type: 'warning' })
  try {
    await adminApi.deleteJob(id)
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
