<template>
  <div class="comment-section">
    <h3 class="section-title">评论</h3>

    <!-- Comment Form -->
    <div v-if="userStore.isLoggedIn" class="comment-form">
      <el-input
        v-model="newComment"
        type="textarea"
        :rows="3"
        placeholder="写下你的评论..."
        maxlength="5000"
        show-word-limit
      />
      <div class="form-actions">
        <el-button type="primary" size="small" :loading="submitting" @click="handleSubmit">
          发表评论
        </el-button>
      </div>
    </div>

    <!-- Comments Tree -->
    <div class="comments-tree">
      <div v-for="comment in comments" :key="comment.id" class="comment-item" :style="{ marginLeft: comment.depth * 24 + 'px' }">
        <div class="comment-header">
          <el-avatar :size="24">{{ comment.nickname?.charAt(0) || comment.username.charAt(0) }}</el-avatar>
          <span class="comment-author">{{ comment.nickname || comment.username }}</span>
          <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
        </div>
        <div class="comment-content">{{ comment.content }}</div>
        <div class="comment-actions">
        <!-- <el-button text size="small" @click="startReply(comment)">回复</el-button> -->
          <el-button
            v-if="comment.user_id === userStore.userInfo?.id || userStore.isAdmin"
            text
            size="small"
            type="danger"
            @click="handleDelete(comment.id)"
          >
            删除
          </el-button>
        </div>

        <!-- Reply Form -->
<!-- 
        <div v-if="replyTo === comment.id" class="reply-form">
          <el-input v-model="replyContent" :rows="2" type="textarea" placeholder="回复..." />
          <div class="form-actions">
            <el-button size="small" @click="cancelReply">取消</el-button>
            <el-button size="small" type="primary" :loading="submitting" @click="handleReply(comment.id)">
              回复
            </el-button>
          </div>
        </div>
-->

        <!-- Nested Children -->
<!--
        <CommentItem
          v-for="child in comment.children"
          :key="child.id"
          :comment="child"
          :depth="comment.depth + 1"
        />
-->


      </div>
    </div>

    <EmptyState v-if="!comments.length && !loading" message="暂无评论" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { interactionsApi } from '@/api/modules/interactions'
import { useUserStore } from '@/stores/user'
import { formatDate } from '@/utils/format'
import EmptyState from '@/components/common/EmptyState.vue'

const props = defineProps<{
  targetType: string
  targetId: number
}>()

const userStore = useUserStore()
const comments = ref<any[]>([])
const loading = ref(false)
const submitting = ref(false)
const newComment = ref('')
const replyTo = ref<number | null>(null)
const replyContent = ref('')

const fetchComments = async () => {
  loading.value = true
  try {
    comments.value = await interactionsApi.getComments(props.targetType, props.targetId)
  } catch {
    comments.value = []
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  submitting.value = true
  try {
    await interactionsApi.createComment(props.targetType, props.targetId, newComment.value)
    ElMessage.success('评论成功')
    newComment.value = ''
    await fetchComments()
  } catch {
    // handled
  } finally {
    submitting.value = false
  }
}

const startReply = (comment: any) => {
  replyTo.value = comment.id
  replyContent.value = ''
}

const cancelReply = () => {
  replyTo.value = null
  replyContent.value = ''
}

const handleReply = async (parentId: number) => {
  if (!replyContent.value.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }
  submitting.value = true
  try {
    await interactionsApi.createComment(props.targetType, props.targetId, replyContent.value, parentId)
    ElMessage.success('回复成功')
    replyContent.value = ''
    replyTo.value = null
    await fetchComments()
  } catch {
    // handled
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (commentId: number) => {
  try {
    await interactionsApi.deleteComment(commentId)
    ElMessage.success('删除成功')
    await fetchComments()
  } catch {
    // handled
  }
}

onMounted(fetchComments)
</script>

<style scoped>
.comment-section {
  margin-top: 24px;
}

.comment-form {
  margin-bottom: 24px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}

.comment-item {
  padding: 12px 0;
  border-bottom: 1px solid #E8E2D8;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.comment-author {
  font-size: 14px;
  font-weight: 500;
}

.comment-time {
  font-size: 12px;
  color: #888880;
}

.comment-content {
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 6px;
}

.comment-actions {
  display: flex;
  gap: 8px;
}

.reply-form {
  margin-top: 8px;
  padding-left: 32px;
}
</style>
