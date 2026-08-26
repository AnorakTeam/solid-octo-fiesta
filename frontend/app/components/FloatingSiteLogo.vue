<script setup lang="ts">
import { motion } from 'motion-v'
import logoUrl from '~/assets/images/solid-octo-fiesta-logo.png'

interface Props {
  floatDistance?: number
  duration?: number
  alt?: string
}

const props = withDefaults(defineProps<Props>(), {
  floatDistance: 12,
  duration: 6.8,
  alt: 'Solid Octo Fiesta',
})

const floatingAnimation = computed(() => ({
  y: [0, -props.floatDistance, 3, -props.floatDistance * 0.55, 0],
  rotateX: [0, 5, -3, 4, 0],
  rotateY: [-5, 6, -4, 3, -5],
  rotateZ: [-1.2, 1, -0.7, 0.8, -1.2],
  scale: [1, 1.015, 0.995, 1.01, 1],
}))
</script>

<template>
  <div
    class="pointer-events-none fixed inset-x-0 top-1 z-40 hidden justify-center [perspective:900px] sm:flex"
  >
    <motion.div
      :initial="{ opacity: 0, y: -16, scale: 0.9 }"
      :animate="{ opacity: 1, y: 0, scale: 1 }"
      :transition="{ duration: 0.55, ease: 'easeOut' }"
    >
      <motion.div
        class="relative w-[min(72vw,18rem)] will-change-transform sm:w-80 lg:w-[22rem] [transform-style:preserve-3d]"
        :animate="floatingAnimation"
        :transition="{
          duration: props.duration,
          repeat: Infinity,
          ease: 'easeInOut',
          times: [0, 0.26, 0.52, 0.78, 1],
        }"
      >
        <div
          class="absolute inset-x-[12%] inset-y-[28%] -z-10 rounded-full bg-cyan-300/20 blur-2xl"
          aria-hidden="true"
        />
        <img
          :src="logoUrl"
          :alt="props.alt"
          class="block h-auto w-full select-none drop-shadow-[0_8px_12px_rgba(0,0,0,0.45)]"
          draggable="false"
        >
      </motion.div>
    </motion.div>
  </div>
</template>
