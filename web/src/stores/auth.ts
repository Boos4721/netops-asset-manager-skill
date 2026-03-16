import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const username = ref<string | null>(localStorage.getItem('username'))
  const role = ref<string | null>(localStorage.getItem('role'))

  const isLoggedIn = () => !!token.value

  async function login(usernameVal: string, password: string): Promise<{ ok: boolean; message?: string }> {
    const res = await axios.post('/api/users/login', { username: usernameVal, password })
    const data = res.data
    if (data.status === 'success') {
      token.value = data.token
      username.value = data.username
      role.value = data.role
      localStorage.setItem('token', data.token)
      localStorage.setItem('username', data.username)
      localStorage.setItem('role', data.role)
      return { ok: true }
    }
    return { ok: false, message: data.message }
  }

  function logout() {
    token.value = null
    username.value = null
    role.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('role')
  }

  function isRoot() { return role.value === 'root' }
  function isOperator() { return role.value === 'operator' || role.value === 'root' }

  return { token, username, role, isLoggedIn, login, logout, isRoot, isOperator }
})
