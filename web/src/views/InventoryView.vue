<script setup lang="ts">
import { ref, computed, onMounted, h, defineComponent } from 'vue'
import { useInventoryStore, type Device } from '@/stores/inventory'
import { useAuthStore } from '@/stores/auth'
import Modal from '@/components/ui/Modal.vue'
import { Plus, Search, Upload, RefreshCw, Power, HardDrive, Pencil, Trash2, Eye } from 'lucide-vue-next'
import api from '@/api/client'

const inv = useInventoryStore()
const auth = useAuthStore()
onMounted(() => inv.fetchDevices())

const search = ref('')
const showAddModal = ref(false)
const showEditModal = ref(false)
const showDetailModal = ref(false)
const showImportModal = ref(false)
const selectedDevice = ref<Device | null>(null)
const actionMsg = ref('')
const actionLoading = ref(false)

type FormModel = {
  ip: string; name: string; vendor: string; model: string; location: string
  sn: string; server: string; ssh_user: string; ssh_pass: string; tags: string; gpu: boolean
}

const form = ref<FormModel>({
  ip: '', name: '', vendor: '', model: '', location: '',
  sn: '', server: '', ssh_user: 'root', ssh_pass: '', tags: '', gpu: false
})

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  if (!q) return inv.devices
  return inv.devices.filter((d: Device) =>
    d.ip.includes(q) || d.name.toLowerCase().includes(q) ||
    d.vendor.toLowerCase().includes(q) || d.location.toLowerCase().includes(q)
  )
})

function resetForm() {
  form.value = { ip: '', name: '', vendor: '', model: '', location: '', sn: '', server: '', ssh_user: 'root', ssh_pass: '', tags: '', gpu: false }
}

async function submitAdd() {
  actionLoading.value = true
  actionMsg.value = ''
  const tags = form.value.tags ? form.value.tags.split(',').map((t: string) => t.trim()).filter(Boolean) : []
  const res = await inv.addDevice({ ...form.value, tags })
  actionLoading.value = false
  if (res.status === 'success') { showAddModal.value = false; resetForm() }
  else actionMsg.value = res.message
}

function openEdit(d: Device) {
  selectedDevice.value = d
  form.value = {
    ip: d.ip, name: d.name, vendor: d.vendor, model: d.model,
    location: d.location, sn: d.sn, server: d.server,
    ssh_user: d.ssh_user || 'root', ssh_pass: '', tags: (d.tags || []).join(', '), gpu: d.gpu
  }
  showEditModal.value = true
}

async function submitEdit() {
  if (!selectedDevice.value) return
  actionLoading.value = true
  const tags = form.value.tags ? form.value.tags.split(',').map((t: string) => t.trim()).filter(Boolean) : []
  const res = await inv.updateDevice(selectedDevice.value.ip, { ...form.value, tags })
  actionLoading.value = false
  if (res.status === 'success') showEditModal.value = false
  else actionMsg.value = res.message
}

async function deleteDevice(d: Device) {
  if (!confirm(`确认删除 ${d.ip}？`)) return
  await inv.deleteDevice(d.ip)
}

async function rebootDevice(d: Device) {
  if (!confirm(`确认重启 ${d.ip}？`)) return
  const res = await inv.rebootDevice(d.ip)
  alert(res.message || (res.status === 'success' ? '已发送重启指令' : '失败'))
}

async function backupDevice(d: Device) {
  const res = await inv.backupDevice(d.ip)
  alert(res.status === 'success' ? `备份成功: ${res.filename}` : (res.message || '备份失败'))
}

const importFile = ref<File | null>(null)

async function submitImport() {
  if (!importFile.value) return
  const fd = new FormData()
  fd.append('file', importFile.value)
  actionLoading.value = true
  try {
    const res = await api.post('/inventory/import', fd)
    const d = res.data
    alert(`导入完成: 成功 ${d.imported}，跳过 ${d.skipped}，共 ${d.total} 条`)
    showImportModal.value = false
    inv.fetchDevices()
  } catch {
    alert('导入失败')
  } finally {
    actionLoading.value = false
  }
}

// Inline form component
const DeviceForm = defineComponent({
  props: {
    modelValue: { type: Object as () => FormModel, required: true },
    editing: Boolean,
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    function upd(key: keyof FormModel, val: unknown) {
      emit('update:modelValue', { ...props.modelValue, [key]: val })
    }
    const fields: { k: keyof FormModel; label: string; type?: string; span?: boolean }[] = [
      { k: 'ip', label: 'IP 地址' },
      { k: 'name', label: '设备名称' },
      { k: 'vendor', label: '厂商 (大写)' },
      { k: 'model', label: '型号' },
      { k: 'location', label: '位置' },
      { k: 'sn', label: '序列号' },
      { k: 'server', label: '所属服务器' },
      { k: 'ssh_user', label: 'SSH 用户' },
      { k: 'ssh_pass', label: 'SSH 密码', type: 'password' },
      { k: 'tags', label: '标签 (逗号分隔)', span: true },
    ]
    return () => h('div', { class: 'grid grid-cols-2 gap-4 text-sm' },
      [
        ...fields.map(f =>
          h('div', { key: f.k, class: f.span ? 'col-span-2' : '' }, [
            h('label', {
              class: 'block text-[10px] font-bold uppercase tracking-wider mb-1',
              style: 'color: var(--text-muted)'
            }, f.label),
            h('input', {
              type: f.type || 'text',
              value: props.modelValue[f.k],
              onInput: (e: Event) => upd(f.k, (e.target as HTMLInputElement).value),
              class: 'w-full px-3 py-2 rounded-xl border text-xs outline-none',
              style: 'background: var(--card-bg); border-color: var(--border); color: var(--text-main)',
            }),
          ])
        ),
        h('div', { class: 'flex items-center gap-2' }, [
          h('input', {
            type: 'checkbox',
            id: 'gpu_chk',
            checked: props.modelValue.gpu,
            onChange: (e: Event) => upd('gpu', (e.target as HTMLInputElement).checked),
          }),
          h('label', { for: 'gpu_chk', class: 'text-xs', style: 'color: var(--text-muted)' }, '含 GPU'),
        ]),
      ]
    )
  }
})
</script>

<template>
  <div class="space-y-4">
    <!-- Toolbar -->
    <div class="flex items-center gap-3 flex-wrap">
      <div class="flex-1 min-w-48 relative">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" style="color: var(--text-muted)" />
        <input
          v-model="search"
          placeholder="搜索 IP、名称、厂商…"
          class="w-full pl-9 pr-4 py-2.5 rounded-xl text-sm outline-none border input-glow"
          style="background: var(--card-bg); border-color: var(--border); color: var(--text-main)"
        />
      </div>
      <button @click="inv.fetchDevices()" class="p-2.5 rounded-xl border transition-colors hover:border-blue-500/50" style="border-color: var(--border)">
        <RefreshCw class="w-4 h-4" style="color: var(--text-muted)" />
      </button>
      <button v-if="auth.isOperator()" @click="showImportModal = true" class="flex items-center gap-2 px-4 py-2.5 rounded-xl border text-sm transition-colors hover:border-blue-500/50" style="border-color: var(--border); color: var(--text-muted)">
        <Upload class="w-4 h-4" /> 导入
      </button>
      <button v-if="auth.isOperator()" @click="showAddModal = true" class="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium transition-colors">
        <Plus class="w-4 h-4" /> 添加设备
      </button>
    </div>

    <!-- Table -->
    <div class="glass rounded-2xl overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr style="border-bottom: 1px solid var(--border)">
              <th v-for="header in ['IP地址','名称','厂商/型号','位置','状态','操作']" :key="header"
                class="text-left px-4 py-3 text-[11px] font-semibold uppercase tracking-wider"
                style="color: var(--text-muted)">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="d in filtered" :key="d.ip"
              class="border-b transition-colors hover:bg-white/2"
              style="border-color: var(--border)"
            >
              <td class="px-4 py-3 mono text-xs text-blue-400 font-medium">{{ d.ip }}</td>
              <td class="px-4 py-3 text-xs" style="color: var(--text-main)">{{ d.name || '—' }}</td>
              <td class="px-4 py-3 text-xs" style="color: var(--text-muted)">{{ d.vendor }}{{ d.model ? ' / ' + d.model : '' }}</td>
              <td class="px-4 py-3 text-xs" style="color: var(--text-muted)">{{ d.location || '—' }}</td>
              <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold" :class="`status-${d.status}`">{{ d.status }}</span>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center gap-1">
                  <button @click="selectedDevice = d; showDetailModal = true" class="p-1.5 rounded-lg hover:bg-blue-500/10 text-blue-400 transition-colors" title="详情">
                    <Eye class="w-3.5 h-3.5" />
                  </button>
                  <template v-if="auth.isOperator()">
                    <button @click="openEdit(d)" class="p-1.5 rounded-lg hover:bg-yellow-500/10 text-yellow-400 transition-colors" title="编辑">
                      <Pencil class="w-3.5 h-3.5" />
                    </button>
                    <button @click="rebootDevice(d)" class="p-1.5 rounded-lg hover:bg-orange-500/10 text-orange-400 transition-colors" title="重启">
                      <Power class="w-3.5 h-3.5" />
                    </button>
                    <button @click="backupDevice(d)" class="p-1.5 rounded-lg hover:bg-purple-500/10 text-purple-400 transition-colors" title="备份配置">
                      <HardDrive class="w-3.5 h-3.5" />
                    </button>
                    <button @click="deleteDevice(d)" class="p-1.5 rounded-lg hover:bg-red-500/10 text-red-400 transition-colors" title="删除">
                      <Trash2 class="w-3.5 h-3.5" />
                    </button>
                  </template>
                </div>
              </td>
            </tr>
            <tr v-if="filtered.length === 0">
              <td colspan="6" class="px-4 py-12 text-center text-sm" style="color: var(--text-muted)">
                {{ inv.loading ? '加载中…' : '暂无设备' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal v-if="showAddModal" title="添加设备" size="lg" @close="showAddModal = false; resetForm()">
      <DeviceForm v-model="form" />
      <p v-if="actionMsg" class="text-red-400 text-xs mt-3">{{ actionMsg }}</p>
      <template #footer>
        <button @click="showAddModal = false; resetForm()" class="px-4 py-2 rounded-xl text-sm border" style="border-color: var(--border); color: var(--text-muted)">取消</button>
        <button @click="submitAdd" :disabled="actionLoading" class="px-4 py-2 rounded-xl text-sm bg-blue-600 hover:bg-blue-500 text-white font-medium disabled:opacity-50">
          {{ actionLoading ? '保存中…' : '保存' }}
        </button>
      </template>
    </Modal>

    <!-- Edit Modal -->
    <Modal v-if="showEditModal" title="编辑设备" size="lg" @close="showEditModal = false">
      <DeviceForm v-model="form" :editing="true" />
      <p v-if="actionMsg" class="text-red-400 text-xs mt-3">{{ actionMsg }}</p>
      <template #footer>
        <button @click="showEditModal = false" class="px-4 py-2 rounded-xl text-sm border" style="border-color: var(--border); color: var(--text-muted)">取消</button>
        <button @click="submitEdit" :disabled="actionLoading" class="px-4 py-2 rounded-xl text-sm bg-blue-600 hover:bg-blue-500 text-white font-medium disabled:opacity-50">
          {{ actionLoading ? '保存中…' : '保存' }}
        </button>
      </template>
    </Modal>

    <!-- Detail Modal -->
    <Modal v-if="showDetailModal && selectedDevice" :title="`设备详情 — ${selectedDevice.ip}`" size="lg" @close="showDetailModal = false">
      <dl class="grid grid-cols-2 gap-x-8 gap-y-3 text-sm">
        <template v-for="[k, v] in (Object.entries(selectedDevice) as [string, unknown][])" :key="k">
          <div v-if="k !== 'id' && k !== 'ssh_pass'">
            <dt class="text-[11px] font-semibold uppercase tracking-wider mb-0.5" style="color: var(--text-muted)">{{ k }}</dt>
            <dd class="mono text-xs" style="color: var(--text-main)">{{ Array.isArray(v) ? (v as string[]).join(', ') || '—' : String(v || '—') }}</dd>
          </div>
        </template>
      </dl>
    </Modal>

    <!-- Import Modal -->
    <Modal v-if="showImportModal" title="批量导入设备" size="sm" @close="showImportModal = false">
      <p class="text-xs mb-3" style="color: var(--text-muted)">上传 Excel (.xlsx) 文件，支持字段: ip, name, vendor, model, location, sn, ssh_user, ssh_pass, tags</p>
      <input type="file" accept=".xlsx,.csv" @change="(e) => importFile = (e.target as HTMLInputElement).files?.[0] ?? null" class="text-sm" style="color: var(--text-main)" />
      <template #footer>
        <button @click="showImportModal = false" class="px-4 py-2 rounded-xl text-sm border" style="border-color: var(--border); color: var(--text-muted)">取消</button>
        <button @click="submitImport" :disabled="!importFile || actionLoading" class="px-4 py-2 rounded-xl text-sm bg-blue-600 hover:bg-blue-500 text-white font-medium disabled:opacity-50">
          {{ actionLoading ? '导入中…' : '开始导入' }}
        </button>
      </template>
    </Modal>
  </div>
</template>
