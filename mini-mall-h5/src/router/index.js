import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/home/index.vue'),
    meta: { title: 'Mini Mall' },
  },
  {
    path: '/goods/:id',
    name: 'goodsDetail',
    component: () => import('../views/goods/detail.vue'),
    meta: { title: '商品详情' },
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Mini Mall'
  next()
})

export default router
