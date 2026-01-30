/*
 * 功能：在每个请求头里自动添加`access token`。
 * 然后拦截请求结果，如果返回结果是身份认证失败（401），
 * 则说明`access_token`过期了，
 * 那么先用`cookie`中的`refresh_token`刷新`access_token`。
 * 如果刷新失败则说明`refreh_token`也过期了，
 * 则调用`user.logout()`在浏览器内存中删除登录状态；
 * 如果刷新成功，则重新发送原请求。
*/

import axios from "axios"
import {useUserStore} from "@/stores/user.js";

// 定义API基础URL
const BASE_URL = 'http://127.0.0.1:8000'

// 创建axios实例，配置基础URL和携带凭证
const api = axios.create({
    baseURL: BASE_URL,
    withCredentials: true,
})

/*
 * 请求拦截器
 * 在每个请求发送前自动添加Authorization头部
 */
api.interceptors.request.use(config => {
    const user = useUserStore()
    if (user.accessToken) {
        config.headers.Authorization = `Bearer ${user.accessToken}`
    }
    return config
})

// 刷新令牌相关状态变量
let isRefreshing = false
let refreshSubscribers = []

/*
 * 订阅令牌刷新回调函数
 * @param {Function} callback - 令牌刷新完成后的回调函数
 */
function subscribeTokenRefresh(callback) {
    refreshSubscribers.push(callback)
}

/*
 * 令牌刷新成功处理函数
 * @param {string} token - 新的访问令牌
 */
function onRefreshed(token) {
    refreshSubscribers.forEach(cb => cb(token))
    refreshSubscribers = []
}

/*
 * 令牌刷新失败处理函数
 * @param {Error} err - 刷新失败的错误信息
 */
function onRefreshFailed(err) {
    refreshSubscribers.forEach(cb => cb(null, err))
    refreshSubscribers = []
}

/*
 * 响应拦截器
 * 处理401未授权错误，自动刷新令牌并重试请求
 */
api.interceptors.response.use(
    response => response,
    async error => {
        const user = useUserStore()
        const originalRequest = error?.config
        
        // 如果没有原始请求配置，直接拒绝Promise
        if (!originalRequest) {
            return Promise.reject(error)
        }

        // 处理401未授权错误且请求未重试过的情况
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            return new Promise((resolve, reject) => {
                // 订阅令牌刷新结果
                subscribeTokenRefresh((token, error) => {
                    if (error) {
                        reject(error)
                    } else {
                        originalRequest.headers.Authorization = `Bearer ${token}`
                        resolve(api(originalRequest))
                    }
                })

                // 如果当前没有正在刷新令牌，则发起刷新请求
                if (!isRefreshing) {
                    isRefreshing = true
                    
                    // 发送刷新令牌请求
                    axios.post(
                        `${BASE_URL}/api/user/account/refresh_token/`,
                        {},
                        {withCredentials: true, timeout: 5000}
                    ).then(res => {
                        // 更新用户存储中的访问令牌
                        user.setAccessToken(res.data.access)
                        // 通知所有订阅者刷新成功
                        onRefreshed(res.data.access)
                    }).catch(error => {
                        // 刷新失败，执行登出操作
                        user.logout()
                        // 通知所有订阅者刷新失败
                        onRefreshFailed(error)
                        reject(error)
                    }).finally(() => {
                        // 重置刷新状态
                        isRefreshing = false
                    })
                }
            })
        }

        return Promise.reject(error)
    }
)

export default api