<script setup>
import Photo from "@/views/create/character/components/Photo.vue";
import Name from "@/views/create/character/components/Name.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import {onMounted, ref, useTemplateRef} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.js";
import {useUserStore} from "@/stores/user.js";
import {useRoute, useRouter} from "vue-router";
import api from "@/js/http/api.js";
import Voice from "@/views/create/character/components/Voice.vue";

const user = useUserStore()
const route = useRoute()
const router = useRouter()
const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const voiceRef = useTemplateRef('voice-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')
const errorMessage = ref('')
const characterId = route.params.character_id
const character = ref(null)

const voices = ref([])
const curVoiceId = ref(null)

onMounted(async () => {
  try {
    const res = await api.get('/api/create/character/get_single/', {
      params: {
        character_id: characterId
      }
    })
    const data = res.data
    if (data.result === 'success') {
      character.value = data.character
      voices.value = data.voices
      curVoiceId.value = data.character.voice_id || data.voices?.[0]?.id || null
    } else {
      errorMessage.value = data.result
    }
  } catch (err) {
    console.log(err)
    errorMessage.value = err?.response?.data?.result || '网络异常，请稍后重试'
  }
})

async function handleUpdate() {
  const photo = photoRef.value.myPhoto
  const name = nameRef.value.myName?.trim()
  const voice = `${voiceRef.value.myVoice ?? ''}`.trim()
  const profile = profileRef.value.myProfile?.trim()
  const backgroundImage = backgroundImageRef.value.myBackgroundImage

  errorMessage.value = ''
  if (!photo) {
    errorMessage.value = '请上传头像'
  } else if (!name) {
    errorMessage.value = '请输入角色名称'
  } else if (!voice) {
    errorMessage.value = '请选择角色音色'
  } else if (!profile) {
    errorMessage.value = '请输入角色介绍'
  } else if (!backgroundImage) {
    errorMessage.value = '请上传聊天背景'
  } else {
    const formData = new FormData()
    formData.append('character_id', characterId)
    formData.append('name', name)
    formData.append('voice_id', voice)
    formData.append('profile', profile)
    // formData.append('photo', base64ToFile(photo, 'photo.png'))
    if (photo !== character.value.photo) {
      formData.append('photo', base64ToFile(photo, 'photo.png'))
    }

    // formData.append('background_image', base64ToFile(backgroundImage, 'background_image.png'))
    if (backgroundImage !== character.value.background_image) {
      formData.append('background_image', base64ToFile(backgroundImage, 'background_image.png'))
    }

    try {
      const res = await api.post('/api/create/character/update/', formData)
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
  <div v-if="character" class="flex justify-center">
    <div class="editor-card card w-120 mt-16">
      <div class="card-body">
        <h3 class="editor-title text-lg my-4">更新角色</h3>
        <Photo ref="photo-ref" :photo="character.photo"/>
        <Name ref="name-ref" :name="character.name"/>
        <Voice ref="voice-ref" :voices="voices" :curVoiceId="curVoiceId"/>
        <Profile ref="profile-ref" :profile="character.profile"/>
        <BackgroundImage ref="background-image-ref" :backgroundImage="character.background_image"/>

        <p v-if="errorMessage" class="text-sm text-red-500">{{ errorMessage }}</p>

        <div class="flex justify-center">
          <button @click="handleUpdate" class="editor-submit btn w-60 mt-2">更新</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
