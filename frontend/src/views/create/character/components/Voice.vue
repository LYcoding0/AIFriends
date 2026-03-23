<script setup>
import {ref, watch} from "vue";

const props = defineProps(['voices', 'curVoiceId'])
const myVoice = ref(props.curVoiceId)

watch(() => props.curVoiceId, newVal => {
  myVoice.value = newVal
})

defineExpose({
  myVoice,
})
</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base">音色</label>
    <select class="select">
      <option v-for="voice in voices" :value="voice.id" :id="voice.id">{{ voice.name}}</option>
    </select>
  </fieldset>
</template>

<style scoped>

</style>