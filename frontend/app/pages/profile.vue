<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const auth = useAuthStore()
const nickname = ref('')
const selectedIcon = ref<File | null>(null)
const preview = ref('')
const isSaving = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

onMounted(async () => {
  if (!auth.user) await auth.loadUser()
  nickname.value = auth.user?.nickname || ''
  preview.value = auth.user?.profile_icon || ''
})

function selectIcon(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  selectedIcon.value = file
  preview.value = URL.createObjectURL(file)
}

async function save() {
  isSaving.value = true; errorMessage.value = ''; successMessage.value = ''
  try {
    await auth.updateProfile(nickname.value, selectedIcon.value)
    preview.value = auth.user?.profile_icon || preview.value
    successMessage.value = 'Perfil actualizado. Tu progreso se mantiene intacto.'
  } catch (error: any) {
    const data = error?.data
    errorMessage.value = data?.nickname?.[0] || data?.profile_icon?.[0] || 'No fue posible guardar el perfil.'
  } finally { isSaving.value = false }
}
</script>

<template>
  <main class="mx-auto min-h-screen max-w-xl px-6 py-12">
    <NuxtLink class="text-cyan-300 hover:text-white" to="/game">← Volver al juego</NuxtLink>
    <section class="mt-6 rounded-2xl border border-cyan-400/30 bg-blue-950/70 p-7 shadow-xl">
      <h1 class="text-3xl font-black text-white">Mi perfil</h1>
      <p class="mt-2 text-cyan-100">Personaliza tu identidad sin afectar tu puntuación.</p>
      <form class="mt-8 grid gap-6" @submit.prevent="save">
        <div class="flex items-center gap-5">
          <img v-if="preview" :src="preview" alt="Vista previa del ícono de perfil" class="h-20 w-20 rounded-full object-cover ring-2 ring-cyan-300" />
          <div v-else class="grid h-20 w-20 place-items-center rounded-full bg-cyan-400 text-3xl font-black text-blue-950">{{ nickname.slice(0, 1).toUpperCase() }}</div>
          <label class="cursor-pointer rounded-lg border border-cyan-300/60 px-4 py-2 text-sm font-semibold text-cyan-100 hover:bg-cyan-300/10">
            Elegir ícono
            <input class="sr-only" type="file" accept="image/png,image/jpeg,image/webp" @change="selectIcon" />
          </label>
        </div>
        <p class="-mt-4 text-xs text-cyan-200/80">JPG, PNG o WebP · máximo 2 MB.</p>
        <label class="grid gap-2 text-sm font-bold text-cyan-100">Nickname
          <input v-model="nickname" minlength="3" maxlength="40" pattern="[a-zA-Z0-9_]+" class="rounded-lg bg-slate-950/70 px-4 py-3 text-white ring-1 ring-cyan-300/40 outline-none focus:ring-2 focus:ring-cyan-300" required />
        </label>
        <p v-if="errorMessage" class="rounded-lg bg-red-950/60 p-3 text-sm text-red-200">{{ errorMessage }}</p>
        <p v-if="successMessage" class="rounded-lg bg-emerald-950/60 p-3 text-sm text-emerald-200">{{ successMessage }}</p>
        <button class="rounded-lg bg-cyan-400 px-5 py-3 font-black text-blue-950 hover:bg-cyan-300 disabled:opacity-60" :disabled="isSaving">{{ isSaving ? 'Guardando…' : 'Guardar cambios' }}</button>
      </form>
    </section>
  </main>
</template>
