<script setup lang="ts">
import type { AuthFormField, FormSubmitEvent } from '@nuxt/ui'
import { motion } from 'motion-v'

interface LoginData {
  email: string
  password: string
}

const auth = useAuthStore()
const isSubmitting = ref(false)
const errorMessage = ref('')

const fields: AuthFormField[] = [
  {
    name: 'email',
    type: 'email',
    label: 'Correo electrónico',
    placeholder: 'tu@correo.com',
    icon: 'i-lucide-mail',
    autocomplete: 'email',
    size: 'xl',
    required: true,
  },
  {
    name: 'password',
    type: 'password',
    label: 'Contraseña',
    placeholder: 'Escribe tu contraseña',
    icon: 'i-lucide-lock-keyhole',
    autocomplete: 'current-password',
    size: 'xl',
    required: true,
  },
]

async function submit(event: FormSubmitEvent<LoginData>) {
  isSubmitting.value = true
  errorMessage.value = ''

  try {
    await auth.login(event.data.email, event.data.password)
    await navigateTo('/game')
  } catch {
    errorMessage.value = 'No pudimos iniciar sesión. Revisa el correo y la contraseña.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="relative grid min-h-screen place-items-center overflow-hidden px-5 py-12">
    <div class="pointer-events-none absolute left-1/2 top-0 h-80 w-80 -translate-x-1/2 rounded-full bg-[#00b4d8]/20 blur-3xl" />
    <div class="pointer-events-none absolute bottom-0 right-0 h-72 w-72 rounded-full bg-[#023e8a]/70 blur-3xl" />

    <div class="relative z-10 grid w-full max-w-4xl items-center gap-6 md:grid-cols-[minmax(0,1fr)_22rem]">
      <motion.div
        :initial="{ opacity: 0, x: -24 }"
        :animate="{ opacity: 1, x: 0 }"
        :transition="{ duration: 0.4, ease: 'easeOut' }"
      >
        <UCard class="border border-cyan-400/25 bg-blue-950/65 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur-xl">
          <UAuthForm
            title="Inicia sesión"
            description="Entra y continúa sumando puntos."
            icon="i-lucide-gamepad-2"
            :fields="fields"
            :loading="isSubmitting"
            :submit="{ label: 'Entrar al juego', size: 'xl', block: true, icon: 'i-lucide-log-in' }"
            @submit="submit"
          >
            <template #validation>
              <UAlert v-if="errorMessage" color="error" variant="subtle" icon="i-lucide-circle-alert" :title="errorMessage" />
            </template>

            <template #footer>
              ¿No tienes cuenta?
              <ULink to="/register" class="font-bold text-cyan-300 hover:text-cyan-200">Regístrate</ULink>
            </template>
          </UAuthForm>
        </UCard>
      </motion.div>

      <motion.div
        :initial="{ opacity: 0, x: 24 }"
        :animate="{ opacity: 1, x: 0 }"
        :transition="{ duration: 0.4, delay: 0.1, ease: 'easeOut' }"
      >
        <GameTopRankings />
      </motion.div>
    </div>
  </main>
</template>
