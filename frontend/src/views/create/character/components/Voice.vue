<script setup>
import {ref, watch} from "vue";

const props = defineProps(['voices', 'curVoiceId'])
const myVoice = ref(props.curVoiceId != null ? String(props.curVoiceId) : '')

watch(() => props.curVoiceId, newVal => {
  myVoice.value = newVal != null ? String(newVal) : ''
})

defineExpose({
  myVoice,
})
</script>

<template>
  <fieldset class="editor-fieldset fieldset">
    <label class="editor-label label text-base">音色</label>
    <select v-model="myVoice" class="editor-select select">
      <option
          v-for="voice in voices"
          :key="voice.id"
          :id="voice.id"
          :value="String(voice.id)"
      >{{ voice.name }}
      </option>
    </select>
  </fieldset>
</template>

<style scoped>

</style>
