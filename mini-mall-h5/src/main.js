import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Vant 按需引入（移动端）
import {
  Button, Search, Tab, Tabs, Card, Tag, Grid, GridItem,
  Image as VanImage, NavBar, Icon, Toast, Stepper,
  SubmitBar, Checkbox, Empty, Pagination, Loading, Skeleton,
  Field, Form,
} from 'vant'
import 'vant/lib/index.css'

const app = createApp(App)

// 注册 Vant 组件
const vantComponents = [
  Button, Search, Tab, Tabs, Card, Tag, Grid, GridItem,
  VanImage, NavBar, Icon, Toast, Stepper,
  SubmitBar, Checkbox, Empty, Pagination, Loading, Skeleton,
]
vantComponents.forEach(comp => app.component(comp.name || comp.__name, comp))

app.use(createPinia())
app.use(router)

// 点击外部关闭指令
app.directive('click-outside', {
  mounted(el, binding) {
    el._clickOutside = (e) => { if (!el.contains(e.target)) binding.value() }
    document.addEventListener('click', el._clickOutside)
  },
  unmounted(el) { document.removeEventListener('click', el._clickOutside) },
})

app.mount('#app')
