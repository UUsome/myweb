<template>
  <header class="app-header">
    <div class="header-inner">
      <div class="logo">
        <router-link to="/">
          <span class="logo-text">win</span>
        </router-link>
      </div>

      <nav class="nav-links">
        <router-link to="/forum" class="nav-item">论坛</router-link>
        <!-- <router-link to="/experts" class="nav-item">专家库</router-link> -->
        <router-link to="/jobs" class="nav-item">人才集市</router-link>
      </nav>

      <div class="header-actions">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown trigger="click">
            <span class="user-info">
              <el-avatar :size="32" :src="userStore.userInfo?.avatar_url || undefined">
                {{ userStore.userInfo?.nickname?.charAt(0) || userStore.userInfo?.username.charAt(0) }}
              </el-avatar>
              <span class="username">{{ userStore.userInfo?.nickname || userStore.userInfo?.username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push('/admin')" v-if="userStore.isAdmin">
                  管理后台
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" size="small" @click="router.push('/login')">登录</el-button>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const handleLogout = async () => {
  await userStore.logout()
}
</script>

<style scoped>
.app-header {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #E8E2D8;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  color: #1B2A4A;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 8px;
  margin-left: 40px;
}

.nav-item {
  padding: 8px 16px;
  color: #4A4A4A;
  text-decoration: none;
  border-radius: 6px;
  font-size: 15px;
  transition: all 0.2s;
}

.nav-item:hover,
.nav-item.router-link-active {
  color: #1B2A4A;
  background: rgba(27, 42, 74, 0.06);
  text-decoration: none;
}

.header-actions {
  margin-left: auto;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  font-size: 14px;
  color: #2C2C2C;
}
</style>
