import {defineStore} from "pinia";
import {ref} from "vue";


export const useUserStore = defineStore('user', () => {
    const id = ref(1)
    const username = ref('lycoding')
    const photo = ref('http://127.0.0.1:8000/media/user/photos/default.jpg')
    const profile = ref('1')
    const accessToken = ref('1')

    function isLogin() {
        return !!accessToken.value  //将任何值转换为严格的 true 或 false,有值则返回true
    }

    function setAccessToken(token) {
        accessToken.value = token
    }

    function setUserInfo(data) { // view/user/account/login.py返回的数据
        id.value = data.user_id
        username.value = data.username
        photo.value = data.photo
        profile.value = data.profile
    }

    function logout(){
        id.value = 0
        username.value = ''
        photo.value = ''
        profile.value = ''
        accessToken.value = ''
    }

    return {
        id,
        username,
        photo,
        profile,
        accessToken,
        setAccessToken,
        setUserInfo,
        logout,
        isLogin
    }
})