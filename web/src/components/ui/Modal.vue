<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { X } from 'lucide-vue-next'

defineProps<{ title?: string; size?: 'sm' | 'md' | 'lg' | 'xl' }>()
const emit = defineEmits(['close'])

function onKey(e: KeyboardEvent) {
  if (e.key === 'Escape') emit('close')
}
onMounted(() => document.addEventListener('keydown', onKey))
onUnmounted(() => document.removeEventListener('keydown', onKey))
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" @click.self="emit('close')">
      <div
        class="glass rounded-2xl w-full shadow-2xl flex flex-col max-h-[90vh]"
        :class="{
          'max-w-md': size === 'sm',
          'max-w-lg': !size || size === 'md',
          'max-w-2xl': size === 'lg',
          'max-w-4xl': size === 'xl',
        }"
      >
        <div class="flex items-center justify-between px-6 py-4 border-b" style="border-color: var(--border)">
          <h2 class="font-semibold text-sm" style="color: var(--text-main)">{{ title }}</h2>
          <button @click="emit('close')" class="p-1.5 rounded-lg hover:bg-white/5 transition-colors" style="color: var(--text-muted)">
            <X class="w-4 h-4" />
          </button>
        </div>
        <div class="overflow-y-auto flex-1 p-6">
          <slot />
        </div>
        <div v-if="$slots.footer" class="px-6 py-4 border-t flex gap-3 justify-end" style="border-color: var(--border)">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </Teleport>
</template>
