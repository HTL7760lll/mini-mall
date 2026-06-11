import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/home/index.vue'), meta: { title: 'Mini Mall' } },
  { path: '/goods/:id', name: 'goodsDetail', component: () => import('../views/goods/detail.vue'), meta: { title: '商品详情' } },
  { path: '/login', name: 'login', component: () => import('../views/member/login.vue'), meta: { title: '登录' } },
  { path: '/register', name: 'register', component: () => import('../views/member/register.vue'), meta: { title: '注册' } },
  { path: '/orders', name: 'orders', component: () => import('../views/order/list.vue'), meta: { title: '我的订单', auth: true } },
  { path: '/order/:id', name: 'orderDetail', component: () => import('../views/order/detail.vue'), meta: { title: '订单详情', auth: true } },
  { path: '/cart', name: 'cart', component: () => import('../views/cart/index.vue'), meta: { title: '购物车', auth: true } },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() { return { top: 0 } },
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Mini Mall'
  if (to.meta.auth && !localStorage.getItem('token')) {
    next('/login')
  } else {
    next()
  }
})

export default router
