<template>
  <div class="admin-expert-form">
    <h2>{{ isEdit ? '编辑专家' : '创建专家' }}</h2>

    <el-form :model="form" label-position="top" style="max-width: 600px">
      <el-form-item label="姓名" required>
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="头衔">
        <el-input v-model="form.title" placeholder="如：AI 技术专家" />
      </el-form-item>
      <el-form-item label="核心简介" required>
        <el-input v-model="form.summary" type="textarea" :rows="3" />
      </el-form-item>
      <el-form-item label="头像 URL">
        <el-input v-model="form.avatar_url" placeholder="https://..." />
      </el-form-item>

      <el-divider>联系方式（选填）</el-divider>

      <el-form-item label="邮箱">
        <el-input v-model="form.contact_email" />
      </el-form-item>
      <el-form-item label="电话">
        <el-input v-model="form.contact_phone" />
      </el-form-item>
      <el-form-item label="微信">
        <el-input v-model="form.contact_wechat" />
      </el-form-item>

      <el-form-item label="发布状态">
        <el-switch v-model="form.is_published" active-text="发布" inactive-text="下架" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
        <el-button @click="router.back()">取消</el-button>
      </el-form-item>
    </el-form>

    <!-- ── 平台管理 ── -->
    <template v-if="isEdit">
      <el-divider />
      <div class="section-header">
        <h3>入驻平台</h3>
        <el-button size="small" type="primary" @click="showPlatformDialog = true; platformForm = { platform_type: '', platform_name: '', blogger_name: '', profile: '', url: '', sort_order: 0 }">
          添加平台
        </el-button>
      </div>

      <el-table :data="platforms" stripe size="small">
        <el-table-column prop="platform_name" label="平台名称" />
        <el-table-column prop="platform_type" label="类型" width="120" />
        <el-table-column prop="blogger_name" label="博主名称" />
        <el-table-column label="操作" width="120">
          <template #default="{ row, $index }">
            <el-button size="small" type="danger" text @click="deletePlatform(row.id, $index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog v-model="showPlatformDialog" title="添加平台" width="500px">
        <el-form :model="platformForm" label-position="top">
          <el-row :gutter="16">
            <el-col :span="12">
              <el-form-item label="平台类型" required>
                <el-select v-model="platformForm.platform_type" style="width:100%">
                  <el-option label="抖音" value="douyin" />
                  <el-option label="小红书" value="xiaohongshu" />
                  <el-option label="微信视频号" value="wechat_video" />
                  <el-option label="B站" value="bilibili" />
                  <el-option label="知乎" value="zhihu" />
                  <el-option label="微博" value="weibo" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="平台名称" required>
                <el-input v-model="platformForm.platform_name" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="博主名称" required>
            <el-input v-model="platformForm.blogger_name" />
          </el-form-item>
          <el-form-item label="简介">
            <el-input v-model="platformForm.profile" type="textarea" :rows="2" />
          </el-form-item>
          <el-form-item label="链接">
            <el-input v-model="platformForm.url" placeholder="https://..." />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showPlatformDialog = false">取消</el-button>
          <el-button type="primary" :loading="savingPlatform" @click="handleAddPlatform">保存</el-button>
        </template>
      </el-dialog>

      <!-- ── 案例管理 ── -->
      <el-divider />
      <div class="section-header">
        <h3>代表案例</h3>
        <el-button size="small" type="primary" @click="showCaseDialog = true; caseForm = { name: '', summary: '', content: '', cover_image: '', sort_order: 0 }">
          添加案例
        </el-button>
      </div>

      <el-table :data="cases" stripe size="small">
        <el-table-column prop="name" label="案例名称" />
        <el-table-column prop="summary" label="摘要" show-overflow-tooltip />
        <el-table-column label="操作" width="120">
          <template #default="{ row, $index }">
            <el-button size="small" type="danger" text @click="deleteCase(row.id, $index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog v-model="showCaseDialog" title="添加案例" width="600px">
        <el-form :model="caseForm" label-position="top">
          <el-form-item label="案例名称" required>
            <el-input v-model="caseForm.name" />
          </el-form-item>
          <el-form-item label="摘要">
            <el-input v-model="caseForm.summary" type="textarea" :rows="2" />
          </el-form-item>
          <el-form-item label="内容（Markdown）">
            <el-input v-model="caseForm.content" type="textarea" :rows="6" />
          </el-form-item>
          <el-form-item label="封面图 URL">
            <el-input v-model="caseForm.cover_image" placeholder="https://..." />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showCaseDialog = false">取消</el-button>
          <el-button type="primary" :loading="savingCase" @click="handleAddCase">保存</el-button>
        </template>
      </el-dialog>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { adminApi } from '@/api/modules/admin'
import { experthubApi } from '@/api/modules/experthub'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const saving = ref(false)

const form = ref({
  name: '',
  title: '',
  summary: '',
  avatar_url: '',
  contact_email: '',
  contact_phone: '',
  contact_wechat: '',
  is_published: true,
})

// ── Platforms ──
const platforms = ref<any[]>([])
const showPlatformDialog = ref(false)
const savingPlatform = ref(false)
const platformForm = ref({ expert_id: 0, platform_type: '', platform_name: '', blogger_name: '', profile: '', url: '', sort_order: 0 })

// ── Cases ──
const cases = ref<any[]>([])
const showCaseDialog = ref(false)
const savingCase = ref(false)
const caseForm = ref({ expert_id: 0, name: '', summary: '', content: '', cover_image: '', sort_order: 0 })

const loadPlatforms = async () => {
  try {
    const res = await adminApi.getExpertPlatforms(Number(route.params.id))
    platforms.value = res.list || res
  } catch { platforms.value = [] }
}

const loadCases = async () => {
  try {
    const res = await adminApi.getExpertCases(Number(route.params.id))
    cases.value = res.list || res
  } catch { cases.value = [] }
}

const handleAddPlatform = async () => {
  savingPlatform.value = true
  try {
    platformForm.value.expert_id = Number(route.params.id)
    await adminApi.createPlatform(platformForm.value)
    ElMessage.success('平台添加成功')
    showPlatformDialog.value = false
    loadPlatforms()
  } catch { /* handled */ }
  finally { savingPlatform.value = false }
}

const deletePlatform = async (id: number, index: number) => {
  try {
    await adminApi.deletePlatform(id)
    platforms.value.splice(index, 1)
    ElMessage.success('已删除')
  } catch { /* handled */ }
}

const handleAddCase = async () => {
  savingCase.value = true
  try {
    caseForm.value.expert_id = Number(route.params.id)
    await adminApi.createCase(caseForm.value)
    ElMessage.success('案例添加成功')
    showCaseDialog.value = false
    loadCases()
  } catch { /* handled */ }
  finally { savingCase.value = false }
}

const deleteCase = async (id: number, index: number) => {
  try {
    await adminApi.deleteCase(id)
    cases.value.splice(index, 1)
    ElMessage.success('已删除')
  } catch { /* handled */ }
}

onMounted(async () => {
  if (isEdit.value) {
    try {
      const expert = await experthubApi.getExpert(Number(route.params.id))
      form.value = {
        name: expert.name,
        title: expert.title || '',
        summary: expert.summary,
        avatar_url: expert.avatar_url || '',
        contact_email: expert.contact_email || '',
        contact_phone: expert.contact_phone || '',
        contact_wechat: expert.contact_wechat || '',
        is_published: expert.is_published,
      }
      platforms.value = expert.platforms
      cases.value = expert.cases
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
      await adminApi.updateExpert(Number(route.params.id), data)
      ElMessage.success('更新成功')
    } else {
      await adminApi.createExpert(data)
      ElMessage.success('创建成功')
    }
    router.push('/admin/experts')
  } catch {
    // handled
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  margin: 0;
}
</style>
