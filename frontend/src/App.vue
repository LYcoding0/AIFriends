<script setup>
import NavBar from "@/components/navbar/NavBar.vue";
import {onMounted} from "vue";
import api from "@/js/http/api.js";
import {useUserStore} from "@/stores/user.js";
import {useRoute, useRouter} from "vue-router";

const user = useUserStore();
const route = useRoute();
const router = useRouter();

/*
 * 组件挂载时的初始化函数
 * 负责获取用户信息并进行初始权限验证
 * @returns {Promise<void>} 无返回值的异步函数
 */
onMounted(async () => {
  try {
    const res = await api.post('/api/user/account/get_user_info/')
    const data = res.data
    if (data.result === 'success') {
      // 请求成功，更新用户信息到store
      user.setUserInfo(data)
    }
  } catch (err) {
    // 请求失败，输出错误信息
    console.log(err)
  } finally {
    // 标记用户信息拉取完成
    user.setHasPulledUserInfo(true)
    
    // 权限验证：如果当前路由需要登录且用户未登录，则重定向到登录页
    if (route.meta.needLogin && !user.isLogin()) {
      await router.replace({
        name: 'user-account-login-index'
      })
    }
  }
})
</script>

<template>
  <NavBar>
    <RouterView/>
  </NavBar>
</template>

<style scoped>

</style>
