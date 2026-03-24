<script setup>
import {ref, useTemplateRef} from "vue";
import {useUserStore} from "@/stores/user.js";
import UpdateIcon from "@/components/character/icons/UpdateIcon.vue";
import RemoveIcon from "@/components/character/icons/RemoveIcon.vue";
import api from "@/js/http/api.js";
import ChatField from "@/components/character/chat_field/ChatField.vue";
import {useRouter} from "vue-router";

const props = defineProps(['character', 'canEdit', 'canRemoveFriend', 'friendId'])
const emit = defineEmits(['remove'])
const user = useUserStore()
const router = useRouter()

async function handleRemoveCharacter() {
  try {
    const res = await api.post('/api/create/character/remove/', {
      character_id: props.character.id,
    })
    if (res.data.result === 'success') {
      emit('remove', props.character.id)
    }
  } catch (err) {
    console.log(err)
  }
}

async function handleRemoveFriend(){
  try{
    const res = await api.post('/api/friend/remove/', {
      friend_id: props.friendId,
    })
    if (res.data.result==='success'){
      emit('remove', props.friendId)
    }
  }catch (err){
    console.log(err)
  }
}

const chatFieldRef = useTemplateRef('chat-field-ref')
const friend = ref(null)

async function openChatField() {
  if (!user.isLogin()) {
    await router.push({
      name: 'user-account-login-index'
    })
  } else {
    try {
      const res = await api.post('/api/friend/get_or_create/', {
        character_id: props.character.id,
      })
      const data = res.data
      if (data.result === 'success') {
        friend.value = data.friend
        chatFieldRef.value.showModal()
      }
    } catch (err) {
      console.log(err)
    }
  }
}
</script>

<template>
  <div class="group w-60">
    <div class="relative isolate h-100 cursor-pointer overflow-hidden rounded-[2rem] border border-white/55 bg-slate-950 shadow-[0_28px_80px_-36px_rgba(15,23,42,0.75)] transition duration-500 hover:-translate-y-1 hover:shadow-[0_38px_90px_-34px_rgba(15,23,42,0.9)]"
         @click="openChatField">
      <img :src="character.background_image"
           class="absolute inset-0 h-full w-full object-cover transition duration-700 group-hover:scale-110"
           alt="">
      <div class="absolute inset-0 bg-gradient-to-b from-slate-950/10 via-slate-950/15 to-slate-950/90"></div>
      <div class="absolute inset-x-0 top-0 h-28 bg-gradient-to-b from-slate-950/55 to-transparent"></div>
      <div class="absolute inset-x-0 bottom-0 h-48 bg-gradient-to-t from-slate-950 via-slate-950/82 to-transparent"></div>

      <div class="absolute left-4 top-4 rounded-full border border-white/20 bg-white/10 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.28em] text-white/80 backdrop-blur-md">
        AI Friend
      </div>

        <div v-if="canEdit && character.author.user_id === user.id" class="absolute right-4 top-4 flex flex-col gap-2">
          <RouterLink @click.stop :to="{name:'update-character',params:{character_id:character.id}}"
                      class="btn btn-circle btn-sm border-0 bg-white/16 text-white shadow-none backdrop-blur-md hover:bg-white/24">
            <UpdateIcon/>
          </RouterLink>
          <button @click.stop="handleRemoveCharacter" class="btn btn-circle btn-sm border-0 bg-white/16 text-white shadow-none backdrop-blur-md hover:bg-white/24">
            <RemoveIcon/>
          </button>
        </div>

        <div v-if="canRemoveFriend" class="absolute right-4 top-4">
          <button @click.stop="handleRemoveFriend" class="btn btn-circle btn-sm border-0 bg-white/16 text-white shadow-none backdrop-blur-md hover:bg-white/24">
            <RemoveIcon/>
          </button>
        </div>

        <div class="absolute inset-x-4 bottom-4 rounded-[1.6rem] border border-white/15 bg-white/10 p-4 backdrop-blur-md">
          <div class="flex items-start gap-3">
            <div class="avatar shrink-0">
              <div class="w-16 rounded-full ring-2 ring-white/80">
            <img :src="character.photo" alt="">
              </div>
            </div>
            <div class="min-w-0 flex-1 pt-1">
              <div class="line-clamp-1 break-all text-lg font-bold text-white">
                {{ character.name }}
              </div>
              <div class="mt-1 text-[11px] uppercase tracking-[0.28em] text-white/55">Tap to chat</div>
            </div>
          </div>
          <div class="mt-4 line-clamp-4 break-all text-sm leading-6 text-white/78">
            {{ character.profile }}
          </div>
        </div>
    </div>

    <RouterLink :to="{name:'user-space-index',params:{user_id:character.author.user_id}}"
                class="mt-4 flex w-60 items-center justify-between gap-2 rounded-full border border-white/65 bg-white/65 px-3 py-2 shadow-[0_18px_30px_-26px_rgba(15,23,42,0.7)] backdrop-blur-md">
      <div class="avatar">
        <div class="w-7 rounded-full">
          <img :src="character.author.photo" alt="">
        </div>
      </div>

      <div class="line-clamp-1 flex-1 text-sm font-medium text-slate-700">
        {{ character.author.username }}
      </div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.24em] text-slate-400">Profile</div>
    </RouterLink>
    <ChatField ref="chat-field-ref" :friend="friend"/>
  </div>
</template>

<style scoped>

</style>
