export default defineNuxtConfig({
  modules: ['@pinia/nuxt', '@nuxt/ui', 'motion-v/nuxt'],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api/v1',
    },
  },
  routeRules: {
    '/api/v1/**': {
      proxy: process.env.GATEWAY_URL ? `${process.env.GATEWAY_URL}/api/v1/**` : 'http://gateway:8000/api/v1/**',
    },
    '/media/**': {
      proxy: process.env.GATEWAY_URL ? `${process.env.GATEWAY_URL}/media/**` : 'http://gateway:8000/media/**',
    },
  },
  compatibilityDate: '2025-01-01',
})
