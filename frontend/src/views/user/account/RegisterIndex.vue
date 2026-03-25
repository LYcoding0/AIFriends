<script setup>
import {ref} from "vue";
import {useUserStore} from "@/stores/user.js";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";

const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');

const user = useUserStore();
const router = useRouter();

async function handleRegister() {
  errorMessage.value = '';
  if (!username.value.trim()) {
    errorMessage.value = '用户名不能为空'
  } else if (!password.value.trim()) {
    errorMessage.value = '密码不能为空'
  } else if (password.value.trim() !== confirmPassword.value.trim()) {
    errorMessage.value = '两次输入的密码不一致'
  } else {
    try {
      const res = await api.post('/api/user/account/register/', {
        username: username.value,
        password: password.value,
      })
      const data = res.data
      if (data.result === 'success') {
        user.setAccessToken(data.access)
        user.setUserInfo(data)
        await router.push({
          name: 'homepage-index',
        })
      } else {
        errorMessage.value = data.result
      }
    } catch (err) {
      console.log(err)
      errorMessage.value = '注册失败，请稍后重试'
    }
  }
}
</script>

<template>
  <div class="page-shell px-4 py-8 sm:px-6 lg:px-8">
    <section class="editor-card relative mx-auto w-full max-w-5xl overflow-hidden">
      <div class="ambient-orb -left-10 top-12 h-40 w-40 bg-[rgba(255,143,107,0.22)]"></div>
      <div class="ambient-orb right-0 top-0 h-48 w-48 bg-[rgba(115,184,255,0.18)]"></div>
      <div class="soft-grid absolute inset-0 opacity-40"></div>
      <div class="relative z-10 grid gap-8 px-6 py-8 lg:grid-cols-[1.1fr_0.9fr] lg:px-10 lg:py-10">
        <div class="flex flex-col justify-between gap-8">
          <div class="max-w-2xl">
            <div class="glass-pill w-fit">AIFriends</div>
            <h1 class="app-title mt-6 text-4xl md:text-5xl">创建你的账号</h1>
            <p class="mt-4 max-w-xl text-sm leading-7 text-slate-600 md:text-base">
              注册后保存你喜欢的角色，管理个人空间，并开始属于你的创作和对话体验。
            </p>
          </div>
          <div class="grid gap-3 sm:grid-cols-2">
            <div class="surface-panel px-4 py-4">
              <div class="text-[11px] uppercase tracking-[0.28em] text-slate-500">入口</div>
              <div class="mt-2 text-lg font-semibold text-slate-900">快速加入 AIFriends</div>
            </div>
            <div class="surface-panel px-4 py-4">
              <div class="text-[11px] uppercase tracking-[0.28em] text-slate-500">开始</div>
              <div class="mt-2 text-lg font-semibold text-slate-900">保存角色并继续创作</div>
            </div>
          </div>
        </div>

        <form
          @submit.prevent="handleRegister"
          class="rounded-[1.75rem] border border-white/80 bg-white/70 p-6 shadow-[0_26px_60px_-36px_rgba(15,23,42,0.42)] backdrop-blur-md"
        >
          <div class="glass-pill w-fit border-white/75 bg-white/72 text-slate-600">注册</div>
          <h2 class="editor-title mt-5 text-2xl">开启你的创作空间</h2>
          <p class="mt-2 text-sm leading-6 text-slate-500">
            设置用户名和密码后，就可以创建角色并进入个人空间。
          </p>

          <div class="editor-fieldset mt-6 space-y-4">
            <div>
              <label class="editor-label mb-2 block">用户名</label>
              <input
                v-model="username"
                type="text"
                autocomplete="username"
                class="editor-input input w-full"
                placeholder="请输入用户名"
              />
            </div>

            <div>
              <label class="editor-label mb-2 block">密码</label>
              <input
                v-model="password"
                type="password"
                autocomplete="new-password"
                class="editor-input input w-full"
                placeholder="请输入密码"
              />
            </div>

            <div>
              <label class="editor-label mb-2 block">确认密码</label>
              <input
                v-model="confirmPassword"
                type="password"
                autocomplete="new-password"
                class="editor-input input w-full"
                placeholder="请再次输入密码"
              />
            </div>
          </div>

          <p
            v-if="errorMessage"
            class="mt-4 rounded-2xl border border-red-200/80 bg-red-50/80 px-4 py-3 text-sm text-red-600"
          >
            {{ errorMessage }}
          </p>

          <button class="editor-submit btn mt-6 h-12 w-full rounded-2xl border-0 text-base font-semibold">
            注册
          </button>

          <div class="mt-5 flex items-center justify-between gap-4 text-sm text-slate-500">
            <span>已经有账号了？</span>
            <RouterLink
              :to="{name: 'user-account-login-index'}"
              class="rounded-full border border-white/80 bg-white/72 px-4 py-2 font-medium text-slate-700 transition hover:bg-white"
            >
              去登录
            </RouterLink>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<style scoped>

</style>