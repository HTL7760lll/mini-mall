import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Vant 按需引入（移动端）
import {
  Button, Search, Tab, Tabs, Card, Tag, Grid, GridItem,
  Image as VanImage, NavBar, Icon, Toast, Stepper,
  SubmitBar, Checkbox, Empty, Pagination, Loading, Skeleton,
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
app.mount('#app')
