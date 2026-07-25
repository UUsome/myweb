<template>
  <div class="admin-dashboard">
    <h2>仪表盘</h2>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ userStore.userInfo?.username }}</div>
        <div class="stat-label">欢迎回来</div>
      </div>

      <div class="stat-card" @click="router.push('/admin/users')">
        <div class="stat-icon"><el-icon :size="32"><User /></el-icon></div>
        <div class="stat-label">用户管理</div>
      </div>

      <div class="stat-card" @click="router.push('/admin/experts')">
        <div class="stat-icon"><el-icon :size="32"><Trophy /></el-icon></div>
        <div class="stat-label">专家管理</div>
      </div>

      <div class="stat-card" @click="router.push('/admin/jobs')">
        <div class="stat-icon"><el-icon :size="32"><Briefcase /></el-icon></div>
        <div class="stat-label">职位管理</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition: transform 0.2s;
  border: 1px solid #E8E2D8;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1B2A4A;
}

.stat-label {
  margin-top: 8px;
  color: #888880;
  font-size: 14px;
}

.stat-icon {
  margin-bottom: 12px;
  color: #1B2A4A;
}
</style>
