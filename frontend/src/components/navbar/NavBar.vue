<script setup>

import MenuIcon from "@/components/navbar/icons/MenuIcon.vue";
import HomepageIcon from "@/components/navbar/icons/HomepageIcon.vue";
import FriendIcon from "@/components/navbar/icons/FriendIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import {useUserStore} from "@/stores/user.js";
import UserMenu from "@/components/navbar/UserMenu.vue";
import {ref, watch} from "vue";
import {useRoute, useRouter} from "vue-router";

const user = useUserStore();
const searchQuery = ref('');
const route = useRoute()
const router = useRouter()

watch(() => route.query.q, newQ => {
  searchQuery.value = newQ || ''
})

function handleSearch() {
  router.push({
    name: 'homepage-index',
    query: {
      q: searchQuery.value.trim(),
    }
  })
}
</script>

<template>
  <div class="drawer min-h-screen lg:drawer-open">
    <input id="my-drawer-4" type="checkbox" class="drawer-toggle"/>
    <div class="drawer-content">
      <nav class="sticky top-0 z-40 px-3 pt-3 sm:px-4 lg:px-6">
        <div class="navbar rounded-[1.75rem] border border-white/60 bg-white/70 px-3 shadow-[0_20px_60px_-35px_rgba(15,23,42,0.45)] backdrop-blur-xl sm:px-5">
        <div class="navbar-start gap-2">
          <label for="my-drawer-4" aria-label="open sidebar"
                 class="btn btn-square btn-ghost rounded-full border border-transparent text-slate-700 hover:border-white/70 hover:bg-white/70">
            <MenuIcon/>
          </label>
          <div class="flex items-center gap-3 pl-1">
            <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-[linear-gradient(135deg,#ffb493,#73b8ff)] text-sm font-black text-white shadow-[0_12px_28px_-16px_rgba(15,23,42,0.85)]">
              AI
            </div>
            <div>
              <div class="text-lg font-black tracking-[-0.04em] text-slate-900 sm:text-xl">AIFriends</div>
              <div class="hidden text-[11px] uppercase tracking-[0.28em] text-slate-500 sm:block">Character Hub</div>
            </div>
          </div>
        </div>
        <div class="navbar-center hidden flex-1 px-4 md:flex">
          <form @submit.prevent="handleSearch"
                class="navbar-search-shell flex w-full max-w-3xl items-center gap-2 rounded-full border border-white/70 bg-white/75 p-2 shadow-[0_14px_30px_-24px_rgba(15,23,42,0.7)]">
            <input v-model="searchQuery" class="input navbar-search-input join-item rounded-l-full w-4/5" placeholder="搜索你感兴趣的内容"/>
            <button class="btn h-11 rounded-full border-0 bg-slate-900 px-5 text-white shadow-none hover:bg-slate-800">
              <SearchIcon/>
              搜索
            </button>
          </form>
        </div>
        <div class="navbar-end gap-2">
          <RouterLink v-if="user.isLogin()" :to="{name: 'create-index'}" active-class="btn-active"
                      class="btn rounded-full border border-white/70 bg-white/75 px-5 text-base text-slate-800 shadow-[0_16px_32px_-24px_rgba(15,23,42,0.75)] hover:border-white hover:bg-white">
            <CreateIcon/>
            创作
          </RouterLink>
          <!--          <RouterLink v-if="user.isLogin()" :to="{name: 'update-character',params:{character_id:1}}"-->
          <!--                      active-class="btn-active" class="btn btn-ghost text-base mr-6">-->
          <!--            <CreateIcon/>-->
          <!--            创作-->
          <!--          </RouterLink>-->
          <RouterLink v-if="user.setHasPulledUserInfo && !user.isLogin()" :to="{name: 'user-account-login-index'}"
                      active-class="btn-active"
                      class="btn rounded-full border border-transparent bg-transparent px-4 text-lg text-slate-700 hover:border-white/70 hover:bg-white/70">
            登录
          </RouterLink>
          <UserMenu v-else-if="user.isLogin()"/>
        </div>
        </div>
      </nav>

      <main class="px-3 pb-12 pt-5 sm:px-4 lg:px-6">
        <div class="page-shell mx-auto w-full max-w-[1440px]">
          <slot></slot>
        </div>
      </main>
    </div>

    <div class="drawer-side z-30 is-drawer-close:overflow-visible">
      <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay"></label>
      <div class="flex min-h-full flex-col items-start border-r border-white/55 bg-white/55 px-3 py-4 backdrop-blur-2xl is-drawer-close:w-20 is-drawer-open:w-64">
        <div class="mb-6 mt-1 hidden w-full px-3 is-drawer-open:block">
          <div class="glass-pill w-fit border-white/70 bg-white/65 text-slate-600">Explore</div>
        </div>
        <ul class="menu w-full grow gap-2">
          <li>
            <RouterLink :to="{name: 'homepage-index'}" active-class="drawer-link-active"
                        class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="首页">
              <HomepageIcon/>
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">首页</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink :to="{name: 'friend-index'}" active-class="drawer-link-active"
                        class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="好友">
              <FriendIcon/>
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">好友</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink :to="{name: 'create-index'}" active-class="drawer-link-active"
                        class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="创作">
              <CreateIcon/>
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">创作</span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.navbar-search-shell {
  color-scheme: only light;
  forced-color-adjust: none;
}

.navbar-search-input {
  height: 2.75rem;
  border: 0 !important;
  background: rgba(255, 255, 255, 0.96) !important;
  color: #0f172a !important;
  box-shadow: none !important;
  caret-color: #0f172a;
}

.navbar-search-input::placeholder {
  color: #64748b !important;
}

.navbar-search-input:focus,
.navbar-search-input:focus-visible {
  outline: none !important;
}
</style>
