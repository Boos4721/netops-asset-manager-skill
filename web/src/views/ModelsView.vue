<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import Modal from '@/components/ui/Modal.vue'
import { Plus, Pencil, Trash2, Star } from 'lucide-vue-next'

const auth = useAuthStore()
const models = ref<any[]>([])

onMounted(fetchModels)

async function fetchModels() {
  const res = await api.get('/models')
  models.value = res.data
}

const showAddModal = ref(false)
const editingModel = ref<any>(null)
const form = ref({ id: '', name: '', provider: '', base_url: '', api_key: '', contextWindow: 4096, maxTokens: 4096, reasoning: false })

function openAdd() {
  form.value = { id: '', name: '', provider: '', base_url: '', api_key: '', contextWindow: 4096, maxTokens: 4096, reasoning: false }
  editingModel.value = null
  showAddModal.value = true
}

function openEdit(m: any) {
  form.value = { id: m.id, name: m.name, provider: m.provider, base_url: m.base_url, api_key: m.api_key, contextWindow: m.contextWindow, maxTokens: m.maxTokens, reasoning: m.reasoning }
  editingModel.value = m
  showAddModal.value = true
}

async function submitForm() {
  if (editingModel.value) {
    await api.put(`/models/${editingModel.value.id}`, form.value)
  } else {
    await api.post('/models/add', form.value)
  }
  showAddModal.value = false
  await fetchModels()
}

async function deleteModel(id: string) {
  if (!confirm('确认删除此模型？')) return
  await api.delete(`/models/${id}`)
  await fetchModels()
}

async function setDefault(m: any) {
  await api.post('/models/set-default', { model_id: m.id, provider: m.provider })
  alert(`已设置 ${m.name} 为默认模型`)
}
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <p class="text-sm" style="color: var(--text-muted)">管理 OpenClaw AI 模型配置</p>
      <button v-if="auth.isRoot()" @click="openAdd" class="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium">
        <Plus class="w-4 h-4" /> 添加模型
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="m in models" :key="m.id" class="glass rounded-2xl p-5 card-hover flex flex-col gap-3">
        <div class="flex items-start justify-between">
          <div>
            <div class="font-semibold text-sm" style="color: var(--text-main)">{{ m.name }}</div>
            <div class="text-xs mono mt-0.5" style="color: var(--text-muted)">{{ m.provider }}</div>
          </div>
          <span v-if="m.reasoning" class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-purple-500/10 text-purple-400">推理</span>
        </div>
        <div class="grid grid-cols-2 gap-2 text-xs" style="color: var(--text-muted)">
          <div><span class="font-medium">Context:</span> {{ (m.contextWindow / 1024).toFixed(0) }}K</div>
          <div><span class="font-medium">MaxTokens:</span> {{ m.maxTokens }}</div>
        </div>
        <div v-if="auth.isRoot()" class="flex items-center gap-1.5 pt-1 border-t" style="border-color: var(--border)">
          <button @click="setDefault(m)" class="flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded-lg text-xs hover:bg-yellow-500/10 text-yellow-400 transition-colors">
            <Star class="w-3.5 h-3.5" /> 设为默认
          </button>
          <button @click="openEdit(m)" class="p-1.5 rounded-lg hover:bg-blue-500/10 text-blue-400 transition-colors">
            <Pencil class="w-3.5 h-3.5" />
          </button>
          <button @click="deleteModel(m.id)" class="p-1.5 rounded-lg hover:bg-red-500/10 text-red-400 transition-colors">
            <Trash2 class="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
      <div v-if="models.length === 0" class="col-span-3 text-center py-12 text-sm" style="color: var(--text-muted)">
        暂无模型，请添加
      </div>
    </div>

    <Modal v-if="showAddModal" :title="editingModel ? '编辑模型' : '添加模型'" @close="showAddModal = false">
      <div class="space-y-4 text-sm">
        <div v-for="field in [
          {k:'id',label:'模型 ID'},
          {k:'name',label:'显示名称'},
          {k:'provider',label:'提供商'},
          {k:'base_url',label:'Base URL'},
          {k:'api_key',label:'API Key',type:'password'},
        ]" :key="field.k">
          <label class="block text-[10px] font-bold uppercase tracking-wider mb-1" style="color: var(--text-muted)">{{ field.label }}</label>
          <input
            v-model="(form as any)[field.k]"
            :type="field.type || 'text'"
            class="w-full px-3 py-2 rounded-xl border text-xs outline-none input-glow"
            style="background: var(--card-bg); border-color: var(--border); color: var(--text-main)"
          />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-wider mb-1" style="color: var(--text-muted)">Context Window</label>
            <input v-model.number="form.contextWindow" type="number" class="w-full px-3 py-2 rounded-xl border text-xs outline-none" style="background: var(--card-bg); border-color: var(--border); color: var(--text-main)" />
          </div>
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-wider mb-1" style="color: var(--text-muted)">Max Tokens</label>
            <input v-model.number="form.maxTokens" type="number" class="w-full px-3 py-2 rounded-xl border text-xs outline-none" style="background: var(--card-bg); border-color: var(--border); color: var(--text-main)" />
          </div>
        </div>
        <div class="flex items-center gap-2">
          <input type="checkbox" v-model="form.reasoning" id="reasoning" />
          <label for="reasoning" class="text-xs" style="color: var(--text-muted)">支持推理 (Reasoning)</label>
        </div>
      </div>
      <template #footer>
        <button @click="showAddModal = false" class="px-4 py-2 rounded-xl text-sm border" style="border-color: var(--border); color: var(--text-muted)">取消</button>
        <button @click="submitForm" class="px-4 py-2 rounded-xl text-sm bg-blue-600 hover:bg-blue-500 text-white font-medium">保存</button>
      </template>
    </Modal>
  </div>
</template>
