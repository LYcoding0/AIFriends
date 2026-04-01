<script setup>
import {onMounted, ref} from "vue";
import api from "@/js/http/api.js";

const errorMessage = ref('')
const successMessage = ref('')
const customVoices = ref([])
const loadingCustomVoices = ref(false)
const creatingCustomVoice = ref(false)
const deletingVoiceId = ref(null)
const customName = ref('')
const customAudioUrl = ref('')
const deleteTarget = ref(null)

async function loadCustomVoices() {
  loadingCustomVoices.value = true
  try {
    const res = await api.get('/api/create/character/voice/custom/list/', {})
    const data = res.data
    if (data.result === 'success') {
      customVoices.value = data.voices || []
    } else {
      errorMessage.value = data.result
    }
  } catch (err) {
    console.log(err)
    errorMessage.value = err?.response?.data?.result || '网络异常，请稍后重试'
  } finally {
    loadingCustomVoices.value = false
  }
}

async function handleCreateCustomVoice() {
  if (creatingCustomVoice.value) return

  const name = customName.value.trim()
  const voiceUrl = customAudioUrl.value.trim()
  errorMessage.value = ''
  successMessage.value = ''

  if (!name) {
    errorMessage.value = '请输入音色名称'
    return
  }
  if (!voiceUrl) {
    errorMessage.value = '请输入音频地址'
    return
  }

  creatingCustomVoice.value = true
  try {
    const res = await api.post('/api/create/character/voice/custom/create/', {
      name,
      voice_url: voiceUrl,
    })
    const data = res.data
    if (data.result === 'success') {
      customName.value = ''
      customAudioUrl.value = ''
      successMessage.value = '创建成功，可在角色页选择该音色'
      await loadCustomVoices()
    } else {
      errorMessage.value = data.result
    }
  } catch (err) {
    console.log(err)
    errorMessage.value = err?.response?.data?.result || '网络异常，请稍后重试'
  } finally {
    creatingCustomVoice.value = false
  }
}

function openDeleteModal(voice) {
  if (!voice?.can_delete || deletingVoiceId.value) return
  deleteTarget.value = voice
}

function closeDeleteModal() {
  deleteTarget.value = null
}

async function confirmDeleteVoice() {
  if (!deleteTarget.value?.id || deletingVoiceId.value) return

  deletingVoiceId.value = deleteTarget.value.id
  errorMessage.value = ''
  successMessage.value = ''
  try {
    const res = await api.post('/api/create/character/voice/custom/delete/', {
      voice_id: deleteTarget.value.id,
    })
    const data = res.data
    if (data.result === 'success') {
      deleteTarget.value = null
      successMessage.value = '删除成功'
      await loadCustomVoices()
    } else {
      errorMessage.value = data.result
    }
  } catch (err) {
    console.log(err)
    errorMessage.value = err?.response?.data?.result || '网络异常，请稍后重试'
  } finally {
    deletingVoiceId.value = null
  }
}

onMounted(async () => {
  await loadCustomVoices()
})
</script>

<template>
  <div class="voice-studio-shell">
    <fieldset class="editor-fieldset fieldset voice-studio mt-6">
      <label class="editor-label label text-base">创建音色</label>

      <div class="voice-list-panel mt-1">
        <div class="flex items-center justify-between mb-2">
          <p class="voice-soft-hint text-xs">仅显示当前账号创建的音色</p>
          <button
              type="button"
              class="voice-mini-icon-btn"
              :disabled="loadingCustomVoices"
              @click="loadCustomVoices"
              aria-label="刷新列表"
              title="刷新列表"
          >
            <svg class="voice-refresh-icon" :class="{'voice-refresh-icon-spinning': loadingCustomVoices}"
                 viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 12A8 8 0 1 1 17.66 6.34" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
              <path d="M20 4V8H16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
                    stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <div
            v-for="voice in customVoices"
            :key="voice.id"
            class="voice-list-item"
        >
          <span class="truncate">{{ voice.name }}</span>
          <span
              class="voice-delete-link"
              :class="{'voice-delete-link-disabled': !voice.can_delete || deletingVoiceId}"
              @click="openDeleteModal(voice)"
          >删除</span>
        </div>
        <p v-if="!customVoices?.length && !loadingCustomVoices" class="voice-soft-hint text-xs">还没有创建自定义音色。</p>
      </div>

      <p class="voice-soft-hint text-xs mt-2">音色名称支持中文；系统会自动生成远端标识（用户ID+随机串）。</p>

      <input
          v-model="customName"
          type="text"
          class="editor-input custom-voice-input mt-2 text-xs"
          placeholder="例如：我的专属音色"
      >

      <input
          v-model="customAudioUrl"
          type="text"
          class="editor-input custom-voice-input mt-2"
          placeholder="请输入可访问的音频 URL"
      >

      <div class="mt-2">
        <button
            type="button"
            class="voice-action-btn"
            :disabled="creatingCustomVoice"
            @click="handleCreateCustomVoice"
        >
          {{ creatingCustomVoice ? '创建中...' : '创建自定义音色' }}
        </button>
      </div>

      <p v-if="errorMessage" class="text-sm text-red-500 mt-2">{{ errorMessage }}</p>
      <p v-else-if="successMessage" class="text-sm text-emerald-700 mt-2">{{ successMessage }}</p>
    </fieldset>

    <!-- Center within this studio card only -->
    <div v-if="deleteTarget" class="voice-confirm-mask" role="dialog" aria-modal="true" @click.self="closeDeleteModal">
      <div class="voice-confirm-card" @click.stop>
        <h4 class="voice-confirm-title">确认删除音色</h4>
        <p class="text-sm opacity-75 mt-2">你将删除「{{ deleteTarget.name }}」，该操作不可撤销。</p>
        <div class="voice-confirm-actions mt-3">
          <button type="button" class="voice-action-btn voice-action-btn-muted" @click="closeDeleteModal">取消</button>
          <button type="button" class="voice-action-btn" :disabled="!!deletingVoiceId" @click="confirmDeleteVoice">
            {{ deletingVoiceId ? '删除中...' : '确认删除' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.voice-studio {
  border-top: 1px solid rgba(216, 203, 186, 0.78);
  padding-top: 0.75rem;
}

.voice-list-panel {
  border: 1px solid rgba(219, 205, 188, 0.95);
  border-radius: 0.95rem;
  background: rgba(255, 252, 248, 0.9);
  padding: 0.5rem;
  max-height: 13rem;
  overflow-y: auto;
}

.voice-list-item {
  width: 100%;
  border: 1px solid transparent;
  border-radius: 0.7rem;
  padding: 0.52rem 0.62rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.6rem;
  color: #172033;
}

.voice-delete-link {
  font-size: 0.74rem;
  color: #c84a4a;
  cursor: pointer;
}

.voice-delete-link-disabled {
  color: #a49a90;
  cursor: not-allowed;
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

.voice-action-btn {
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 0.8rem;
  padding: 0.45rem 0.86rem;
  font-size: 0.8rem;
  font-weight: 700;
  background: linear-gradient(135deg, #34425c 0%, #212d44 100%);
  color: #fff8f2;
  cursor: pointer;
}

.voice-action-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.voice-action-btn-muted {
  background: linear-gradient(135deg, #f4ece1 0%, #eadfd1 100%);
  color: #5f564b;
  border: 1px solid rgba(208, 190, 169, 0.8);
}

.custom-voice-input {
  border-radius: 0.75rem;
  min-height: 2.6rem;
  padding: 0.45rem 0.72rem;
  background: linear-gradient(180deg, #fffefc, #fdf8f2) !important;
}

:deep(.custom-voice-input::placeholder),
:deep(.custom-voice-input::-webkit-input-placeholder),
:deep(.custom-voice-input::-moz-placeholder),
:deep(.custom-voice-input:-ms-input-placeholder),
:deep(.custom-voice-input::-ms-input-placeholder) {
  color: #b8aea2 !important;
}

.voice-soft-hint {
  color: #b8aea2;
}

.custom-voice-input:focus,
.custom-voice-input:focus-visible {
  border-color: rgba(198, 173, 142, 0.95) !important;
  box-shadow: 0 0 0 3px rgba(224, 201, 171, 0.18),
  inset 0 1px 0 rgba(255, 255, 255, 0.96) !important;
}

.voice-studio-shell {
  position: relative;
}

.voice-confirm-mask {
  position: absolute;
  inset: 0;
  z-index: 30;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(16, 24, 38, 0.22);
  border-radius: 1rem;
}

.voice-confirm-card {
  width: min(100%, 25rem);
  max-width: calc(100% - 0.5rem);
  box-sizing: border-box;
  border: 1px solid rgba(255, 255, 255, 0.86);
  border-radius: 1rem;
  padding: 1rem;
  background: linear-gradient(180deg, rgba(253, 249, 243, 0.98), rgba(247, 239, 230, 0.96));
  box-shadow: 0 28px 60px -35px rgba(15, 23, 42, 0.45);
}

.voice-confirm-title {
  font-size: 1rem;
  font-weight: 800;
  color: #1b2437;
}

.voice-confirm-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>
