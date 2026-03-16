<script setup lang="ts">
import { ref, nextTick } from 'vue'
import api from '@/api/client'
import { Send } from 'lucide-vue-next'

interface Message {
  from: 'user' | 'ai'
  text: string
  html?: string
}

const messages = ref<Message[]>([
  { from: 'ai', text: '你好！我是 NetOps AI 助手，基于 OpenClaw 驱动。我可以帮你查询资产信息、分析日志，或直接录入新设备。请问有什么需要帮助？' }
])
const input = ref('')
const loading = ref(false)
const chatBox = ref<HTMLElement>()

let marked: any = null

async function getMarked() {
  if (!marked) {
    const m = await import('marked')
    marked = m.marked
  }
  return marked
}

async function renderMarkdown(text: string) {
  const m = await getMarked()
  return m(text)
}

async function send() {
  const msg = input.value.trim()
  if (!msg || loading.value) return
  input.value = ''

  messages.value.push({ from: 'user', text: msg })
  loading.value = true
  await scrollBottom()

  try {
    const history = messages.value.slice(-20).map(m => ({ from: m.from, text: m.text }))
    const res = await api.post('/chat', { message: msg, history })
    const reply = res.data.reply || res.data.message || '（无响应）'
    const html = await renderMarkdown(reply)
    messages.value.push({ from: 'ai', text: reply, html })
  } catch(e) {
    messages.value.push({ from: 'ai', text: '连接失败，请检查 OpenClaw 服务。' })
  } finally {
    loading.value = false
    await scrollBottom()
  }
}

async function scrollBottom() {
  await nextTick()
  if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
}

function onKey(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
}
</script>

<template>
  <div class="flex flex-col h-[calc(100vh-8rem)] glass rounded-2xl overflow-hidden">
    <!-- Messages -->
    <div ref="chatBox" class="flex-1 overflow-y-auto p-6 space-y-4">
      <div v-for="(msg, i) in messages" :key="i" :class="msg.from === 'user' ? 'flex justify-end' : 'flex justify-start'">
        <div
          :class="[
            'max-w-[75%] px-4 py-3 rounded-2xl text-sm',
            msg.from === 'user'
              ? 'bg-blue-600 text-white rounded-tr-sm'
              : 'glass rounded-tl-sm'
          ]"
        >
          <div v-if="msg.from === 'ai' && msg.html" class="markdown-body" v-html="msg.html"></div>
          <p v-else class="whitespace-pre-wrap" :style="msg.from === 'user' ? '' : 'color: var(--text-main)'">{{ msg.text }}</p>
        </div>
      </div>
      <div v-if="loading" class="flex justify-start">
        <div class="glass px-4 py-3 rounded-2xl rounded-tl-sm">
          <div class="flex gap-1.5 items-center">
            <div v-for="n in 3" :key="n" class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce" :style="`animation-delay: ${(n-1) * 0.15}s`"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="p-4 border-t" style="border-color: var(--border)">
      <div class="flex gap-3">
        <textarea
          v-model="input"
          @keydown="onKey"
          rows="1"
          placeholder="输入消息… (Enter 发送，Shift+Enter 换行)"
          class="flex-1 px-4 py-3 rounded-xl border text-sm outline-none resize-none input-glow"
          style="background: var(--card-bg); border-color: var(--border); color: var(--text-main); min-height: 44px; max-height: 120px"
        ></textarea>
        <button
          @click="send"
          :disabled="!input.trim() || loading"
          class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white transition-colors disabled:opacity-40"
        >
          <Send class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>
