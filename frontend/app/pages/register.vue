<script setup lang="ts">
import type { AuthFormField, FormSubmitEvent } from '@nuxt/ui'
import { motion } from 'motion-v'

interface RegisterData {
  email: string
  password: string
}

const api = useRuntimeConfig().public.apiBase
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
    description: 'Usa al menos 8 caracteres.',
    placeholder: 'Crea una contraseña',
    icon: 'i-lucide-lock-keyhole',
    autocomplete: 'new-password',
    minlength: 8,
    size: 'xl',
    required: true,
  },
]

async function submit(event: FormSubmitEvent<RegisterData>) {
  isSubmitting.value = true
  errorMessage.value = ''

  try {
    await $fetch(`${api}/auth/register`, {
      method: 'POST',
      body: {
        email: event.data.email,
        password: event.data.password,
      },
    })
    await navigateTo('/login')
  } catch {
    errorMessage.value = 'No pudimos crear la cuenta. Revisa los datos e inténtalo de nuevo.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="relative grid min-h-screen place-items-center overflow-hidden bg-[#03045e] px-5 py-12">
    <div class="pointer-events-none absolute left-1/2 top-0 h-80 w-80 -translate-x-1/2 rounded-full bg-[#00b4d8]/20 blur-3xl" />
    <div class="pointer-events-none absolute bottom-0 left-0 h-72 w-72 rounded-full bg-[#023e8a]/70 blur-3xl" />

    <motion.div
      class="relative z-10 w-full max-w-md"
      :initial="{ opacity: 0, y: 24 }"
      :animate="{ opacity: 1, y: 0 }"
      :transition="{ duration: 0.4, ease: 'easeOut' }"
    >
      <UCard class="border border-cyan-400/25 bg-blue-950/65 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur-xl">
        <UAuthForm
          title="Crea tu cuenta"
          description="Regístrate con tu correo y empieza a jugar."
          icon="i-lucide-user-round-plus"
          :fields="fields"
          :loading="isSubmitting"
          :submit="{ label: 'Crear cuenta', size: 'xl', block: true, icon: 'i-lucide-user-plus' }"
          @submit="submit"
        >
          <template #validation>
            <UAlert v-if="errorMessage" color="error" variant="subtle" icon="i-lucide-circle-alert" :title="errorMessage" />
          </template>

          <template #footer>
            ¿Ya tienes cuenta?
            <ULink to="/login" class="font-bold text-cyan-300 hover:text-cyan-200">Inicia sesión</ULink>
          </template>
        </UAuthForm>
      </UCard>
    </motion.div>
  </main>
</template>
