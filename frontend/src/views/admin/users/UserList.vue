<template>
  <div class="admin-user-list">
    <div class="header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="router.push('/admin/users/create')">创建用户</el-button>
    </div>

    <el-input
      v-model="keyword"
      placeholder="搜索用户名/邮箱"
      style="width: 240px; margin-bottom: 16px;"
      clearable
      @input="fetchData"
    />

    <el-table :data="tableData" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column prop="role" label="角色" width="100">
        <template #default="{ row }">
          <el-tag :type="row.role === 'admin' ? 'danger' : row.role === 'moderator' ? 'warning' : 'info'" size="small">
            {{ row.role }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240">
        <template #default="{ row }">
          <el-button size="small" @click="router.push(`/admin/users/${row.id}/edit`)">编辑</el-button>
          <el-button
            size="small"
            :type="row.status === 'active' ? 'warning' : 'success'"
            @click="handleToggleStatus(row)"
          >
            {{ row.status === 'active' ? '冻结' : '解冻' }}
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
const keyword = ref('')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const fetchData = async () => {
  loading.value = true
  try {
    const res = await adminApi.getUsers({
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

const handleToggleStatus = async (row: any) => {
  try {
    const newStatus = row.status === 'active' ? 'frozen' : 'active'
    await adminApi.updateUser(row.id, { status: newStatus })
    ElMessage.success(newStatus === 'frozen' ? '已冻结' : '已解冻')
    fetchData()
  } catch {
    // handled
  }
}

const handleDelete = async (id: number) => {
  await ElMessageBox.confirm('确定要删除该用户吗？', '警告', { type: 'warning' })
  try {
    await adminApi.deleteUser(id)
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

.header h2 {
  margin: 0;
}
</style>
