export default defineNuxtRouteMiddleware(async () => {
  const auth = useAuthStore()
  if (!await auth.restoreSession()) return navigateTo('/login')
})
