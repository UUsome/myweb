<template>
  <div class="job-filter filter-bar">
    <el-input
      v-model="localFilters.keyword"
      placeholder="搜索职位/公司"
      clearable
      style="width: 200px"
      @input="emitChange"
    />

    <el-select v-model="localFilters.city" placeholder="城市" clearable style="width: 140px" @change="emitChange">
      <el-option v-for="city in options.cities" :key="city" :label="city" :value="city" />
    </el-select>

    <el-select v-model="localFilters.industry" placeholder="行业" clearable style="width: 140px" @change="emitChange">
      <el-option v-for="ind in options.industries" :key="ind" :label="ind" :value="ind" />
    </el-select>

    <el-select v-model="localFilters.job_type" placeholder="类型" clearable style="width: 120px" @change="emitChange">
      <el-option v-for="t in options.job_types" :key="t" :label="t" :value="t" />
    </el-select>

    <el-select v-model="localFilters.tag_type" placeholder="标签" clearable style="width: 120px" @change="emitChange">
      <el-option label="内推" value="internal" />
      <el-option label="急招" value="urgent" />
      <el-option label="专家推荐" value="expert" />
    </el-select>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { JobFilterOptions } from '@/api/types/models'

const props = defineProps<{
  options: JobFilterOptions
}>()

const emit = defineEmits<{
  change: [filters: typeof localFilters]
}>()

const localFilters = reactive({
  keyword: '',
  city: '',
  industry: '',
  job_type: '',
  tag_type: '',
})

const emitChange = () => {
  emit('change', { ...localFilters })
}

// Reset filters when options change
watch(() => props.options, () => {}, { deep: true })
</script>
