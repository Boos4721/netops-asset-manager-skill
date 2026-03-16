import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/client'

export const useStatsStore = defineStore('stats', () => {
  const stats = ref({ total: 0, online: 0, offline: 0, alerts: 0, gpu_count: 0 })

  async function fetchStats() {
    const res = await api.get('/stats')
    stats.value = res.data
  }

  return { stats, fetchStats }
})
