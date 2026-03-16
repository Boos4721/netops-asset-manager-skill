<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { Sun, Moon, Monitor, Bell } from 'lucide-vue-next'

const route = useRoute()
const theme = useThemeStore()

const titles: Record<string, string> = {
  '/dashboard': '控制台',
  '/inventory': '资产清单',
  '/topology': '拓扑图',
  '/jobs': '任务管理',
  '/deploy': '系统部署',
  '/models': '模型管理',
  '/chat': 'AI 助手',
  '/settings': '系统设置',
}

function currentTitle() {
  return titles[route.path] || 'NetOps Pro'
}

function cycleTheme() {
  const order: Array<'dark' | 'light' | 'auto'> = ['dark', 'light', 'auto']
  const idx = order.indexOf(theme.preference)
  theme.set(order[(idx + 1) % order.length])
}
</script>

<template>
  <header class="h-14 flex items-center justify-between px-6 border-b" style="border-color: var(--border); background: var(--card-bg);">
    <h1 class="font-semibold text-sm" style="color: var(--text-main)">{{ currentTitle() }}</h1>
    <div class="flex items-center gap-2">
      <button @click="cycleTheme" class="p-2 rounded-xl hover:bg-blue-500/10 transition-colors" style="color: var(--text-muted)">
        <Sun v-if="theme.preference === 'light'" class="w-4 h-4" />
        <Moon v-else-if="theme.preference === 'dark'" class="w-4 h-4" />
        <Monitor v-else class="w-4 h-4" />
      </button>
      <button class="p-2 rounded-xl hover:bg-blue-500/10 transition-colors" style="color: var(--text-muted)">
        <Bell class="w-4 h-4" />
      </button>
    </div>
  </header>
</template>
