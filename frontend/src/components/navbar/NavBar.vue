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
                class="navbar-search-shell flex w-full max-w-3xl items-center gap-3 rounded-full border border-white/70 p-2">
            <input v-model="searchQuery" class="input navbar-search-input join-item rounded-l-full w-4/5" placeholder="搜索你感兴趣的内容"/>
            <button class="btn navbar-search-button h-11 rounded-full border-0 px-5 text-white shadow-none">
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
  align-items: center;
  gap: 0.75rem;
  background: linear-gradient(180deg, rgba(251, 247, 242, 0.92), rgba(244, 236, 226, 0.88));
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.88),
    0 14px 30px -24px rgba(15, 23, 42, 0.42);
}

.navbar-search-input {
  height: 2.75rem;
  min-width: 18rem;
  flex: 1 1 auto;
  border: 1px solid rgba(221, 209, 191, 0.95) !important;
  border-radius: 999px !important;
  background: linear-gradient(180deg, #fffdfa, #faf3ec) !important;
  color: #0f172a !important;
  padding: 0 1.25rem !important;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.92),
    0 2px 6px rgba(15, 23, 42, 0.04) !important;
  caret-color: #0f172a;
  appearance: none;
  opacity: 1;
  -webkit-text-fill-color: #0f172a;
}

.navbar-search-input::placeholder {
  color: #7a6f63 !important;
  opacity: 1;
}

.navbar-search-input:focus,
.navbar-search-input:focus-visible {
  outline: none !important;
  border-color: rgba(180, 159, 132, 0.92) !important;
  box-shadow:
    0 0 0 3px rgba(210, 187, 156, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.92) !important;
}

.navbar-search-input::-webkit-search-decoration,
.navbar-search-input::-webkit-search-cancel-button,
.navbar-search-input::-webkit-search-results-button,
.navbar-search-input::-webkit-search-results-decoration {
  appearance: none;
}

.navbar-search-button {
  background: linear-gradient(135deg, #33425c 0%, #1f293f 100%) !important;
  border: 1px solid rgba(255, 255, 255, 0.24) !important;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.12),
    0 14px 24px -18px rgba(31, 41, 63, 0.68) !important;
}

.navbar-search-button:hover {
  background: linear-gradient(135deg, #3b4c69 0%, #24304a 100%) !important;
}
</style>
