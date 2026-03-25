<script setup>

import {computed, nextTick, ref, useTemplateRef} from "vue";
import api from "@/js/http/api.js";
import InputField from "@/components/character/chat_field/input_field/InputField.vue";
import CharacterPhotoField from "@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue";
import ChatHistory from "@/components/character/chat_field/chat_history/ChatHistory.vue";
import RemoveIcon from "@/components/character/icons/RemoveIcon.vue";

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')
const inputRef = useTemplateRef('input-ref')
const history = ref([])
const chatHistoryRef = useTemplateRef('chat-history-ref')
const isClearing = ref(false)
const isConfirmingClear = ref(false)
const isProcessing = ref(false)

async function showModal() {
  modalRef.value.showModal()

  await nextTick()
  inputRef.value.focus()
}

const modalStyle = computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})

function handlePushBackMessage(msg) {
  history.value.push(msg)
  chatHistoryRef.value.scrollToBottom()
}

function handleAddToLastMessage(delta) {
  if (!history.value.length) return
  history.value.at(-1).content += delta
  chatHistoryRef.value.scrollToBottom()
}

function handlePushFrontMessage(msg) {
  history.value.unshift(msg)
}

function handleProcessingChange(value) {
  isProcessing.value = value
}

function requestClearHistory() {
  if (!props.friend || isClearing.value) return
  isConfirmingClear.value = true
}

async function handleClearHistory() {
  if (!props.friend || isClearing.value) return

  isConfirmingClear.value = false
  isClearing.value = true
  try {
    inputRef.value?.interrupt?.()
    const res = await api.post('/api/friend/message/clear_history/', {
      friend_id: props.friend.id,
    })
    const data = res.data
    if (data.result === 'success') {
      history.value = []
      await nextTick()
      await chatHistoryRef.value?.resetHistory?.(true)
    } else {
      window.alert(data.result)
    }
  } catch (err) {
    console.log(err)
    window.alert(err?.response?.data?.result || '网络异常，请稍后重试')
  } finally {
    isClearing.value = false
  }
}

function handleClose() {
  isConfirmingClear.value = false
  inputRef.value?.close?.()
}

defineExpose({
  showModal
})
</script>

<template>
  <dialog ref="modal-ref" class="modal" @close="handleClose">
    <div class="modal-box relative h-150 w-90 overflow-hidden rounded-[2rem] border border-white/35 bg-slate-950 p-0 shadow-[0_40px_120px_-30px_rgba(15,23,42,0.85)]" :style="modalStyle">
      <div class="absolute inset-0 bg-gradient-to-b from-slate-950/30 via-slate-950/35 to-slate-950/88"></div>
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.18),transparent_42%)]"></div>
      <div class="absolute right-3 top-3 z-20 flex items-center gap-2">
        <button
          @click="requestClearHistory"
          :disabled="isClearing"
          class="btn btn-sm h-9 rounded-full border-0 bg-white/12 px-3 text-white backdrop-blur-md hover:bg-white/20 disabled:cursor-not-allowed disabled:bg-white/10 disabled:text-white/55"
        >
          <RemoveIcon/>
          {{ isClearing ? '清空中' : '清空' }}
        </button>
        <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost border-0 bg-white/12 text-white backdrop-blur-md hover:bg-white/20">
          &times;
        </button>
      </div>
      <div
        v-if="isConfirmingClear"
        class="absolute inset-0 z-30 flex items-center justify-center bg-slate-950/26 px-5 backdrop-blur-sm"
      >
        <div class="w-full max-w-[18rem] rounded-[1.75rem] border border-white/18 bg-slate-950/72 p-5 text-white shadow-[0_26px_70px_-28px_rgba(15,23,42,0.88)]">
          <div class="text-[11px] uppercase tracking-[0.28em] text-white/45">清空历史</div>
          <h3 class="mt-3 text-lg font-semibold">确认清空当前历史对话？</h3>
          <p class="mt-3 text-sm leading-6 text-white/68">
            这会删除当前角色与你的历史消息，并清空长期记忆。该操作不可恢复。
          </p>
          <div class="mt-5 flex items-center justify-end gap-3">
            <button
              @click="isConfirmingClear = false"
              class="btn btn-sm h-10 rounded-full border border-white/15 bg-white/10 px-4 text-white hover:bg-white/16"
            >
              取消
            </button>
            <button
              @click="handleClearHistory"
              :disabled="isClearing"
              class="btn btn-sm h-10 rounded-full border-0 bg-[linear-gradient(135deg,#3db6ff,#67d7ff)] px-4 text-slate-950 shadow-[0_16px_34px_-18px_rgba(79,181,255,0.85)] hover:brightness-105 disabled:cursor-not-allowed disabled:opacity-65"
            >
              {{ isClearing ? '清空中' : '确认清空' }}
            </button>
          </div>
        </div>
      </div>
      <div class="relative z-10 h-full">
        <ChatHistory ref="chat-history-ref" v-if="friend" :friendId="friend.id" :history="history"
                     :character="friend.character" @pushFrontMessage="handlePushFrontMessage"/>
        <InputField
          v-if="friend"
          :friendId="friend.id"
          ref="input-ref"
          @pushBackMessage="handlePushBackMessage"
          @addToLastMessage="handleAddToLastMessage"
          @processingChange="handleProcessingChange"
        />
        <CharacterPhotoField v-if="friend" :character="friend.character" :isProcessing="isProcessing"/>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

</style>
