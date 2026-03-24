<script setup>
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icon/CameraIcon.vue";
import Croppie from "croppie";
import 'croppie/croppie.css'

const props = defineProps(['backgroundImage'])
const myBackgroundImage = ref(props.backgroundImage)

watch(() => props.backgroundImage, newVal => {
  myBackgroundImage.value = newVal
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

async function openModal(photo) {
  modalRef.value.showModal()
  await nextTick()
  if (!croppie) {
    croppie = new Croppie(croppieRef.value, {
      viewport: {width: 300, height: 500},
      boundary: {width: 600, height: 600},
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
  myBackgroundImage.value = await croppie.result({
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
  myBackgroundImage,
})
</script>

<template>
  <fieldset class="editor-fieldset fieldset">
    <label class="editor-label label text-base">聊天背景</label>
    <div class="avatar relative">
      <div v-if="myBackgroundImage" class="upload-background-frame w-15 h-25 rounded-box">
        <img :src="myBackgroundImage" alt="">
      </div>
      <div v-else class="upload-background-empty w-15 h-25 rounded-box"></div>
      <button type="button" @click="fileInputRef.click()"
              class="upload-background-trigger absolute left-0 top-0 flex h-25 w-15 items-center justify-center rounded-box">
        <span class="upload-background-icon">
          <CameraIcon/>
        </span>
      </button>
    </div>
  </fieldset>

  <input @change="onFileChange" ref="file-input-ref" type="file" class="hidden" accept="image/*">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none max-w-2xl">
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
.upload-background-frame,
.upload-background-empty {
  overflow: hidden;
  border: 1px solid rgba(224, 211, 194, 0.96);
  box-shadow: 0 18px 34px -24px rgba(15, 23, 42, 0.22);
}

.upload-background-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-background-empty {
  background:
    radial-gradient(circle at 25% 20%, rgba(255, 255, 255, 0.88), transparent 34%),
    linear-gradient(180deg, #fffdfa 0%, #f8efe4 100%);
}

.upload-background-trigger {
  color-scheme: only light;
  forced-color-adjust: none;
  color: #43516b;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), rgba(23, 32, 51, 0.06));
  transition: background-color 180ms ease;
}

.upload-background-trigger:hover {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.12), rgba(23, 32, 51, 0.1));
}

.upload-background-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.85rem;
  height: 2.85rem;
  border: 1px solid rgba(255, 255, 255, 0.92);
  border-radius: 999px;
  background: rgba(255, 252, 247, 0.9);
  box-shadow: 0 12px 22px -18px rgba(15, 23, 42, 0.48);
}
</style>
