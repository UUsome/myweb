<template>
  <div class="admin-layout">
    <!-- Admin Sidebar -->
    <aside class="admin-sidebar" :class="{ collapsed: appStore.sidebarCollapsed }">
      <div class="sidebar-header">
        <router-link to="/admin" class="sidebar-logo">
          <span v-if="!appStore.sidebarCollapsed">MyWeb 管理</span>
          <span v-else>M</span>
        </router-link>
      </div>

      <el-menu
        :default-active="route.path"
        :collapse="appStore.sidebarCollapsed"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/admin">
          <el-icon><DataAnalysis /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>

        <el-sub-menu index="users">
          <template #title>
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </template>
          <el-menu-item index="/admin/users">用户列表</el-menu-item>
          <el-menu-item index="/admin/users/create">创建用户</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="experts">
          <template #title>
            <el-icon><Trophy /></el-icon>
            <span>专家管理</span>
          </template>
          <el-menu-item index="/admin/experts">专家列表</el-menu-item>
          <el-menu-item index="/admin/experts/create">创建专家</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="jobs">
          <template #title>
            <el-icon><Briefcase /></el-icon>
            <span>职位管理</span>
          </template>
          <el-menu-item index="/admin/jobs">职位列表</el-menu-item>
          <el-menu-item index="/admin/jobs/create">创建职位</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="forum">
          <template #title>
            <el-icon><ChatDotSquare /></el-icon>
            <span>论坛管理</span>
          </template>
          <el-menu-item index="/admin/posts">帖子管理</el-menu-item>
          <el-menu-item index="/admin/categories">板块管理</el-menu-item>
        </el-sub-menu>
      </el-menu>

      <div class="sidebar-footer">
        <el-button text @click="appStore.toggleSidebar">
          <el-icon><Fold v-if="!appStore.sidebarCollapsed" /><Expand v-else /></el-icon>
        </el-button>
        <el-button text @click="router.push('/')">
          <el-icon><HomeFilled /></el-icon>
          <span v-if="!appStore.sidebarCollapsed">返回前台</span>
        </el-button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="admin-main" :class="{ collapsed: appStore.sidebarCollapsed }">
      <header class="admin-header">
        <h2>{{ route.meta?.title || '管理后台' }}</h2>
        <div class="admin-user">
          <span>{{ userStore.userInfo?.nickname || userStore.userInfo?.username }}</span>
          <el-button text @click="handleLogout">退出</el-button>
        </div>
      </header>
      <main class="admin-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

const handleLogout = async () => {
  await userStore.logout()
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.admin-sidebar {
  width: 240px;
  background: #1B2A4A;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 10;
}

.admin-sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-logo {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  text-decoration: none;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
  background: transparent;
}

.sidebar-menu .el-menu-item,
.sidebar-menu .el-sub-menu__title {
  color: #bfcbd9 !important;
}

.sidebar-menu .el-menu-item.is-active {
  color: #D8B05E !important;
  background: rgba(216, 176, 94, 0.12) !important;
}

.sidebar-footer {
  padding: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sidebar-footer .el-button {
  color: #bfcbd9;
  justify-content: flex-start;
}

.admin-main {
  flex: 1;
  margin-left: 240px;
  transition: margin-left 0.3s;
}

.admin-main.collapsed {
  margin-left: 64px;
}

.admin-header {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #E8E2D8;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 5;
}

.admin-header h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.admin-user {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
}

.admin-content {
  padding: 24px;
}
</style>
