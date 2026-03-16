<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { RefreshCw, RotateCcw, Square, Trash2, FileText } from 'lucide-vue-next'

const auth = useAuthStore()
const tasks = ref<any[]>([])
const loading = ref(false)
const logModal = ref(false)
const logContent = ref('')
const logTarget = ref('')

onMounted(fetchTasks)

async function fetchTasks() {
  loading.value = true
  try {
    const res = await api.get('/pm2/status')
    tasks.value = res.data
  } finally {
    loading.value = false
  }
}

async function pm2Action(action: string, name: string) {
  await api.post(`/pm2/${action}/${name}`)
  await fetchTasks()
}

async function viewLogs(name: string) {
  logTarget.value = name
  const res = await api.get(`/pm2/logs/${name}`)
  logContent.value = res.data.logs || ''
  logModal.value = true
}

function statusColor(s: string) {
  if (s === 'online') return 'status-online'
  if (s === 'stopped') return 'status-offline'
  return 'status-unknown'
}
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h2 class="text-sm font-semibold" style="color: var(--text-main)">PM2 进程列表</h2>
      <button @click="fetchTasks" class="flex items-center gap-2 px-3 py-2 rounded-xl border text-sm" style="border-color: var(--border); color: var(--text-muted)">
        <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loading }" /> 刷新
      </button>
    </div>

    <div class="glass rounded-2xl overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr style="border-bottom: 1px solid var(--border)">
            <th v-for="h in ['进程名', '状态', '重启次数', 'CPU', '内存', '操作']" :key="h"
              class="text-left px-4 py-3 text-[11px] font-semibold uppercase tracking-wider"
              style="color: var(--text-muted)">{{ h }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in tasks" :key="t.name" class="border-b transition-colors hover:bg-white/2" style="border-color: var(--border)">
            <td class="px-4 py-3 mono text-xs font-medium" style="color: var(--text-main)">{{ t.name }}</td>
            <td class="px-4 py-3">
              <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold" :class="statusColor(t.status)">{{ t.status }}</span>
            </td>
            <td class="px-4 py-3 text-xs mono" style="color: var(--text-muted)">{{ t.restarts ?? '—' }}</td>
            <td class="px-4 py-3 text-xs mono" style="color: var(--text-muted)">{{ t.cpu != null ? t.cpu + '%' : '—' }}</td>
            <td class="px-4 py-3 text-xs mono" style="color: var(--text-muted)">
              {{ t.memory != null ? (t.memory / 1024 / 1024).toFixed(1) + ' MB' : '—' }}
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center gap-1">
                <button @click="viewLogs(t.name)" class="p-1.5 rounded-lg hover:bg-blue-500/10 text-blue-400 transition-colors" title="日志">
                  <FileText class="w-3.5 h-3.5" />
                </button>
                <template v-if="auth.isOperator()">
                  <button @click="pm2Action('restart', t.name)" class="p-1.5 rounded-lg hover:bg-emerald-500/10 text-emerald-400 transition-colors" title="重启">
                    <RotateCcw class="w-3.5 h-3.5" />
                  </button>
                  <button @click="pm2Action('stop', t.name)" class="p-1.5 rounded-lg hover:bg-yellow-500/10 text-yellow-400 transition-colors" title="停止">
                    <Square class="w-3.5 h-3.5" />
                  </button>
                </template>
                <button v-if="auth.isRoot()" @click="pm2Action('delete', t.name)" class="p-1.5 rounded-lg hover:bg-red-500/10 text-red-400 transition-colors" title="删除">
                  <Trash2 class="w-3.5 h-3.5" />
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="tasks.length === 0">
            <td colspan="6" class="px-4 py-12 text-center text-sm" style="color: var(--text-muted)">
              {{ loading ? '加载中…' : '暂无 PM2 进程' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Log Modal -->
    <Teleport to="body">
      <div v-if="logModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" @click.self="logModal = false">
        <div class="glass rounded-2xl w-full max-w-3xl max-h-[80vh] flex flex-col">
          <div class="flex items-center justify-between px-6 py-4 border-b" style="border-color: var(--border)">
            <span class="text-sm font-semibold mono" style="color: var(--text-main)">{{ logTarget }} — 日志</span>
            <button @click="logModal = false" class="text-xs px-3 py-1.5 rounded-lg border" style="border-color: var(--border); color: var(--text-muted)">关闭</button>
          </div>
          <pre class="overflow-auto p-6 text-xs mono flex-1" style="color: var(--text-main); white-space: pre-wrap">{{ logContent || '暂无日志' }}</pre>
        </div>
      </div>
    </Teleport>
  </div>
</template>
