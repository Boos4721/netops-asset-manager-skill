<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api/client'
import { Rocket, Container, Cpu } from 'lucide-vue-next'

const loading = ref(false)
const result = ref('')

const deployOptions = [
  { type: 'docker', label: 'Docker Engine', desc: '安装 Docker 引擎及相关组件', icon: Container, color: 'text-blue-400', bg: 'bg-blue-500/10' },
  { type: 'vllm', label: 'vLLM', desc: '高性能 LLM 推理框架（需 GPU）', icon: Cpu, color: 'text-purple-400', bg: 'bg-purple-500/10' },
  { type: 'llama-cpp', label: 'llama.cpp', desc: 'CPU 本地推理引擎，编译安装', icon: Rocket, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
]

async function deploy(type: string) {
  if (!confirm(`确认部署 ${type}？此操作将在后台执行。`)) return
  loading.value = true
  result.value = ''
  try {
    const res = await api.post('/deploy/system', { type })
    result.value = res.data.message || '已启动'
  } catch(e: any) {
    result.value = '部署失败: ' + (e.response?.data?.message || e.message)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <p class="text-sm" style="color: var(--text-muted)">选择要部署的系统组件，部署任务将在后台通过 PM2 执行，可在「任务管理」页面查看进度。</p>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div v-for="opt in deployOptions" :key="opt.type" class="glass rounded-2xl p-6 card-hover flex flex-col gap-4">
        <div class="w-12 h-12 rounded-2xl flex items-center justify-center" :class="opt.bg">
          <component :is="opt.icon" class="w-6 h-6" :class="opt.color" />
        </div>
        <div>
          <h3 class="font-semibold text-sm mb-1" style="color: var(--text-main)">{{ opt.label }}</h3>
          <p class="text-xs" style="color: var(--text-muted)">{{ opt.desc }}</p>
        </div>
        <button
          @click="deploy(opt.type)"
          :disabled="loading"
          class="mt-auto w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium transition-colors disabled:opacity-50"
        >
          {{ loading ? '部署中…' : '立即部署' }}
        </button>
      </div>
    </div>

    <div v-if="result" class="glass rounded-2xl p-4">
      <p class="text-sm mono" style="color: var(--text-main)">{{ result }}</p>
    </div>
  </div>
</template>
