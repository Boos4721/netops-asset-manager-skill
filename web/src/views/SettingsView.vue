<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import Modal from '@/components/ui/Modal.vue'
import { Plus, Trash2, Sun, Moon, Monitor } from 'lucide-vue-next'

const auth = useAuthStore()
const theme = useThemeStore()

// System info
const sysInfo = ref<any>({})
onMounted(async () => {
  const res = await api.get('/system/info')
  sysInfo.value = res.data
  if (auth.isRoot()) fetchUsers()
})

// Users
const users = ref<any[]>([])
const showAddUser = ref(false)
const userForm = ref({ username: '', password: '', role: 'operator' })
const userMsg = ref('')

async function fetchUsers() {
  const res = await api.get('/users')
  users.value = res.data
}

async function addUser() {
  userMsg.value = ''
  const res = await api.post('/users', userForm.value)
  if (res.data.status === 'success') {
    showAddUser.value = false
    userForm.value = { username: '', password: '', role: 'operator' }
    await fetchUsers()
  } else {
    userMsg.value = res.data.message || '创建失败'
  }
}

async function deleteUser(id: number) {
  if (!confirm('确认删除此用户？')) return
  await api.delete(`/users/${id}`)
  await fetchUsers()
}

const themeOptions = [
  { value: 'dark', label: '深色', icon: Moon },
  { value: 'light', label: '浅色', icon: Sun },
  { value: 'auto', label: '自动', icon: Monitor },
] as const
</script>

<template>
  <div class="space-y-6">
    <!-- System Info -->
    <div class="glass rounded-2xl p-6">
      <h2 class="font-semibold text-sm mb-4" style="color: var(--text-main)">系统信息</h2>
      <dl class="grid grid-cols-2 gap-4 text-sm">
        <div v-for="[k, v] in Object.entries(sysInfo)" :key="k">
          <dt class="text-[11px] font-semibold uppercase tracking-wider mb-0.5" style="color: var(--text-muted)">{{ k }}</dt>
          <dd class="mono text-xs" style="color: var(--text-main)">{{ v }}</dd>
        </div>
      </dl>
    </div>

    <!-- Theme -->
    <div class="glass rounded-2xl p-6">
      <h2 class="font-semibold text-sm mb-4" style="color: var(--text-main)">外观主题</h2>
      <div class="flex gap-3">
        <button
          v-for="opt in themeOptions"
          :key="opt.value"
          @click="theme.set(opt.value)"
          class="flex items-center gap-2 px-4 py-2.5 rounded-xl border text-sm transition-all"
          :class="theme.preference === opt.value ? 'border-blue-500 text-blue-400 bg-blue-500/10' : 'hover:border-blue-500/40'"
          :style="theme.preference !== opt.value ? 'border-color: var(--border); color: var(--text-muted)' : ''"
        >
          <component :is="opt.icon" class="w-4 h-4" />
          {{ opt.label }}
        </button>
      </div>
    </div>

    <!-- User Management (root only) -->
    <div v-if="auth.isRoot()" class="glass rounded-2xl p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-semibold text-sm" style="color: var(--text-main)">用户管理</h2>
        <button @click="showAddUser = true" class="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium">
          <Plus class="w-4 h-4" /> 添加用户
        </button>
      </div>
      <table class="w-full text-sm">
        <thead>
          <tr style="border-bottom: 1px solid var(--border)">
            <th v-for="h in ['用户名', '角色', '状态', '创建时间', '操作']" :key="h"
              class="text-left py-2 px-3 text-[11px] font-semibold uppercase tracking-wider"
              style="color: var(--text-muted)">{{ h }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id" class="border-b" style="border-color: var(--border)">
            <td class="py-2.5 px-3 text-xs font-medium" style="color: var(--text-main)">{{ u.username }}</td>
            <td class="py-2.5 px-3">
              <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold"
                :class="u.role === 'root' ? 'bg-red-500/10 text-red-400' : u.role === 'operator' ? 'bg-blue-500/10 text-blue-400' : 'bg-slate-500/10 text-slate-400'">
                {{ u.role }}
              </span>
            </td>
            <td class="py-2.5 px-3">
              <span :class="u.active ? 'text-emerald-400' : 'text-slate-500'" class="text-xs">{{ u.active ? '活跃' : '禁用' }}</span>
            </td>
            <td class="py-2.5 px-3 text-xs mono" style="color: var(--text-muted)">{{ new Date(u.created_at).toLocaleDateString() }}</td>
            <td class="py-2.5 px-3">
              <button v-if="u.username !== auth.username" @click="deleteUser(u.id)" class="p-1.5 rounded-lg hover:bg-red-500/10 text-red-400">
                <Trash2 class="w-3.5 h-3.5" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add User Modal -->
    <Modal v-if="showAddUser" title="添加用户" size="sm" @close="showAddUser = false">
      <div class="space-y-4">
        <div v-for="field in [{k:'username',label:'用户名'},{k:'password',label:'密码',type:'password'}]" :key="field.k">
          <label class="block text-[10px] font-bold uppercase tracking-wider mb-1" style="color: var(--text-muted)">{{ field.label }}</label>
          <input v-model="(userForm as any)[field.k]" :type="field.type || 'text'" class="w-full px-3 py-2 rounded-xl border text-xs outline-none input-glow" style="background: var(--card-bg); border-color: var(--border); color: var(--text-main)" />
        </div>
        <div>
          <label class="block text-[10px] font-bold uppercase tracking-wider mb-1" style="color: var(--text-muted)">角色</label>
          <select v-model="userForm.role" class="w-full px-3 py-2 rounded-xl border text-xs outline-none" style="background: var(--card-bg); border-color: var(--border); color: var(--text-main)">
            <option value="viewer">viewer</option>
            <option value="operator">operator</option>
            <option value="root">root</option>
          </select>
        </div>
        <p v-if="userMsg" class="text-red-400 text-xs">{{ userMsg }}</p>
      </div>
      <template #footer>
        <button @click="showAddUser = false" class="px-4 py-2 rounded-xl text-sm border" style="border-color: var(--border); color: var(--text-muted)">取消</button>
        <button @click="addUser" class="px-4 py-2 rounded-xl text-sm bg-blue-600 hover:bg-blue-500 text-white font-medium">创建</button>
      </template>
    </Modal>
  </div>
</template>
