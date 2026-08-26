export const useAuthStore = defineStore('auth', () => {
  // Estas cookies son legibles por Nuxt porque el access token se envía como
  // header Authorization. En producción, servir la aplicación por HTTPS.
  const access = useCookie<string>('clicker_access', {
    default: () => '', maxAge: 60 * 60 * 4, sameSite: 'lax', secure: !import.meta.dev,
  })
  const refresh = useCookie<string>('clicker_refresh', {
    default: () => '', maxAge: 60 * 60 * 24 * 7, sameSite: 'lax', secure: !import.meta.dev,
  })
  const user = useState<any | null>('auth_user', () => null)
  const api = useRuntimeConfig().public.apiBase

  function clearSession() { access.value = ''; refresh.value = ''; user.value = null }

  async function refreshAccessToken() {
    if (!refresh.value) return false
    try {
      const data: any = await $fetch(`${api}/auth/refresh`, { method: 'POST', body: { refresh: refresh.value } })
      access.value = data.access
      return true
    } catch {
      clearSession()
      return false
    }
  }

  async function apiFetch<T>(path: string, options: Record<string, any> = {}, retried = false): Promise<T> {
    try {
      return await $fetch<T>(`${api}${path}`, {
        ...options,
        headers: { ...options.headers, Authorization: `Bearer ${access.value}` },
      })
    } catch (error: any) {
      const status = error?.response?.status ?? error?.statusCode
      if (status === 401 && !retried && await refreshAccessToken()) return apiFetch<T>(path, options, true)
      throw error
    }
  }

  async function login(email: string, password: string) {
    const data: any = await $fetch(`${api}/auth/login`, { method: 'POST', body: { email, password } })
    access.value = data.access; refresh.value = data.refresh
    await loadUser()
  }
  async function loadUser() { user.value = await apiFetch('/users/me') }
  async function updateProfile(nickname: string, profileIcon?: File | null) {
    const body = new FormData()
    body.append('nickname', nickname)
    if (profileIcon) body.append('profile_icon', profileIcon)
    user.value = await apiFetch('/users/me/profile', { method: 'PATCH', body })
  }
  async function restoreSession() {
    if (access.value) return true
    return refreshAccessToken()
  }
  function logout() { clearSession(); return navigateTo('/login') }
  return { access, refresh, user, login, loadUser, updateProfile, logout, restoreSession, refreshAccessToken, apiFetch }
})
