<script setup>
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icon/CameraIcon.vue";
import Croppie from "croppie";
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

watch(() => props.photo, newVal => {
  myPhoto.value = newVal
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')

async function openModal(photo) {
  modalRef.value.showModal()
  await nextTick()
  if (!croppie) {
    croppie = new Croppie(croppieRef.value, {
      viewport: {width: 200, height: 200, type: 'square'},
      boundary: {width: 300, height: 300},
      enableOrientation: true,
      enforceBoundary: true,
    })
  }
  croppie.bind({
    url: photo,
  })
}

async function crop() {
  if (!croppie) return
  myPhoto.value = await croppie.result({
    type: 'base64',
    size: 'viewport',
  })
  modalRef.value.close()
}

function onFileChange(e) {
  const file = e.target.files[0]
  e.target.value = ''
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    openModal(reader.result)
  }
  reader.readAsDataURL(file)
}

onBeforeUnmount(() => {
  croppie?.destroy()
})

defineExpose({
  myPhoto,
})
</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div v-if="myPhoto" class="upload-photo-frame w-28 rounded-full">
        <img :src="myPhoto" alt="">
      </div>
      <div v-else class="upload-photo-empty w-28 h-28 rounded-full"></div>
      <button type="button" @click="fileInputRef.click()"
              class="upload-photo-trigger absolute left-0 top-0 flex h-28 w-28 items-center justify-center rounded-full">
        <span class="upload-photo-icon">
          <CameraIcon/>
        </span>
      </button>
    </div>
  </div>

  <input @change="onFileChange" ref="file-input-ref" type="file" class="hidden" accept="image/*">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
      <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">×</button>

      <div ref="croppie-ref" class="flex-flex-col my-4"></div>

      <div class="modal-action">
        <button @click="modalRef.close()" class="btn">取消</button>
        <button @click="crop" class="btn btn-primary">确定</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
.upload-photo-frame,
.upload-photo-empty {
  overflow: hidden;
  border: 1px solid rgba(224, 211, 194, 0.96);
  box-shadow: 0 18px 34px -24px rgba(15, 23, 42, 0.22);
}

.upload-photo-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-photo-empty {
  background:
    radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.9), transparent 38%),
    linear-gradient(180deg, #fffdfa 0%, #f8efe4 100%);
}

.upload-photo-trigger {
  color-scheme: only light;
  forced-color-adjust: none;
  color: #43516b;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), rgba(23, 32, 51, 0.06));
  transition: background-color 180ms ease, transform 180ms ease;
}

.upload-photo-trigger:hover {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.12), rgba(23, 32, 51, 0.1));
}

.upload-photo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3.15rem;
  height: 3.15rem;
  border: 1px solid rgba(255, 255, 255, 0.92);
  border-radius: 999px;
  background: rgba(255, 252, 247, 0.9);
  box-shadow: 0 12px 22px -18px rgba(15, 23, 42, 0.48);
}
</style>
