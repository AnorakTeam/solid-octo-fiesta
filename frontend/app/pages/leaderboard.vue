<script setup
    lang="ts">    const api = useRuntimeConfig().public.apiBase; const rows: any = await $fetch(`${api}/game/leaderboard`)</script>
<template>
    <main class="max-w-xl mx-auto p-8">
        <h1 class="text-3xl mb-6">Ranking</h1>
        <div v-for="row in rows" :key="row.position" class="flex justify-between border-b border-blue-400 py-3">
            <span>#{{ row.position }} {{ row.nickname }}</span><strong>{{ row.score }}</strong></div>
    </main>
</template>
