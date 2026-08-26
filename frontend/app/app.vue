<script setup lang="ts">
const globalNumberSpawner = ref<{
  spawn: (options?: { x?: number; y?: number }) => void
} | null>(null)
const route = useRoute()
const showFloatingLogo = computed(() => route.meta.hideFloatingLogo !== true)

function handleGlobalClick(event: MouseEvent) {
  globalNumberSpawner.value?.spawn({
    x: event.clientX,
    y: event.clientY,
  })
}

onMounted(() => window.addEventListener('click', handleGlobalClick))
onBeforeUnmount(() => window.removeEventListener('click', handleGlobalClick))
</script>

<template>
  <FloatingBubbleBackground />
  <FloatingSiteLogo v-if="showFloatingLogo" />
  <div class="relative z-10">
    <NuxtPage />
  </div>
  <FloatingNumberSpawner ref="globalNumberSpawner" text="+0" />
</template>
