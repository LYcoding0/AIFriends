<script setup>
import {useUserStore} from "@/stores/user.js";
import UserSpaceIcon from "@/components/navbar/icons/UserSpaceIcon.vue";
import UserLogoutIcon from "@/components/navbar/icons/UserLogoutIcon.vue";
import UserProfileIcon from "@/components/navbar/icons/UserProfileIcon.vue";
import VoiceIcon from "@/components/navbar/icons/VoiceIcon.vue";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";

const user = useUserStore()
const router = useRouter()

function closeMenu() {
  const element = document.activeElement
  if (element && element instanceof HTMLElement) element.blur()
}

async function handleLogout() {
  try {
    const res = await api.post('/api/user/account/logout/')
    if (res.data.result === 'success') {
      user.logout()
      await router.push({
        name: 'homepage-index'
      })
    }
  } catch (err) {
    console.log(err)
  }
}

</script>

<template>
  <div class="dropdown dropdown-end">
    <div tabindex="0" role="button" class="user-menu-trigger avatar btn btn-circle mr-6 h-8 w-8 border border-white/75 bg-white/82 text-slate-800 shadow-[0_16px_30px_-24px_rgba(15,23,42,0.8)]">
      <div class="w-8 rounded-full">
        <img :src="user.photo" alt="">
      </div>
    </div>
    <ul tabindex="-1" class="user-menu-panel dropdown-content menu z-1 w-56 rounded-[1.5rem] border border-white/75 bg-white/96 p-2 text-slate-800 shadow-[0_30px_70px_-32px_rgba(15,23,42,0.85)] backdrop-blur-xl">
      <li>
        <RouterLink @click="closeMenu" :to="{name: 'user-space-index', params: {user_id: user.id}}" class="rounded-2xl px-3 py-3 text-slate-900 hover:bg-slate-100/90">
          <div class="avatar">
            <div class="w-10 rounded-full">
              <img :src="user.photo" alt="">
            </div>
          </div>
          <span class="text-base font-bold line-clamp-1 break-all">{{ user.username }}</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name: 'user-space-index', params: {user_id: user.id}}"
                    class="rounded-2xl py-3 text-sm font-bold text-slate-700 hover:bg-slate-100/90">
          <UserSpaceIcon/>
          个人空间
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name: 'user-profile-index'}" class="rounded-2xl py-3 text-sm font-bold text-slate-700 hover:bg-slate-100/90">
          <UserProfileIcon/>
          编辑资料
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name: 'user-voice-studio-index'}" class="rounded-2xl py-3 text-sm font-bold text-slate-700 hover:bg-slate-100/90">
          <VoiceIcon/>
          创建音色
        </RouterLink>
        <hr class="mx-4 rounded-none">
      </li>
      <li>
        <a @click="handleLogout" class="rounded-2xl py-3 text-sm font-bold text-slate-700 hover:bg-slate-100/90">
          <UserLogoutIcon/>
          退出登录
        </a>
      </li>
    </ul>

  </div>
</template>

<style scoped>
.user-menu-trigger,
.user-menu-panel {
  color-scheme: only light;
  forced-color-adjust: none;
}

.user-menu-panel :deep(svg),
.user-menu-trigger :deep(svg) {
  color: currentColor;
}
</style>
