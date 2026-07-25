<template>
  <div class="forum-page page-container">
    <div class="forum-layout">
      <aside class="forum-sidebar">
        <h3 class="section-title">板块分类</h3>
        <CategoryTree :categories="forumStore.categories" />
      </aside>

      <main class="forum-main">
        <div class="forum-header">
          <h2>最新帖子</h2>
          <el-button v-if="userStore.isLoggedIn" type="primary" @click="showCreate = true">
            发帖
          </el-button>
        </div>

        <!-- Create Post Dialog -->
        <el-dialog v-model="showCreate" title="发布帖子" width="600px">
          <el-form :model="createForm" label-position="top">
            <el-form-item label="板块">
              <el-select v-model="createForm.category_id" placeholder="选择板块" style="width: 100%">
                <el-option
                  v-for="cat in forumStore.categories"
                  :key="cat.id"
                  :label="cat.name"
                  :value="cat.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="标题">
              <el-input v-model="createForm.title" placeholder="请输入标题" maxlength="200" />
            </el-form-item>
            <el-form-item label="内容">
              <el-input
                v-model="createForm.content"
                type="textarea"
                :rows="8"
                placeholder="请输入内容"
              />
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="showCreate = false">取消</el-button>
            <el-button type="primary" :loading="creating" @click="handleCreatePost">发布</el-button>
          </template>
        </el-dialog>

        <!-- Post List -->
        <PostCard v-for="post in pagination.items.value" :key="post.id" :post="post" />

        <div ref="sentinel" v-if="pagination.hasMore.value" class="loading-trigger">
          <el-icon v-if="pagination.loading.value" class="is-loading"><Loading /></el-icon>
        </div>

        <EmptyState
          v-if="pagination.initialized.value && !pagination.items.value.length"
          message="暂无帖子"
        />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { forumApi } from '@/api/modules/forum'
import { useForumStore } from '@/stores/forum'
import { useUserStore } from '@/stores/user'
import { usePagination } from '@/composables/usePagination'
import { useInfiniteScroll } from '@/composables/useInfiniteScroll'
import CategoryTree from '@/components/forum/CategoryTree.vue'
import PostCard from '@/components/forum/PostCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const forumStore = useForumStore()
const userStore = useUserStore()

const pagination = usePagination({
  fetchFn: (p) => forumApi.getPosts(p),
  initialParams: { limit: 20 },
})

const { sentinel } = useInfiniteScroll(pagination.loadMore, pagination.hasMore, pagination.loading)

const showCreate = ref(false)
const creating = ref(false)

const createForm = ref({
  title: '',
  content: '',
  category_id: null as number | null,
})

const handleCreatePost = async () => {
  if (!createForm.value.title || !createForm.value.content || !createForm.value.category_id) {
    ElMessage.warning('请填写完整信息')
    return
  }

  creating.value = true
  try {
    await forumApi.createPost({
      title: createForm.value.title,
      content: createForm.value.content,
      category_id: createForm.value.category_id,
    })
    ElMessage.success('发布成功')
    showCreate.value = false
    createForm.value = { title: '', content: '', category_id: null }
    pagination.refresh()
  } catch {
    // Error handled by interceptor
  } finally {
    creating.value = false
  }
}

onMounted(async () => {
  await Promise.all([
    forumStore.fetchCategories(),
    pagination.refresh(),
  ])
})
</script>

<style scoped>
.forum-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 24px;
}

.forum-sidebar {
  position: sticky;
  top: 80px;
  align-self: start;
}

.forum-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.forum-header h2 {
  margin: 0;
  font-size: 20px;
}

@media (max-width: 768px) {
  .forum-layout {
    grid-template-columns: 1fr;
  }

  .forum-sidebar {
    display: none;
  }
}
</style>
