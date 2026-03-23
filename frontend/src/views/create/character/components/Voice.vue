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
  <fieldset class="fieldset">
    <label class="label text-base">音色</label>
    <select v-model="myVoice" class="select">
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
