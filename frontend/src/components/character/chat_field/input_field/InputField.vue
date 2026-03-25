<script setup>

import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
import {onUnmounted, ref, useTemplateRef} from "vue";
import api from "@/js/http/api.js";
import streamApi from "@/js/http/streamApi.js";
import Microphone from "@/components/character/chat_field/input_field/Microphone.vue";

const inputRef = useTemplateRef('input-ref')
const message = ref('')
const props = defineProps(['friendId'])
const emit = defineEmits(['pushBackMessage', 'addToLastMessage', 'processingChange'])
const isProcessing = ref(false)
let processId = 0
const showMic = ref(false)
let currentController = null

let mediaSource = null;
let sourceBuffer = null;
let audioPlayer = new Audio();
let audioQueue = [];
let isUpdating = false;

const initAudioStream = () => {
  audioPlayer.pause();
  audioQueue = [];
  isUpdating = false;

  mediaSource = new MediaSource();
  audioPlayer.src = URL.createObjectURL(mediaSource);

  mediaSource.addEventListener('sourceopen', () => {
    try {
      sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');
      sourceBuffer.addEventListener('updateend', () => {
        isUpdating = false;
        processQueue();
      });
    } catch (e) {
      console.error("MSE AddSourceBuffer Error:", e);
    }
  });

  audioPlayer.play().catch(e => console.error("等待用户交互以播放音频", e));
};

const processQueue = () => {
  if (isUpdating || audioQueue.length === 0 || !sourceBuffer || sourceBuffer.updating) {
    return;
  }

  isUpdating = true;
  const chunk = audioQueue.shift();
  try {
    sourceBuffer.appendBuffer(chunk);
  } catch (e) {
    console.error("SourceBuffer Append Error:", e);
    isUpdating = false;
  }
};

const stopAudio = () => {
  audioPlayer.pause();
  audioQueue = [];
  isUpdating = false;

  if (mediaSource) {
    if (mediaSource.readyState === 'open') {
      try {
        mediaSource.endOfStream();
      } catch (e) {
      }
    }
    mediaSource = null;
  }

  if (audioPlayer.src) {
    URL.revokeObjectURL(audioPlayer.src);
    audioPlayer.src = '';
  }
};

const handleAudioChunk = (base64Data) => {
  try {
    const binaryString = atob(base64Data);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    audioQueue.push(bytes);
    processQueue();
  } catch (e) {
    console.error("Base64 Decode Error:", e);
  }
};

onUnmounted(() => {
  audioPlayer.pause();
  audioPlayer.src = '';
});

function focus() {
  inputRef.value.focus()
}

function setProcessing(value) {
  isProcessing.value = value
  emit('processingChange', value)
}

function stopCurrentRequest(notifyServer = false) {
  ++processId
  if (currentController) {
    currentController.abort()
    currentController = null
  }
  setProcessing(false)
  stopAudio()

  if (notifyServer && props.friendId) {
    api.post('/api/friend/message/interrupt/', {
      friend_id: props.friendId,
    }).catch(err => {
      console.log(err)
    })
  }
}

async function handleSend(event, audioMsg) {
  const content = audioMsg ? audioMsg.trim() : message.value.trim()

  if (!content) return

  if (isProcessing.value) {
    stopCurrentRequest()
  }

  setProcessing(true)
  initAudioStream()

  const curId = ++processId
  currentController = new AbortController()
  message.value = ''

  emit('pushBackMessage', {role: 'user', content: content, id: crypto.randomUUID()})
  emit('pushBackMessage', {role: 'ai', content: '', id: crypto.randomUUID()})

  try {
    await streamApi('/api/friend/message/chat/', {
      body: {
        friend_id: props.friendId,
        message: content,
      },
      signal: currentController.signal,
      onmessage(data, isDone) {
        if (curId !== processId) return

        if (isDone) {
          currentController = null
          setProcessing(false)
          return
        }

        if (data.content) {
          emit('addToLastMessage', data.content)
        }
        if (data.audio) {
          handleAudioChunk(data.audio)
        }
      },
      onerror(err) {
        console.log(err)
      },
      onclose() {
        if (curId === processId) {
          currentController = null
          setProcessing(false)
        }
      },
    })
  } catch (err) {
    if (err?.name !== 'AbortError') {
      console.log(err)
    }
  } finally {
    if (curId === processId) {
      currentController = null
      setProcessing(false)
    }
  }
}

function close() {
  stopCurrentRequest(true)
  showMic.value = false
}

function handleStop() {
  stopCurrentRequest(true)
}

function interrupt() {
  stopCurrentRequest(true)
}

function handleMicClick() {
  if (isProcessing.value) {
    interrupt()
  }
  showMic.value = true
}

defineExpose({
  focus,
  close,
  interrupt,
})
</script>

<template>
  <form v-if="!showMic" @submit.prevent="handleSend" class="absolute bottom-4 left-2 flex h-12 w-86 items-center">
    <input
      ref="input-ref"
      v-model="message"
      class="input h-full w-full rounded-2xl bg-black/30 pr-20 text-base text-white backdrop-blur-sm"
      type="text"
      placeholder="请输入信息..."
    />
    <div
      @click="handleSend"
      class="absolute right-2 flex h-8 w-8 items-center justify-center"
      :class="isProcessing ? 'cursor-pointer opacity-85' : 'cursor-pointer'"
    >
      <SendIcon/>
    </div>
    <div
      @click="handleMicClick"
      class="absolute right-10 flex h-8 w-8 items-center justify-center"
      :class="isProcessing ? 'cursor-pointer opacity-85' : 'cursor-pointer'"
    >
      <MicIcon/>
    </div>
  </form>
  <Microphone v-else @close="showMic = false" @send="handleSend" @stop="handleStop"/>
</template>

<style scoped>

</style>
