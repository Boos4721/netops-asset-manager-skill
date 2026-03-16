<script setup lang="ts">
defineProps<{ status: string }>()
</script>

<template>
  <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold mono" :class="`status-${status}`">
    {{ status }}
  </span>
</template>
