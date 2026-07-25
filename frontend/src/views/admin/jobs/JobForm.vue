<template>
  <div class="admin-job-form">
    <h2>{{ isEdit ? '编辑职位' : '创建职位' }}</h2>

    <el-form :model="form" label-position="top" style="max-width: 700px">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="职位名称" required>
            <el-input v-model="form.title" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="公司名称" required>
            <el-input v-model="form.company_name" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="薪资" required>
            <el-input v-model="form.salary_text" placeholder="20K-35K·14薪" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="城市" required>
            <el-input v-model="form.city" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="行业" required>
            <el-input v-model="form.industry" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="职位类型">
        <el-select v-model="form.job_type" style="width: 100%">
          <el-option label="全职" value="全职" />
          <el-option label="兼职" value="兼职" />
          <el-option label="实习" value="实习" />
        </el-select>
      </el-form-item>

      <el-form-item label="职位描述">
        <el-input v-model="form.description" type="textarea" :rows="6" />
      </el-form-item>

      <el-form-item label="任职要求">
        <el-input v-model="form.requirements" type="textarea" :rows="6" />
      </el-form-item>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="联系人姓名" required>
            <el-input v-model="form.contact_name" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="关联专家（可选）">
            <el-select v-model="form.contact_expert_id" placeholder="选择关联专家" clearable filterable style="width: 100%">
              <el-option v-for="e in experts" :key="e.id" :label="`${e.name} (${e.title || '专家'})`" :value="e.id" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item>
        <el-checkbox v-model="form.is_active">上架</el-checkbox>
        <el-checkbox v-model="form.is_featured">置顶</el-checkbox>
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
import { jobApi } from '@/api/modules/jobhub'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const saving = ref(false)
const experts = ref<{ id: number; name: string; title: string | null }[]>([])

const form = ref({
  title: '',
  company_name: '',
  company_logo: '',
  salary_text: '',
  city: '',
  industry: '',
  job_type: '全职',
  description: '',
  requirements: '',
  contact_name: '',
  contact_expert_id: null as number | null,
  is_active: true,
  is_featured: false,
})

onMounted(async () => {
  // Load experts list for selector
  try {
    const res = await adminApi.getExperts({ page: 1, page_size: 100 })
    experts.value = res.list.map((e: any) => ({ id: e.id, name: e.name, title: e.title }))
  } catch {
    // ignore
  }

  if (isEdit.value) {
    try {
      const job = await jobApi.getJob(Number(route.params.id))
      form.value = {
        title: job.title,
        company_name: job.company_name,
        company_logo: job.company_logo || '',
        salary_text: job.salary_text,
        city: job.city,
        industry: job.industry,
        job_type: job.job_type,
        description: job.description || '',
        requirements: job.requirements || '',
        contact_name: job.contact_name,
        contact_expert_id: job.contact_expert_id,
        is_active: job.is_active,
        is_featured: job.is_featured,
      }
    } catch {
      // ignore
    }
  }
})

const handleSave = async () => {
  saving.value = true
  try {
    const data = { ...form.value }
    if (isEdit.value) {
      await adminApi.updateJob(Number(route.params.id), data)
      ElMessage.success('更新成功')
    } else {
      await adminApi.createJob(data)
      ElMessage.success('创建成功')
    }
    router.push('/admin/jobs')
  } catch {
    // handled
  } finally {
    saving.value = false
  }
}
</script>
