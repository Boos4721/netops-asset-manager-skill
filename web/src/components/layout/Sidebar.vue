<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  LayoutDashboard, Server, Network, Briefcase, Rocket,
  Brain, MessageSquare, Settings, ShieldCheck, LogOut
} from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const navItems = [
  { label: '控制台', path: '/dashboard', icon: LayoutDashboard },
  { label: '资产清单', path: '/inventory', icon: Server },
  { label: '拓扑图', path: '/topology', icon: Network },
  { label: '任务管理', path: '/jobs', icon: Briefcase },
  { label: '系统部署', path: '/deploy', icon: Rocket },
  { label: '模型管理', path: '/models', icon: Brain },
  { label: 'AI 助手', path: '/chat', icon: MessageSquare },
  { label: '系统设置', path: '/settings', icon: Settings },
]

function logout() {
  auth.logout()
  router.push('/login')
}

function isActive(path: string) {
  return route.path === path || route.path.startsWith(path + '/')
}
</script>

<template>
  <aside class="w-64 flex flex-col border-r glass" style="background: var(--sidebar-bg); border-color: var(--border);">
    <!-- Logo -->
    <div class="p-6 flex items-center gap-3">
      <div class="w-10 h-10 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/20 glow-blue">
        <ShieldCheck class="w-5 h-5 text-white" />
      </div>
      <div>
        <div class="font-bold text-sm" style="color: var(--text-main)">NetOps <span class="text-blue-500">Pro</span></div>
        <div class="text-xs" style="color: var(--text-muted)">网络资产管理</div>
      </div>
    </div>

    <!-- Nav -->
    <nav class="flex-1 px-4 space-y-0.5 overflow-y-auto">
      <button
        v-for="item in navItems"
        :key="item.path"
        @click="router.push(item.path)"
        class="sidebar-item w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium"
        :class="{ active: isActive(item.path) }"
      >
        <component :is="item.icon" class="w-4 h-4 flex-shrink-0" />
        {{ item.label }}
      </button>
    </nav>

    <!-- User info + logout -->
    <div class="p-4 border-t" style="border-color: var(--border)">
      <div class="flex items-center gap-3 px-2 py-1.5">
        <div class="w-8 h-8 rounded-xl bg-blue-600/20 flex items-center justify-center text-xs font-bold text-blue-400">
          {{ (auth.username || 'U')[0].toUpperCase() }}
        </div>
        <div class="flex-1 min-w-0">
          <div class="text-xs font-semibold truncate" style="color: var(--text-main)">{{ auth.username }}</div>
          <div class="text-[10px]" style="color: var(--text-muted)">{{ auth.role }}</div>
        </div>
        <button @click="logout" class="p-1.5 rounded-lg hover:bg-red-500/10 text-red-400 transition-colors">
          <LogOut class="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  </aside>
</template>
