<script setup>
import {computed, onBeforeUnmount, onMounted, ref, watch} from "vue";

const props = defineProps([
  'customVoices',
  'curVoiceId',
  'loadingCustomVoices',
])
const emit = defineEmits([
  'select-voice',
  'refresh-custom-voices',
])

const myVoice = ref(props.curVoiceId != null ? String(props.curVoiceId) : '')
const isOpen = ref(false)
const dropdownRef = ref(null)
const searchQuery = ref('')

const currentVoice = computed(() => {
  return props.customVoices?.find(voice => String(voice.id) === myVoice.value) || null
})

const filteredCustomVoices = computed(() => {
  const list = props.customVoices || []
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return list
  return list.filter(v => String(v?.name || '').toLowerCase().includes(q))
})

watch(() => props.curVoiceId, newVal => {
  myVoice.value = newVal != null ? String(newVal) : ''
})

watch(isOpen, open => {
  if (!open) searchQuery.value = ''
})

function toggleMenu() {
  if (!props.customVoices?.length) return
  isOpen.value = !isOpen.value
}

function selectVoice(voiceId) {
  myVoice.value = String(voiceId)
  isOpen.value = false
  emit('select-voice', {voice_id: voiceId})
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
</script>

<template>
  <fieldset class="editor-fieldset fieldset">
    <label class="editor-label label text-base">自定义音色</label>

    <div class="voice-list-panel mt-2">
      <div class="flex items-center justify-between mb-2">
        <p class="text-xs opacity-70">仅显示当前账号创建的音色</p>
        <button
            type="button"
            class="voice-mini-icon-btn"
            :disabled="loadingCustomVoices"
            @click="emit('refresh-custom-voices')"
            aria-label="刷新列表"
            title="刷新列表"
        >
          <svg class="voice-refresh-icon" :class="{'voice-refresh-icon-spinning': loadingCustomVoices}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 12A8 8 0 1 1 17.66 6.34" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
            <path d="M20 4V8H16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
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
          <div class="voice-select-search">
            <input
                v-model="searchQuery"
                type="text"
                class="voice-search-input"
                placeholder="搜索音色"
            >
          </div>
          <button
              v-for="voice in filteredCustomVoices"
              :key="voice.id"
              type="button"
              class="voice-select-option"
              :class="{'voice-select-option-active': String(voice.id) === myVoice}"
              @click="selectVoice(voice.id)"
          >
            <span class="truncate">{{ voice.name }}</span>
            <span v-if="String(voice.id) === myVoice" class="voice-select-check">已选</span>
          </button>

          <p v-if="!filteredCustomVoices.length" class="voice-empty">无匹配结果</p>
        </div>
      </div>

      <p v-if="!customVoices?.length && !loadingCustomVoices" class="text-xs opacity-60 mt-2">还没有创建自定义音色。</p>
    </div>

    <p class="text-xs opacity-60 mt-2">这里只用于选择你已创建的自定义音色，创建入口已迁移到右上角头像菜单。</p>
  </fieldset>
</template>

<style scoped>
.voice-list-panel {
  border: 1px solid rgba(219, 205, 188, 0.95);
  border-radius: 0.95rem;
  background: rgba(255, 252, 248, 0.9);
  padding: 0.5rem;
}

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

.voice-select-search {
  padding: 0.7rem 0.85rem 0.5rem;
  border-bottom: 1px solid rgba(232, 224, 212, 0.88);
}

.voice-search-input {
  width: 100%;
  border: 1px solid rgba(221, 209, 191, 0.95);
  border-radius: 0.85rem;
  background: linear-gradient(180deg, #fffdfa, #faf3ec);
  padding: 0.55rem 0.8rem;
  font-size: 0.85rem;
  color: #0f172a;
}

.voice-search-input::placeholder {
  color: #c2b9ad;
  opacity: 1;
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

.voice-empty {
  padding: 0.8rem 1rem;
  font-size: 0.8rem;
  color: #a49a90;
}

.voice-mini-icon-btn {
  width: 2rem;
  height: 2rem;
  border: 1px solid rgba(208, 190, 169, 0.75);
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #76695c;
  background: rgba(255, 255, 255, 0.7);
  cursor: pointer;
}

.voice-mini-icon-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.voice-refresh-icon {
  width: 1rem;
  height: 1rem;
}

.voice-refresh-icon-spinning {
  animation: voice-spin 0.9s linear infinite;
}

@keyframes voice-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

</style>
