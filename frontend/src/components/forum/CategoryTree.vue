<template>
  <div class="category-tree">
    <div
      v-for="cat in categories"
      :key="cat.id"
      class="category-item"
      :class="{ active: Number(route.params.id) === cat.id }"
      @click="handleClick(cat)"
    >
      <span class="category-name">{{ cat.name }}</span>
      <span v-if="cat.children?.length" class="expand-icon">
        <el-icon><ArrowRight /></el-icon>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import type { Category } from '@/api/types/models'

defineProps<{
  categories: Category[]
}>()

const route = useRoute()
const router = useRouter()

const handleClick = (cat: Category) => {
  router.push(`/forum/category/${cat.id}`)
}
</script>

<style scoped>
.category-tree {
  background: #fff;
  border-radius: 12px;
  padding: 12px;
  border: 1px solid #E8E2D8;
}

.category-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
}

.category-item:hover {
  background: rgba(27, 42, 74, 0.06);
}

.category-item.active {
  background: rgba(27, 42, 74, 0.06);
  color: #1B2A4A;
  font-weight: 600;
}

.category-name {
  font-size: 14px;
}

.expand-icon {
  display: flex;
  align-items: center;
}
</style>
