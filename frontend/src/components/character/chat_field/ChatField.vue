<script setup>

import {computed, nextTick, ref, useTemplateRef} from "vue";
import InputField from "@/components/character/chat_field/input_field/InputField.vue";
import CharacterPhotoField from "@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue";
import ChatHistory from "@/components/character/chat_field/chat_history/ChatHistory.vue";

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')
const inputRef = useTemplateRef('input-ref')
const history = ref([])
const chatHistoryRef = useTemplateRef('chat-history-ref')


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
  history.value.at(-1).content += delta
  chatHistoryRef.value.scrollToBottom()
}

function handlePushFrontMessage(msg) {
  history.value.unshift(msg)
}

function handleClose() {
  inputRef.value.close()
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
      <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost absolute right-3 top-3 z-20 border-0 bg-white/12 text-white backdrop-blur-md hover:bg-white/20">
        ×
      </button>
      <div class="relative z-10 h-full">
        <ChatHistory ref="chat-history-ref" v-if="friend" :friendId="friend.id" :history="history"
                     :character="friend.character" @pushFrontMessage="handlePushFrontMessage"/>
        <InputField v-if="friend" :friendId="friend.id" ref="input-ref" @pushBackMessage="handlePushBackMessage"
                    @addToLastMessage="handleAddToLastMessage"/>
        <CharacterPhotoField v-if="friend" :character="friend.character"/>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

</style>
