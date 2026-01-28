<script setup>
import {useRoute, useRouter} from "vue-router";

const route = useRoute();   // 获取路由参数信息
const router = useRouter();  // 获取路由实例，用于执行路由跳转操作
</script>

<template>
个人空间 user_id: {{route.params.user_id}}
</template>

<style scoped>

</style>