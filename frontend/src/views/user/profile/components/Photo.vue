<script setup>
import {nextTick, onBeforeMount, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icon/CameraIcon.vue";
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

watch(() => props.photo, newVal => {
  myPhoto.value = newVal
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

async function openModal(photo) {
  modalRef.value.showModal()
  await nextTick() // 等待所有DOM更新完成

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

async function crop(){
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

/**
 * 组件卸载前的清理函数
 * 在组件被销毁之前执行必要的清理操作，防止内存泄漏
 * 主要用于销毁croppie图片裁剪实例
 */
onBeforeUnmount(()=>{
  croppie?.destroy()
})

/**
 * 暴露组件属性给父组件使用
 * 通过defineExpose将myPhoto响应式引用暴露出去，
 * 使得父组件可以通过模板引用访问该组件的头像数据
 * 
 * @property {Ref} myPhoto - 当前用户的头像图片数据的响应式引用
 */
defineExpose({
  myPhoto,
})
</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div class="w-28 rounded-full">
        <img :src="myPhoto" alt="用户头像">
      </div>
      <div @click="fileInputRef.click()"
           class="absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
        <CameraIcon/>
      </div>
    </div>
  </div>

  <input @change="onFileChange" ref="file-input-ref" type="file" accept="image/*" class="hidden">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
      <button @click="modalRef.close()" class="btn btn-circle btn-sm btn-ghost absolute right-2 top-2">×</button>

      <div ref="croppie-ref" class="flex flex-col justify-center my-4"></div>

      <div class="modal-action">
        <button @click="modalRef.close()" class="btn">取消</button>
        <button @click="crop" class="btn btn-primary">确定</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

</style>