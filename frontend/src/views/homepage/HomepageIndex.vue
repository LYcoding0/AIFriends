<script setup>
import {computed, nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch} from "vue";
import api from "@/js/http/api.js";
import Character from "@/components/character/Character.vue";
import {useRoute} from "vue-router";

const characters = ref([])
const isLoading = ref(false)
const hasCharacter = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const route = useRoute()
const activeQuery = computed(() => String(route.query.q || '').trim())
const sectionTitle = computed(() => activeQuery.value || 'AIFriends')

function checkSentinelVisible() { // 辅助函数，判断哨兵是否能被看见
  if (!sentinelRef.value) return false
  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore() {
  if (isLoading.value || !hasCharacter.value) return
  isLoading.value = true

  let newCharacters = []
  try {
    const res = await api.get('/api/homepage/index/', {
      params: {
        items_count: characters.value.length,
        search_query: route.query.q || ''
      }
    })
    const data = res.data
    if (data.result === 'success') {
      newCharacters = data.characters
    }
  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
    if (newCharacters.length === 0) {
      hasCharacter.value = false
    } else {
      characters.value.push(...newCharacters)
      await nextTick()

      if (checkSentinelVisible()) {
        await loadMore()
      }
    }
  }
}

let observer = null
onMounted(async () => {
  await loadMore()

  observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            loadMore()
          }
        })
      },
      {root: null, rootMargin: '2px', threshold: 0}
  )
  observer.observe(sentinelRef.value)
})

function reset() {
  characters.value = []
  isLoading.value = false
  hasCharacter.value = true
  loadMore()
}

watch(() => route.query.q, newQ => {
  reset()
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>
  <div class="page-shell flex flex-col gap-10 pb-6">
    <section class="hero-panel relative overflow-hidden">
      <div class="ambient-orb -left-10 top-8 h-36 w-36 bg-[rgba(255,143,107,0.24)]"></div>
      <div class="ambient-orb right-0 top-0 h-48 w-48 bg-[rgba(115,184,255,0.18)]"></div>
      <div class="soft-grid absolute inset-0 opacity-40"></div>
      <div class="relative z-10 flex flex-col gap-8 px-6 py-8 md:px-10 md:py-10">
        <div class="glass-pill w-fit">AIFriends</div>
        <div class="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div class="max-w-3xl">
            <h1 class="app-title text-4xl md:text-6xl">{{ sectionTitle }}</h1>
            <p class="mt-4 max-w-2xl text-sm leading-7 text-slate-600 md:text-base">
              探索更有氛围感的 AI 伙伴，浏览风格鲜明的角色卡片，在被某个角色吸引的瞬间，直接开启一场对话。
            </p>
          </div>
          <div class="grid gap-3 sm:grid-cols-2">
            <div class="surface-panel px-4 py-4">
              <div class="text-[11px] uppercase tracking-[0.28em] text-slate-500">模式</div>
              <div class="mt-2 text-lg font-semibold text-slate-900">{{ activeQuery ? '搜索结果' : '发现角色' }}</div>
            </div>
            <div class="surface-panel px-4 py-4">
              <div class="text-[11px] uppercase tracking-[0.28em] text-slate-500">操作</div>
              <div class="mt-2 text-lg font-semibold text-slate-900">开始对话</div>
            </div>
          </div>
        </div>
        <div class="flex flex-wrap gap-3">
          <div v-if="activeQuery" class="glass-pill border-white/80 bg-white/72 text-slate-700"># {{ activeQuery }}</div>
          <div class="glass-pill border-white/60 bg-white/50 text-slate-500">点击任意角色卡片即可开始对话</div>
        </div>
      </div>
    </section>

    <section class="surface-panel px-4 py-5 sm:px-6">
      <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-8 justify-items-center w-full">
      <Character
          v-for="character in characters"
          :key="character.id"
          :character="character"
      />
      </div>
      <div ref="sentinel-ref" class="h-2 mt-8 "></div>
      <div v-if="isLoading" class="mt-5 text-center text-sm font-medium tracking-[0.18em] text-slate-500 uppercase">加载中</div>
      <div v-else-if="!hasCharacter && characters.length" class="mt-5 text-center text-sm text-slate-500">没有更多角色了</div>
      <div v-else-if="!isLoading && !characters.length" class="mt-4 rounded-[1.25rem] border border-dashed border-slate-300/70 bg-white/50 px-6 py-10 text-center text-slate-500">
        当前筛选条件下还没有可显示的角色。
      </div>
      <!--
    <div v-if="isLoading" class="text-gray-500 mt-4">加载中...</div>
    <div v-else-if="!hasCharacter" class="text-gray-500 mt-4">没有更多角色了</div>
      -->
    </section>
  </div>
</template>

<style scoped>

</style>
