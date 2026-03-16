import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/client'

export interface Device {
  id: number
  ip: string
  name: string
  vendor: string
  model: string
  location: string
  sn: string
  server: string
  driver: string
  tags: string[]
  ssh_user: string
  status: 'online' | 'offline' | 'unknown'
  last_seen: string | null
  gpu: boolean
  created_at: string
  updated_at: string
}

export const useInventoryStore = defineStore('inventory', () => {
  const devices = ref<Device[]>([])
  const loading = ref(false)

  async function fetchDevices() {
    loading.value = true
    try {
      const res = await api.get('/inventory')
      devices.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function addDevice(payload: Partial<Device> & { ssh_pass?: string }) {
    const res = await api.post('/inventory/add', payload)
    if (res.data.status === 'success') await fetchDevices()
    return res.data
  }

  async function updateDevice(ip: string, payload: Partial<Device> & { ssh_pass?: string }) {
    const res = await api.put(`/inventory/${ip}`, payload)
    if (res.data.status === 'success') await fetchDevices()
    return res.data
  }

  async function deleteDevice(ip: string) {
    const res = await api.delete(`/inventory/${ip}`)
    if (res.data.status === 'success') await fetchDevices()
    return res.data
  }

  async function rebootDevice(ip: string, user = 'root', password = '') {
    const res = await api.post(`/inventory/reboot/${ip}`, { user, password })
    return res.data
  }

  async function backupDevice(ip: string) {
    const res = await api.post(`/inventory/backup/${ip}`)
    return res.data
  }

  return { devices, loading, fetchDevices, addDevice, updateDevice, deleteDevice, rebootDevice, backupDevice }
})
