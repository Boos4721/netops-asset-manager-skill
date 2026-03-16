<script setup lang="ts">
defineProps<{ message?: string; loading?: boolean }>()
const emit = defineEmits<{ confirm: []; cancel: [] }>()
</script>

<template>
  <Modal title="确认操作" size="sm" @close="emit('cancel')">
    <p class="text-sm" style="color: var(--text-muted)">{{ message || '确认执行此操作？' }}</p>
    <template #footer>
      <button @click="emit('cancel')" class="px-4 py-2 rounded-xl text-sm border transition-colors" style="border-color: var(--border); color: var(--text-muted)">取消</button>
      <button @click="emit('confirm')" :disabled="loading" class="px-4 py-2 rounded-xl text-sm bg-red-600 hover:bg-red-500 text-white font-medium transition-colors disabled:opacity-50">
        {{ loading ? '执行中…' : '确认' }}
      </button>
    </template>
  </Modal>
</template>

<script>
import Modal from './Modal.vue'
</script>
