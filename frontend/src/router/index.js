import {createRouter, createWebHistory} from 'vue-router'
import HomepageIndex from "@/views/homepage/HomepageIndex.vue";
import FriendIndex from "@/views/friend/FriendIndex.vue";
import CreateIndex from "@/views/create/CreateIndex.vue";
import NotFoundIndex from "@/views/error/NotFoundIndex.vue";
import LoginIndex from "@/views/user/account/LoginIndex.vue";
import RegisterIndex from "@/views/user/account/RegisterIndex.vue";
import SpaceIndex from "@/views/user/space/SpaceIndex.vue";
import ProfileIndex from "@/views/user/profile/ProfileIndex.vue";
import {useUserStore} from "@/stores/user.js";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'homepage-index',
            component: HomepageIndex,
            meta: {
                needLogin: false
            }
        },
        {
            path: '/friend/',
            name: 'friend-index',
            component: FriendIndex,
            meta: {
                needLogin: true
            }

        },
        {
            path: '/create/',
            name: 'create-index',
            component: CreateIndex,
            meta: {
                needLogin: true
            }
        },
        {
            path: '/404/',
            name: '404',
            component: NotFoundIndex,
            meta: {
                needLogin: false
            }
        },
        {
            path: '/user/account/login/',
            name: 'user-account-login-index',
            component: LoginIndex,
            meta: {
                needLogin: false
            }
        },
        {
            path: '/user/account/register/',
            name: 'user-account-register-index',
            component: RegisterIndex,
            meta: {
                needLogin: false
            }
        },
        {
            path: '/user/space/:user_id/',
            name: 'user-space-index',
            component: SpaceIndex,
            meta: {
                needLogin: true
            }
        },
        {
            path: '/user/profile',
            name: 'user-profile-index',
            component: ProfileIndex,
            meta: {
                needLogin: true
            }
        },
        {
            path: '/:pathMatch(.*)*', // 匹配任意路径,作为兜底路由
            name: 'not-found',
            component: NotFoundIndex,
            meta: {
                needLogin: false
            }
        }
    ],
})

/*
 * 全局路由前置守卫函数
 * 在每次路由跳转前执行权限验证
 * @param {RouteLocationNormalized} to - 即将要进入的目标路由对象
 * @param {RouteLocationNormalized} from - 当前导航正要离开的路由对象
 * @param {NavigationGuardNext} next - 用来resolve这个钩子的函数
 * @returns {boolean|Object} 返回true允许导航继续，返回路由对象则重定向到指定路由
 */
router.beforeEach((to, from) => {
    const user = useUserStore()
    
    // 权限验证逻辑：
    // 1. 检查目标路由是否需要登录权限 (to.meta.needLogin)
    // 2. 确认用户信息已加载完成 (user.hasPulledUserInfo)
    // 3. 验证用户是否未登录 (!user.isLogin())
    // 只有同时满足这三个条件时才重定向到登录页
    if (to.meta.needLogin && user.hasPulledUserInfo && !user.isLogin()) {
        return {name: 'user-account-login-index'}
    }
    
    // 允许正常导航
    return true
})

export default router
