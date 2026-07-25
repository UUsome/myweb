<template>
  <div class="admin-post-list">
    <div class="header">
      <h2>帖子管理</h2>
    </div>

    <el-table :data="tableData" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" min-width="250" show-overflow-tooltip />
      <el-table-column prop="username" label="作者" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag
            :type="row.status === 'published' ? 'success' : row.status === 'pinned' ? 'danger' : row.status === 'essence' ? 'warning' : 'info'"
            size="small"
          >
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="comment_count" label="回复" width="60" />
      <el-table-column prop="like_count" label="点赞" width="60" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-select
            v-model="row.status"
            size="small"
            style="width: 100px"
            @change="(val: string) => handleUpdateStatus(row.id, val)"
          >
            <el-option label="已发布" value="published" />
            <el-option label="置顶" value="pinned" />
            <el-option label="精华" value="essence" />
            <el-option label="草稿" value="draft" />
          </el-select>
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminApi } from '@/api/modules/admin'

const tableData = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const fetchData = async () => {
  loading.value = true
  try {
    const res = await adminApi.getPosts({ page: page.value, page_size: pageSize.value })
    tableData.value = res.list
    total.value = res.total
  } finally {
    loading.value = false
  }
}

const handleUpdateStatus = async (id: number, status: string) => {
  try {
    await adminApi.updatePost(id, { status })
    ElMessage.success('状态更新成功')
  } catch {
    // handled
  }
}

const handleDelete = async (id: number) => {
  await ElMessageBox.confirm('确定要删除该帖子吗？', '警告', { type: 'warning' })
  try {
    await adminApi.deletePost(id)
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
