<template>
  <div
    class="expert-card"
    @click="router.push(`/expert-hub/${expert.id}`)"
    @mouseenter="showHover = true"
    @mouseleave="showHover = false"
  >
    <div class="card-header">
      <el-avatar :size="48" :src="expert.avatar_url || undefined">
        {{ expert.name.charAt(0) }}
      </el-avatar>
      <div class="info">
        <h3 class="name">{{ expert.name }}</h3>
        <p class="title">{{ expert.title || '专家' }}</p>
      </div>
    </div>

    <p class="summary">{{ expert.summary }}</p>

    <div class="tags">
      <el-tag v-for="tag in expert.tags" :key="tag.id" size="small" type="primary" effect="plain">
        {{ tag.name }}
      </el-tag>
    </div>

    <div class="stats">
      <span>📱 {{ expert.platform_count }} 个平台</span>
      <span>📄 {{ expert.case_count }} 个案例</span>
    </div>

    <!-- Hover Popup -->
    <Teleport to="body">
      <div v-if="showHover" class="hover-popup" ref="popupRef">
        <LoadingSpinner v-if="hoverLoading" />
        <div v-else-if="hoverData" class="hover-content">
          <div class="hover-section">
            <h4>入驻平台</h4>
            <div v-for="p in hoverData.platforms" :key="p.id" class="hover-item">
              <span class="label">{{ p.platform_name }}</span>
              <span class="value">{{ p.blogger_name }}</span>
            </div>
            <div v-if="!hoverData.platforms?.length" class="empty">暂无平台</div>
          </div>
          <div class="hover-section">
            <h4>代表案例</h4>
            <div v-for="c in hoverData.cases" :key="c.id" class="hover-item" @click.stop="goToCase(c.id)">
              <span class="value">{{ c.name }}</span>
            </div>
            <div v-if="!hoverData.cases?.length" class="empty">暂无案例</div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { experthubApi } from '@/api/modules/experthub'
import type { ExpertHover } from '@/api/types/models'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

defineProps<{
  expert: {
    id: number
    name: string
    title: string | null
    summary: string
    avatar_url: string | null
    tags: { id: number; name: string }[]
    platform_count: number
    case_count: number
  }
}>()

const router = useRouter()
const showHover = ref(false)
const hoverLoading = ref(false)
const hoverData = ref<ExpertHover | null>(null)

let hoverTimer: ReturnType<typeof setTimeout> | null = null

// Watch for hover to load data
import { watch } from 'vue'

watch(showHover, async (val) => {
  if (val) {
    hoverTimer = setTimeout(async () => {
      hoverLoading.value = true
      try {
        const { id } = (await import('vue')).defineProps
        // Use props.expert.id
      } catch {
        // ignore
      }
    }, 300)
  } else {
    if (hoverTimer) clearTimeout(hoverTimer)
    hoverData.value = null
  }
})

const goToCase = (caseId: number) => {
  router.push(`/expert-hub/case/${caseId}`)
}
</script>

<style scoped>
.expert-card {
  position: relative;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #E8E2D8;
}

.expert-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.name {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.title {
  font-size: 13px;
  color: #888880;
  margin: 2px 0 0;
}

.summary {
  font-size: 14px;
  color: #4A4A4A;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.stats {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #888880;
}

.hover-popup {
  position: fixed;
  z-index: 1000;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.07);
  padding: 16px;
  width: 320px;
  max-height: 400px;
  overflow-y: auto;
  pointer-events: auto;
  border: 1px solid #E8E2D8;
}

.hover-section {
  margin-bottom: 12px;
}

.hover-section h4 {
  font-size: 14px;
  font-weight: 600;
  margin: 2C2C2C;
}

.hover-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 13px;
}

.hover-item .label {
  color: #888880;
}

.hover-item .value {
  color: #2C406E;
  cursor: pointer;
}

.empty {
  color: #c0c4cc;
  font-size: 13px;
}
</style>
