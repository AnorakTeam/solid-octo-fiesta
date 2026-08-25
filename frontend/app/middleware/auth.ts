export default defineNuxtRouteMiddleware(() => { if (!useAuthStore().access) return navigateTo('/login') })
