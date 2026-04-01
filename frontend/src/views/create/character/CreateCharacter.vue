<script setup>
import Photo from "@/views/create/character/components/Photo.vue";
import Name from "@/views/create/character/components/Name.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import {computed, onMounted, ref, useTemplateRef, watch} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.js";
import {useUserStore} from "@/stores/user.js";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";
import VoiceSelect from "@/views/create/character/components/VoiceSelect.vue";
import CustomVoiceManager from "@/views/create/character/components/CustomVoiceManager.vue";

const user = useUserStore()
const router = useRouter()
const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')
const errorMessage = ref('')

const voices = ref([])
const customVoices = ref([])
const voiceSource = ref('system')
const systemVoiceId = ref(null)
const customVoiceId = ref(null)
const loadingCustomVoices = ref(false)

const systemVoices = computed(() => {
  return (voices.value || []).filter(v => !v.is_custom)
})

const selectedVoiceId = computed(() => {
  if (voiceSource.value === 'custom') {
    return customVoiceId.value != null ? String(customVoiceId.value) : ''
  }
  return systemVoiceId.value != null ? String(systemVoiceId.value) : ''
})

function handleSelectSystemVoice(next) {
  if (next == null || String(next) === '') return
  systemVoiceId.value = String(next)
  customVoiceId.value = null
  voiceSource.value = 'system'
}

async function loadVoices(preferVoiceId = null) {
  const res = await api.get('/api/create/character/voice/get_list/', {})
  const data = res.data
  if (data.result !== 'success') {
    errorMessage.value = data.result
    return
  }

  voices.value = data.voices || []
  const currentSystemId = systemVoiceId.value != null ? String(systemVoiceId.value) : null
  const firstSystem = systemVoices.value?.[0]?.id || null

  if (currentSystemId && systemVoices.value.some(v => String(v.id) === currentSystemId)) {
    return
  }
  systemVoiceId.value = firstSystem
}

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

onMounted(async () => {
  try {
    await loadVoices()
    await loadCustomVoices()
  } catch (err) {
    console.log(err)
    errorMessage.value = err?.response?.data?.result || '网络异常，请稍后重试'
  }
})

function handleSelectVoice(payload) {
  const voiceId = payload?.voice_id
  if (!voiceId) return
  customVoiceId.value = String(voiceId)
  voiceSource.value = 'custom'
}

function handleSelectVoiceSource(next) {
  if (next !== 'system' && next !== 'custom') return
  voiceSource.value = next
  if (next === 'system') {
    customVoiceId.value = null
    if (!systemVoiceId.value) {
      systemVoiceId.value = systemVoices.value?.[0]?.id || null
    }
    return
  }
  if (!customVoiceId.value && customVoices.value?.length) {
    customVoiceId.value = String(customVoices.value[0].id)
  }
}

async function handleRefreshCustomVoices() {
  await loadCustomVoices()
}

async function handleCreate() {
  const photo = photoRef.value.myPhoto
  const name = nameRef.value.myName?.trim()
  const voice = `${selectedVoiceId.value ?? ''}`.trim()
  const profile = profileRef.value.myProfile?.trim()
  const backgroundImage = backgroundImageRef.value.myBackgroundImage

  errorMessage.value = ''
  if (!photo) {
    errorMessage.value = '请上传头像'
  } else if (!name) {
    errorMessage.value = '请输入角色名称'
  } else if (!voice) {
    errorMessage.value = '请选择音色'
  } else if (!profile) {
    errorMessage.value = '请输入角色介绍'
  } else if (!backgroundImage) {
    errorMessage.value = '请上传聊天背景'
  } else {
    const formData = new FormData()
    formData.append('name', name)
    formData.append('voice_id', voice)
    formData.append('profile', profile)
    formData.append('photo', base64ToFile(photo, 'photo.png'))
    formData.append('background_image', base64ToFile(backgroundImage, 'background_image.png'))

    try {
      const res = await api.post('/api/create/character/create/', formData)
      const data = res.data
      if (data.result === 'success') {
        await router.push({
          name: 'user-space-index',
          params: {
            user_id: user.id
          }
        })
      } else {
        errorMessage.value = data.result
      }
    } catch (err) {
      console.log(err)
      errorMessage.value = err?.response?.data?.result || '网络异常，请稍后重试'
    }
  }
}
</script>

<template>
  <div class="flex justify-center">
    <div class="editor-card card w-120 mt-16">
      <div class="card-body">
        <h3 class="editor-title text-lg my-4">创建角色</h3>
        <Photo ref="photo-ref"/>
        <Name ref="name-ref"/>
        <div class="voice-source-head">
          <button
              type="button"
              class="voice-source-tab"
              :class="{'voice-source-tab-active': voiceSource === 'system'}"
              @click="handleSelectVoiceSource('system')"
          >系统音色</button>
          <button
              type="button"
              class="voice-source-tab"
              :class="{'voice-source-tab-active': voiceSource === 'custom'}"
              @click="handleSelectVoiceSource('custom')"
          >自定义音色</button>
        </div>

        <div v-if="voiceSource === 'system'" class="system-voice-block">
          <VoiceSelect
              :voices="systemVoices"
              v-model="systemVoiceId"
              placeholder="请选择系统音色"
              searchPlaceholder="搜索系统音色"
              @update:modelValue="handleSelectSystemVoice"
          />
        </div>
        <div v-else class="custom-voice-block">
          <CustomVoiceManager
              :customVoices="customVoices"
              :curVoiceId="customVoiceId"
              :loadingCustomVoices="loadingCustomVoices"
              @select-voice="handleSelectVoice"
              @refresh-custom-voices="handleRefreshCustomVoices"
          />
        </div>
        <Profile ref="profile-ref"/>
        <BackgroundImage ref="background-image-ref"/>

        <p v-if="errorMessage" class="text-sm text-red-500">{{ errorMessage }}</p>

        <div class="flex justify-center">
          <button @click="handleCreate" class="editor-submit btn w-60 mt-2">创建</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.voice-source-head {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6rem;
  margin-bottom: 0.65rem;
}

.voice-source-tab {
  border: 1px solid rgba(214, 202, 186, 0.96);
  border-radius: 1rem;
  padding: 0.75rem 1rem;
  font-weight: 800;
  color: #63594e;
  background: rgba(255, 255, 255, 0.72);
  cursor: pointer;
}

.voice-source-tab-active {
  border-color: rgba(194, 167, 133, 0.96);
  background: rgba(245, 235, 223, 0.92);
  color: #0f172a;
  box-shadow:
    0 0 0 3px rgba(222, 197, 164, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.96);
}

:deep(.system-voice-block .editor-fieldset > .editor-label) {
  display: none;
}

:deep(.custom-voice-block .editor-fieldset > .editor-label) {
  display: none;
}
</style>
