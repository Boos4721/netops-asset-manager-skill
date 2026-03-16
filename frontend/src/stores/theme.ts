import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

type Theme = 'dark' | 'light' | 'auto'

function getAutoTheme(): 'dark' | 'light' {
  const hour = new Date().getHours()
  return (hour >= 8 && hour < 18) ? 'light' : 'dark'
}

export const useThemeStore = defineStore('theme', () => {
  const preference = ref<Theme>((localStorage.getItem('theme') as Theme) || 'auto')

  const current = computed((): 'dark' | 'light' => {
    if (preference.value === 'auto') return getAutoTheme()
    return preference.value
  })

  function set(t: Theme) {
    preference.value = t
    localStorage.setItem('theme', t)
    applyTheme()
  }

  function applyTheme() {
    document.documentElement.setAttribute('data-theme', current.value)
  }

  applyTheme()

  return { preference, current, set, applyTheme }
})
