<script setup>
import {ref, watch} from "vue";

const props = defineProps(['username'])
const myUsername = ref(props.username)

watch(() => props.username, newVal => {
  myUsername.value = newVal
})

/**
 * 暴露组件属性给父组件使用
 * 通过defineExpose将myPhoto响应式引用暴露出去，
 * 使得父组件可以通过模板引用访问该组件的头像数据
 *
 * @property {Ref} myUsername - 当前用户的头像图片数据的响应式引用
 */
defineExpose({
  myUsername,
})
</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base">用户名</label>
    <input v-model="myUsername"  type="text" class="input w-108">
  </fieldset>

</template>

<style scoped>

</style>