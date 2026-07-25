<template>
  <div class="expert-detail-page page-container">
    <div class="back-link">
      <el-button text @click="router.back()">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>
    </div>

    <LoadingSpinner v-if="loading" />

    <div v-else-if="expert" class="expert-detail">
      <div class="expert-header card">
        <div class="header-left">
          <el-avatar :size="80" :src="expert.avatar_url || undefined">
            {{ expert.name.charAt(0) }}
          </el-avatar>
          <div class="header-info">
            <h1>{{ expert.name }}</h1>
            <p class="title">{{ expert.title || '专家' }}</p>
            <div class="tags">
              <el-tag v-for="tag in expert.tags" :key="tag.id" type="primary" effect="plain">
                {{ tag.name }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>

      <div class="expert-summary card">
        <h3>核心简介</h3>
        <p>{{ expert.summary }}</p>
      </div>

      <div class="expert-body">
        <div class="expert-section card">
          <h3>入驻平台 ({{ expert.platforms.length }})</h3>
          <PlatformList :platforms="expert.platforms" />
          <EmptyState v-if="!expert.platforms.length" message="暂无平台信息" />
        </div>

        <div class="expert-section card">
          <h3>代表案例 ({{ expert.cases.length }})</h3>
          <div v-for="c in expert.cases" :key="c.id" class="case-item" @click="router.push(`/expert-hub/case/${c.id}`)">
            <h4>{{ c.name }}</h4>
            <p v-if="c.summary">{{ c.summary }}</p>
          </div>
          <EmptyState v-if="!expert.cases.length" message="暂无案例信息" />
        </div>
      </div>

      <!-- Interactions -->
      <div class="expert-interactions card">
        <LikeButton target-type="expert" :target-id="expert.id" />
        <CommentSection target-type="expert" :target-id="expert.id" />
      </div>
    </div>

    <div v-else>
      <EmptyState message="专家不存在" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { experthubApi } from '@/api/modules/experthub'
import type { ExpertDetail } from '@/api/types/models'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import PlatformList from '@/components/experthub/PlatformList.vue'
import LikeButton from '@/components/interactions/LikeButton.vue'
import CommentSection from '@/components/interactions/CommentSection.vue'

const route = useRoute()
const router = useRouter()

const expert = ref<ExpertDetail | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    expert.value = await experthubApi.getExpert(Number(route.params.id))
  } catch {
    expert.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.back-link {
  margin-bottom: 16px;
}

.expert-header {
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.header-info h1 {
  margin: 0 0 4px;
  font-size: 24px;
}

.header-info .title {
  color: #888880;
  margin: 0 0 8px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.expert-summary {
  margin-bottom: 20px;
}

.expert-summary h3 {
  margin-top: 0;
}

.expert-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.expert-section h3 {
  margin-top: 0;
  padding-bottom: 12px;
  border-bottom: 1px solid #E8E2D8;
}

.case-item {
  padding: 12px 0;
  border-bottom: 1px solid #E8E2D8;
  cursor: pointer;
}

.case-item:last-child {
  border-bottom: none;
}

.case-item h4 {
  margin: 0 0 4px;
  color: #2C406E;
}

.case-item p {
  margin: 0;
  font-size: 13px;
  color: #4A4A4A;
}

.expert-interactions {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .expert-body {
    grid-template-columns: 1fr;
  }
}
</style>
