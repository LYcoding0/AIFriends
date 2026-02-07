<script setup>

import Photo from "@/views/user/profile/components/Photo.vue";
import Username from "@/views/user/profile/components/Username.vue";
import Profile from "@/views/user/profile/components/Profile.vue";
import {useUserStore} from "@/stores/user.js";
import {ref, useTemplateRef} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";

const user = useUserStore()
const photoRef = useTemplateRef('photo-ref')
const usernameRef = useTemplateRef('username-ref')
const profileRef = useTemplateRef('profile-ref')
const errorMassage = ref('')

async function handleUpdate() {
  const photo = photoRef.value.myPhoto
  const username = usernameRef.value.myUsername.trim()
  const profile = profileRef.value.myProfile.trim()

  errorMassage.value = ''
  if (!photo) {
    errorMassage.value = '头像不能为空'
  } else if (!username) {
    errorMassage.value = '用户名不能为空'
  } else if (!profile) {
    errorMassage.value = '简介不能为空'
  } else {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('profile', profile)
    if (photo !== user.photo) {
      formData.append('photo', base64ToFile(photo, 'photo.png'))
    }

    try {
      const res = await api.post('/api/user/profile/update/', formData)
      const data = res.data
      if (data.result === 'success') {
        user.setUserInfo(data)
      }else {
        errorMassage.value = data.result
      }
    } catch (err) {
      console.log(err)
    }
  }
}
</script>

<template>
  <div class="flex justify-center">
    <div class="card w-120 bg-base-200 shadow-sm mt-16">
      <div class="card-body">
        <h3 class="text-lg font-bold mt-4">编辑资料</h3>
        <Photo ref="photo-ref" :photo="user.photo"/>
        <Username ref="username-ref" :username="user.username"/>
        <Profile ref="profile-ref" :profile="user.profile"/>
        <p v-if="errorMassage" class="text-sm text-red-500">{{ errorMassage }}</p>
        <div class="flex justify-center">
          <button @click="handleUpdate" class="btn btn-neutral w-60 mt-2">更新</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>