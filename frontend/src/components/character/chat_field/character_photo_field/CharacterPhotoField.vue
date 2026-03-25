<script setup>
defineProps(['character', 'isProcessing'])
</script>

<template>
  <div class="absolute left-2 right-24 top-6 z-20 flex items-center gap-3">
    <div class="flex h-10 max-w-[10rem] items-center gap-2 rounded-full bg-black/50 px-2">
      <div class="avatar">
        <div class="w-8 rounded-full">
          <img :src="character.photo" alt="">
        </div>
      </div>
      <div class="line-clamp-1 break-all text-sm text-white">
        {{ character.name }}
      </div>
    </div>

    <div
      v-if="isProcessing"
      class="max-w-[9.5rem] rounded-full bg-white/12 px-3 py-1.5 text-xs text-white/85 backdrop-blur-md"
    >
      对方正在输入中...
    </div>
  </div>
</template>

<style scoped>

</style>
