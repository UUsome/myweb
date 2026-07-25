<template>
  <div class="admin-user-form">
    <h2>{{ isEdit ? '编辑用户' : '创建用户' }}</h2>

    <el-form :model="form" label-position="top" style="max-width: 500px">
      <el-form-item label="用户名" required>
        <el-input v-model="form.username" :disabled="isEdit" />
      </el-form-item>
      <el-form-item label="邮箱" required>
        <el-input v-model="form.email" />
      </el-form-item>
      <el-form-item label="密码" :required="!isEdit">
        <el-input v-model="form.password" type="password" show-password :placeholder="isEdit ? '留空则不修改' : ''" />
      </el-form-item>
      <el-form-item label="昵称">
        <el-input v-model="form.nickname" />
      </el-form-item>
      <el-form-item label="角色">
        <el-select v-model="form.role" style="width: 100%">
          <el-option label="管理员" value="admin" />
          <el-option label="版主" value="moderator" />
          <el-option label="成员" value="member" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="form.status" style="width: 100%">
          <el-option label="正常" value="active" />
          <el-option label="冻结" value="frozen" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
        <el-button @click="router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { adminApi } from '@/api/modules/admin'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const saving = ref(false)

const form = ref({
  username: '',
  email: '',
  password: '',
  nickname: '',
  role: 'member',
  status: 'active',
})

onMounted(async () => {
  if (isEdit.value) {
    // Load user data
    try {
      const res = await adminApi.getUsers({ page: 1, page_size: 100 })
      const user = res.list.find((u: any) => u.id === Number(route.params.id))
      if (user) {
        form.value = { ...form.value, ...user, password: '' }
      }
    } catch {
      // ignore
    }
  }
})

const handleSave = async () => {
  saving.value = true
  try {
    if (isEdit.value) {
      const updateData: Record<string, any> = { ...form.value }
      if (!updateData.password) delete updateData.password
      delete updateData.username
      await adminApi.updateUser(Number(route.params.id), updateData)
      ElMessage.success('更新成功')
    } else {
      await adminApi.createUser(form.value)
      ElMessage.success('创建成功')
    }
    router.push('/admin/users')
  } catch {
    // handled
  } finally {
    saving.value = false
  }
}
</script>
