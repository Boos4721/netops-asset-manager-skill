<script setup lang="ts">
import { onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { RouterView } from 'vue-router'

const theme = useThemeStore()
onMounted(() => theme.applyTheme())
</script>

<template>
  <div class="mesh-gradient"></div>
  <RouterView />
</template>
