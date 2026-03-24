<script setup>
import {ref, watch} from "vue";

const props = defineProps(['name'])
const myName = ref(props.name)

watch(() => props.name, newVal => {
  myName.value = newVal
})

defineExpose({
  myName,
})
</script>

<template>
  <fieldset class="editor-fieldset fieldset">
    <label class="editor-label label text-base">名字</label>
    <input v-model="myName" type="text" class="editor-input input w-108">
  </fieldset>
</template>

<style scoped>

</style>
