<script setup>
import {computed, onBeforeUnmount, onMounted, ref, watch} from "vue";

const props = defineProps(['voices', 'curVoiceId'])
const myVoice = ref(props.curVoiceId != null ? String(props.curVoiceId) : '')
const isOpen = ref(false)
const dropdownRef = ref(null)

const currentVoice = computed(() => {
  return props.voices?.find(voice => String(voice.id) === myVoice.value) || null
})

watch(() => props.curVoiceId, newVal => {
  myVoice.value = newVal != null ? String(newVal) : ''
})

function toggleMenu() {
  if (!props.voices?.length) return
  isOpen.value = !isOpen.value
}

function selectVoice(voiceId) {
  myVoice.value = String(voiceId)
  isOpen.value = false
}

function handleClickOutside(event) {
  if (!dropdownRef.value?.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

defineExpose({
  myVoice,
})
</script>

<template>
  <fieldset class="editor-fieldset fieldset">
    <label class="editor-label label text-base">音色</label>

    <div ref="dropdownRef" class="voice-select relative">
      <button
          type="button"
          class="editor-select voice-select-trigger"
          :class="{'voice-select-trigger-open': isOpen}"
          @click="toggleMenu"
      >
        <span class="truncate">{{ currentVoice?.name || '请选择音色' }}</span>
        <span class="voice-select-chevron" :class="{'voice-select-chevron-open': isOpen}"></span>
      </button>

      <div v-if="isOpen" class="voice-select-menu">
        <button
            v-for="voice in voices"
            :key="voice.id"
            type="button"
            class="voice-select-option"
            :class="{'voice-select-option-active': String(voice.id) === myVoice}"
            @click="selectVoice(voice.id)"
        >
          <span class="truncate">{{ voice.name }}</span>
          <span v-if="String(voice.id) === myVoice" class="voice-select-check">已选</span>
        </button>
      </div>
    </div>
  </fieldset>
</template>

<style scoped>
.voice-select {
  width: 100%;
}

.voice-select-trigger {
  display: flex;
  width: 100%;
  min-height: 3rem;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  border-radius: 1rem;
  padding: 0.75rem 1rem;
  text-align: left;
  cursor: pointer;
}

.voice-select-trigger-open {
  border-color: rgba(194, 167, 133, 0.96) !important;
  box-shadow:
    0 0 0 3px rgba(222, 197, 164, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.96) !important;
}

.voice-select-chevron {
  flex: 0 0 auto;
  width: 0.65rem;
  height: 0.65rem;
  border-right: 2px solid #7a6f63;
  border-bottom: 2px solid #7a6f63;
  transform: rotate(45deg);
  transition: transform 160ms ease;
}

.voice-select-chevron-open {
  transform: rotate(-135deg);
}

.voice-select-menu {
  position: absolute;
  z-index: 40;
  top: calc(100% + 0.6rem);
  left: 0;
  right: 0;
  max-height: 16rem;
  overflow-y: auto;
  border: 1px solid rgba(214, 202, 186, 0.96);
  border-radius: 1.15rem;
  background: rgba(255, 251, 246, 0.98);
  box-shadow:
    0 26px 50px -30px rgba(15, 23, 42, 0.42),
    inset 0 1px 0 rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(16px);
}

.voice-select-option {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem 1rem;
  color: #172033;
  text-align: left;
  background: transparent;
  transition: background-color 140ms ease, color 140ms ease;
}

.voice-select-option:hover {
  background: rgba(242, 232, 219, 0.9);
}

.voice-select-option + .voice-select-option {
  border-top: 1px solid rgba(232, 224, 212, 0.88);
}

.voice-select-option-active {
  background: rgba(245, 235, 223, 0.92);
  color: #0f172a;
  font-weight: 700;
}

.voice-select-check {
  flex: 0 0 auto;
  border-radius: 999px;
  background: rgba(52, 66, 92, 0.12);
  padding: 0.18rem 0.55rem;
  font-size: 0.75rem;
  color: #34425c;
}
</style>
