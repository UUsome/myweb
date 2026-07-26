<template>
  <div class="home-page page-container">
    <section class="hero">
      <h1>欢迎来到 win</h1>
      <p>连接专家与机会的知识社区</p>
      <div class="hero-actions">
        <el-button type="primary" size="large" @click="router.push('/experts')">
          浏览专家
        </el-button>
        <el-button size="large" @click="router.push('/jobs')">
          查看职位
        </el-button>
      </div>
    </section>

    <section class="features">
      <div class="feature-card" @click="router.push('/forum')">
        <el-icon :size="36" color="#1B2A4A"><ChatDotSquare /></el-icon>
        <h3>技术论坛</h3>
        <p>交流技术、分享经验</p>
      </div>
      <div class="feature-card" @click="router.push('/experts')">
        <el-icon :size="36" color="#C4973E"><Trophy /></el-icon>
        <h3>专家库</h3>
        <p>发现行业顶尖专家</p>
      </div>
      <div class="feature-card" @click="router.push('/jobs')">
        <el-icon :size="36" color="#C26B6B"><Briefcase /></el-icon>
        <h3>人才集市</h3>
        <p>优质岗位等你来</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 80px 20px;
}

.hero h1 {
  font-size: 36px;
  margin: 0 0 12px;
}

.hero p {
  font-size: 18px;
  color: #888880;
  margin-bottom: 32px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding: 40px 0;
}

.feature-card {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: all 0.3s;
  border: 1px solid #E8E2D8;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.feature-card h3 {
  margin: 16px 0 8px;
  font-size: 18px;
}
</style>
