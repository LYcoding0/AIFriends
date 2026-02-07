<script setup>
import {ref, watch} from "vue";

const props = defineProps(['profile'])
const myProfile = ref(props.profile)

/**
 * 监听props.profile的变化并同步更新myProfile
 *
 * @param {Function} getter - 返回要监听的响应式数据的函数
 * @param {Function} callback - 当监听的数据发生变化时执行的回调函数
 *   @param {*} newVal - 新的属性值
 *   @param {*} oldVal - 旧的属性值
 */
watch(() => props.profile, newVal => {
  // 同步更新内部响应式变量
  myProfile.value = newVal
})

/**
 * 暴露组件属性给父组件使用
 * 通过defineExpose将myPhoto响应式引用暴露出去，
 * 使得父组件可以通过模板引用访问该组件的头像数据
 *
 * @property {Ref} myProfile - 当前用户的头像图片数据的响应式引用
 */
defineExpose({
  myProfile,
})
</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base">简介</label>
    <textarea v-model="myProfile" rows="6" class="textarea w-108"></textarea>
  </fieldset>
</template>

<style scoped>

</style>