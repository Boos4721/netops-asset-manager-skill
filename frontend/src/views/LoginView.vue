<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ShieldCheck, ArrowRight } from 'lucide-vue-next'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function login() {
  error.value = ''
  loading.value = true
  try {
    const res = await auth.login(username.value, password.value)
    if (res.ok) {
      router.push('/dashboard')
    } else {
      error.value = res.message || '认证失败'
    }
  } catch (e) {
    error.value = '服务器连接失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center p-4" style="background: var(--bg)">
    <div class="glass rounded-[2.5rem] p-12 max-w-md w-full relative overflow-hidden">
      <div class="absolute -top-24 -left-24 w-48 h-48 bg-blue-600/10 blur-[100px]"></div>

      <div class="text-center mb-10">
        <div class="w-20 h-20 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-2xl shadow-blue-500/20 glow-blue">
          <ShieldCheck class="w-10 h-10 text-white" />
        </div>
        <h2 class="text-3xl font-bold tracking-tight" style="color: var(--text-main)">
          NetOps <span class="text-blue-500">Pro</span>
        </h2>
        <p class="text-sm mt-3 font-medium" style="color: var(--text-muted)">智能网络资产管理平台</p>
      </div>

      <form @submit.prevent="login" class="space-y-5">
        <div class="space-y-1.5">
          <label class="block text-[10px] font-bold uppercase tracking-widest ml-1" style="color: var(--text-muted)">身份 (Username)</label>
          <input
            v-model="username"
            type="text"
            required
            placeholder="Username"
            class="w-full px-5 py-4 rounded-2xl text-sm outline-none transition-all input-glow border"
            style="background: rgba(148,163,184,0.05); border-color: rgba(148,163,184,0.1); color: var(--text-main)"
          />
        </div>
        <div class="space-y-1.5">
          <label class="block text-[10px] font-bold uppercase tracking-widest ml-1" style="color: var(--text-muted)">凭据 (Access Key)</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
            class="w-full px-5 py-4 rounded-2xl text-sm outline-none transition-all input-glow border"
            style="background: rgba(148,163,184,0.05); border-color: rgba(148,163,184,0.1); color: var(--text-main)"
          />
        </div>
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-2xl font-bold transition-all shadow-xl shadow-blue-600/20 active:scale-95 flex items-center justify-center gap-2 disabled:opacity-60"
        >
          {{ loading ? '验证中…' : '验证身份' }}
          <ArrowRight v-if="!loading" class="w-4 h-4" />
        </button>
        <p v-if="error" class="text-red-400 text-xs text-center font-medium">{{ error }}</p>
      </form>
    </div>
  </div>
</template>
