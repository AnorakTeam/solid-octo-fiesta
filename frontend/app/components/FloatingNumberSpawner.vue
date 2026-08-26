<script setup lang="ts">
import { motion } from 'motion-v'

interface Props {
  text?: string
  duration?: number
  rise?: number
  spread?: number
  fontSize?: number
  color?: string
  opacity?: number
}

interface SpawnOptions {
  x?: number
  y?: number
  text?: string
  duration?: number
  rise?: number
  spread?: number
  fontSize?: number
  color?: string
  opacity?: number
}

interface FloatingNumber {
  id: number
  x: number
  y: number
  text: string
  duration: number
  rise: number
  drift: number
  fontSize: number
  color: string
  opacity: number
}

const props = withDefaults(defineProps<Props>(), {
  text: '+1',
  duration: 1_200,
  rise: 90,
  spread: 18,
  fontSize: 28,
  color: '#caf0f8',
  opacity: 0.65,
})

const floatingNumbers = ref<FloatingNumber[]>([])
const despawnTimers = new Map<number, ReturnType<typeof setTimeout>>()
let nextId = 0

function despawn(id: number) {
  floatingNumbers.value = floatingNumbers.value.filter(number => number.id !== id)
  despawnTimers.delete(id)
}

function spawn(options: SpawnOptions = {}) {
  const duration = Math.max(100, options.duration ?? props.duration)
  const spread = Math.max(0, options.spread ?? props.spread)
  const id = nextId++

  floatingNumbers.value.push({
    id,
    x: options.x ?? window.innerWidth / 2,
    y: options.y ?? window.innerHeight / 2,
    text: options.text ?? props.text,
    duration,
    rise: options.rise ?? props.rise,
    drift: (Math.random() * 2 - 1) * spread,
    fontSize: options.fontSize ?? props.fontSize,
    color: options.color ?? props.color,
    opacity: Math.min(1, Math.max(0, options.opacity ?? props.opacity)),
  })

  despawnTimers.set(id, setTimeout(() => despawn(id), duration + 100))
}

onBeforeUnmount(() => {
  despawnTimers.forEach(timer => clearTimeout(timer))
  despawnTimers.clear()
})

defineExpose({ spawn })
</script>

<template>
  <Teleport to="body">
    <motion.span
      v-for="number in floatingNumbers"
      :key="number.id"
      class="pointer-events-none fixed z-50 select-none font-black drop-shadow-[0_0_10px_rgba(0,180,216,0.9)]"
      :style="{
        left: `${number.x}px`,
        top: `${number.y}px`,
        color: number.color,
        fontSize: `${number.fontSize}px`,
      }"
      :initial="{ opacity: 0, x: 0, y: 0, scale: 0.8, filter: 'blur(1px)' }"
      :animate="{
        opacity: [0, number.opacity, number.opacity, 0],
        x: number.drift,
        y: -number.rise,
        scale: [0.8, 1.08, 1],
        filter: ['blur(1px)', 'blur(0px)', 'blur(0px)'],
      }"
      :transition="{
        duration: number.duration / 1000,
        times: [0, 0.1, 0.82, 1],
        ease: 'easeOut',
      }"
      aria-hidden="true"
    >
      {{ number.text }}
    </motion.span>
  </Teleport>
</template>
