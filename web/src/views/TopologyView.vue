<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
// @ts-ignore
import { Network, DataSet } from 'vis-network/standalone'
import api from '@/api/client'
import { useInventoryStore } from '@/stores/inventory'
import { useAuthStore } from '@/stores/auth'
import { Plus, Trash2 } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'

const inv = useInventoryStore()
const auth = useAuthStore()
const theme = useThemeStore()

const container = ref<HTMLElement>()
let network: Network | null = null

const links = ref<any[]>([])
const newLink = ref({ source_ip: '', target_ip: '', label: '' })

onMounted(async () => {
  await inv.fetchDevices()
  await fetchLinks()
  renderNetwork()
})

onUnmounted(() => network?.destroy())

async function fetchLinks() {
  const res = await api.get('/topology/links')
  links.value = res.data
}

async function addLink() {
  if (!newLink.value.source_ip || !newLink.value.target_ip) return
  await api.post('/topology/links', newLink.value)
  newLink.value = { source_ip: '', target_ip: '', label: '' }
  await fetchLinks()
  renderNetwork()
}

async function deleteLink(id: number) {
  await api.delete(`/topology/links/${id}`)
  await fetchLinks()
  renderNetwork()
}

function renderNetwork() {
  if (!container.value) return
  network?.destroy()

  const isDark = theme.current === 'dark'
  const nodeColor = isDark ? '#1e293b' : '#e2e8f0'
  const fontColor = isDark ? '#f1f5f9' : '#0f172a'
  const edgeColor = isDark ? '#3b82f6' : '#2563eb'

  const nodeSet = new Set<string>()
  links.value.forEach(l => { nodeSet.add(l.source_ip); nodeSet.add(l.target_ip) })
  inv.devices.forEach(d => nodeSet.add(d.ip))

  const nodes = new DataSet(
    [...nodeSet].map(ip => {
      const d = inv.devices.find(x => x.ip === ip)
      return {
        id: ip,
        label: d ? `${d.name || ip}\n${ip}` : ip,
        color: {
          background: d?.status === 'online' ? (isDark ? '#064e3b' : '#d1fae5') : nodeColor,
          border: d?.status === 'online' ? '#10b981' : (isDark ? '#334155' : '#94a3b8'),
        },
        font: { color: fontColor, size: 11 },
        shape: 'box',
        margin: { top: 8, bottom: 8, left: 10, right: 10 },
        borderWidth: 1.5,
        borderWidthSelected: 3,
      }
    })
  )

  const edges = new DataSet(
    links.value.map(l => ({
      id: l.id,
      from: l.source_ip,
      to: l.target_ip,
      label: l.label || '',
      color: { color: edgeColor, opacity: 0.7 },
      font: { color: fontColor, size: 10 },
      smooth: { type: 'curvedCW', roundness: 0.2 },
    }))
  )

  network = new Network(container.value, { nodes, edges }, {
    physics: { enabled: true, stabilization: { iterations: 100 } },
    interaction: { hover: true, zoomView: true },
    layout: { improvedLayout: true },
  })
}
</script>

<template>
  <div class="space-y-4">
    <!-- Add link form -->
    <div v-if="auth.isOperator()" class="glass rounded-2xl p-4 flex items-center gap-3 flex-wrap">
      <select v-model="newLink.source_ip" class="flex-1 min-w-32 px-3 py-2 rounded-xl border text-sm outline-none" style="background: var(--card-bg); border-color: var(--border); color: var(--text-main)">
        <option value="">源节点</option>
        <option v-for="d in inv.devices" :key="d.ip" :value="d.ip">{{ d.ip }} {{ d.name ? '— ' + d.name : '' }}</option>
      </select>
      <span style="color: var(--text-muted)" class="text-sm">→</span>
      <select v-model="newLink.target_ip" class="flex-1 min-w-32 px-3 py-2 rounded-xl border text-sm outline-none" style="background: var(--card-bg); border-color: var(--border); color: var(--text-main)">
        <option value="">目标节点</option>
        <option v-for="d in inv.devices" :key="d.ip" :value="d.ip">{{ d.ip }} {{ d.name ? '— ' + d.name : '' }}</option>
      </select>
      <input v-model="newLink.label" placeholder="标签(可选)" class="w-32 px-3 py-2 rounded-xl border text-sm outline-none" style="background: var(--card-bg); border-color: var(--border); color: var(--text-main)" />
      <button @click="addLink" class="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium">
        <Plus class="w-4 h-4" /> 添加连接
      </button>
    </div>

    <!-- Network canvas -->
    <div class="glass rounded-2xl overflow-hidden">
      <div ref="container" class="w-full" style="height: 520px; background: var(--item-hover)"></div>
    </div>

    <!-- Links list -->
    <div class="glass rounded-2xl p-4">
      <h3 class="text-sm font-semibold mb-3" style="color: var(--text-main)">连接列表 ({{ links.length }})</h3>
      <div class="space-y-2">
        <div v-for="l in links" :key="l.id" class="flex items-center justify-between text-xs py-1.5 px-2 rounded-lg hover:bg-white/2">
          <span class="mono" style="color: var(--text-main)">{{ l.source_ip }} <span class="text-blue-400">→</span> {{ l.target_ip }}</span>
          <div class="flex items-center gap-2">
            <span v-if="l.label" style="color: var(--text-muted)">{{ l.label }}</span>
            <button v-if="auth.isOperator()" @click="deleteLink(l.id)" class="p-1 rounded hover:bg-red-500/10 text-red-400">
              <Trash2 class="w-3 h-3" />
            </button>
          </div>
        </div>
        <p v-if="links.length === 0" class="text-xs text-center py-4" style="color: var(--text-muted)">暂无连接</p>
      </div>
    </div>
  </div>
</template>
