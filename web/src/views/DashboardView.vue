<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useInventoryStore } from '@/stores/inventory'
import { useStatsStore } from '@/stores/stats'
import { Server, Wifi, WifiOff, AlertTriangle, Cpu } from 'lucide-vue-next'

const inv = useInventoryStore()
const statsStore = useStatsStore()

onMounted(async () => {
  await Promise.all([inv.fetchDevices(), statsStore.fetchStats()])
})

const stats = computed(() => statsStore.stats)

const recentDevices = computed(() => [...inv.devices].slice(0, 8))

const statCards = computed(() => [
  { label: '资产总数', value: stats.value.total, icon: Server, color: 'text-blue-400', bg: 'bg-blue-500/10' },
  { label: '在线设备', value: stats.value.online, icon: Wifi, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
  { label: '离线设备', value: stats.value.offline, icon: WifiOff, color: 'text-red-400', bg: 'bg-red-500/10' },
  { label: 'GPU 节点', value: stats.value.gpu_count, icon: Cpu, color: 'text-purple-400', bg: 'bg-purple-500/10' },
])
</script>

<template>
  <div class="space-y-6">
    <!-- Stat cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        v-for="card in statCards"
        :key="card.label"
        class="glass rounded-2xl p-5 card-hover"
      >
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-medium" style="color: var(--text-muted)">{{ card.label }}</span>
          <div class="w-8 h-8 rounded-xl flex items-center justify-center" :class="card.bg">
            <component :is="card.icon" class="w-4 h-4" :class="card.color" />
          </div>
        </div>
        <div class="text-3xl font-bold mono" style="color: var(--text-main)">{{ card.value }}</div>
      </div>
    </div>

    <!-- Recent devices table -->
    <div class="glass rounded-2xl p-6">
      <h2 class="font-semibold text-sm mb-4" style="color: var(--text-main)">最近资产</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr style="color: var(--text-muted)">
              <th class="text-left pb-3 font-medium text-xs uppercase tracking-wider">IP</th>
              <th class="text-left pb-3 font-medium text-xs uppercase tracking-wider">名称</th>
              <th class="text-left pb-3 font-medium text-xs uppercase tracking-wider">厂商</th>
              <th class="text-left pb-3 font-medium text-xs uppercase tracking-wider">位置</th>
              <th class="text-left pb-3 font-medium text-xs uppercase tracking-wider">状态</th>
            </tr>
          </thead>
          <tbody class="divide-y" style="divide-color: var(--border)">
            <tr v-for="d in recentDevices" :key="d.ip" class="hover:bg-white/2 transition-colors">
              <td class="py-3 mono text-xs text-blue-400">{{ d.ip }}</td>
              <td class="py-3 text-xs" style="color: var(--text-main)">{{ d.name || '—' }}</td>
              <td class="py-3 text-xs" style="color: var(--text-muted)">{{ d.vendor || '—' }}</td>
              <td class="py-3 text-xs" style="color: var(--text-muted)">{{ d.location || '—' }}</td>
              <td class="py-3">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold" :class="`status-${d.status}`">{{ d.status }}</span>
              </td>
            </tr>
            <tr v-if="recentDevices.length === 0">
              <td colspan="5" class="py-8 text-center text-xs" style="color: var(--text-muted)">暂无设备数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
