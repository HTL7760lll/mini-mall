<template>
  <div class="home-dark">
    <!-- 侧边抽屉 -->
    <div class="sidebar-overlay" :class="{show: sidebarOpen}" @click="sidebarOpen=false" />
    <aside class="sidebar" :class="{open: sidebarOpen}">
      <div class="side-head">
        <div class="side-logo">
          <span class="s-m">M</span><span class="s-i">i</span><span class="s-n">n</span><span class="s-i2">i</span>
          <span class="s-m2">M</span><span class="s-a">a</span><span class="s-l">ll</span>
        </div>
      </div>
      <div class="side-section">
        <div class="side-label">CATEGORY</div>
        <div class="side-item" :class="{active: activeCategory===0}" @click="pickCat(0)">全部</div>
        <div class="side-item" v-for="c in categories" :key="c.id"
          :class="{active: activeCategory===c.id}" @click="pickCat(c.id)">
          {{ c.name }}
          <span class="cat-count">{{ c.goods_count }}</span>
        </div>
      </div>
    </aside>

    <!-- 主内容 -->
    <div class="main-area">
      <!-- 顶栏 -->
      <header class="topbar">
        <div class="menu-btn" @click="sidebarOpen=!sidebarOpen">
          <span /><span /><span />
        </div>
        <div class="top-logo">
          <span class="t-m">M</span><span class="t-i">i</span><span class="t-n">n</span><span class="t-i2">i</span>
          <span class="t-m2">M</span><span class="t-a">a</span><span class="t-ll">ll</span>
        </div>
        <div class="top-right">
          <div class="search-mini">
            <input v-model="keyword" placeholder="Search" @keyup.enter="onSearch" />
            <span class="search-icon" @click="onSearch">&#8981;</span>
          </div>
          <div class="user-btn" @click="goLogin">&#9786;</div>
        </div>
      </header>

      <!-- 内容区 -->
      <div v-if="loading" class="loading-wrap">
        <div class="spinner" />
      </div>

      <div v-else-if="goodsList.length" class="goods-grid">
        <GoodsCard v-for="item in goodsList" :key="item.id" :goods="item" @click="goDetail(item.id)" />
      </div>

      <div v-else class="empty">No products found</div>

      <div v-if="total > pageSize" class="pagination-wrap">
        <van-pagination v-model="currentPage" :total-items="total" :items-per-page="pageSize" mode="simple" @change="onPageChange" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getGoodsPage, getCategoryTree } from '../../api/goods'
import GoodsCard from '../../components/GoodsCard.vue'

const router = useRouter()
const sidebarOpen = ref(false)
const keyword = ref('')
const categories = ref([])
const activeCategory = ref(0)
const goodsList = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = 20
const total = ref(0)

const loadCategories = async () => {
  try {
    const data = await getCategoryTree()
    const flat = []
    for (const p of data) {
      if (p.children?.length) for (const c of p.children) { if (c.goods_count > 0) flat.push(c) }
      if (p.goods_count > 0) flat.push(p)
    }
    categories.value = flat
  } catch (e) { console.error(e) }
}

const loadGoods = async () => {
  loading.value = true
  try {
    const params = { page: currentPage.value, pageSize }
    if (keyword.value) params.keyword = keyword.value
    if (activeCategory.value > 0) params.categoryId = activeCategory.value
    const data = await getGoodsPage(params)
    goodsList.value = data.records || []
    total.value = data.total || 0
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

const pickCat = (id) => { activeCategory.value = id; currentPage.value = 1; sidebarOpen.value = false; loadGoods() }
const onSearch = () => { currentPage.value = 1; loadGoods() }
const onPageChange = (p) => { currentPage.value = p; loadGoods() }
const goDetail = (id) => router.push(`/goods/${id}`)
const goLogin = () => router.push('/login')

onMounted(() => { loadCategories(); loadGoods() })
</script>

<style scoped>
.home-dark { display: flex; min-height: 100vh; background: #0d1117; }

/* SIDEBAR */
.sidebar-overlay { position: fixed; inset:0; background: rgba(0,0,0,.5); z-index:90; opacity:0; pointer-events:none; transition: opacity .25s; }
.sidebar-overlay.show { opacity:1; pointer-events:auto; }
.sidebar {
  position: fixed; top:0; left:0; bottom:0; width: 220px; z-index:95;
  background: #161b22; border-right: 1px solid #21262d;
  transform: translateX(-100%); transition: transform .25s;
  display: flex; flex-direction: column; overflow-y: auto;
}
.sidebar.open { transform: translateX(0); }

.side-head { padding: 20px 16px; border-bottom: 1px solid #21262d; }
.side-logo { font-size: 22px; font-weight: 800; letter-spacing: -1px; }
.s-m { color: #ff6b35; } .s-i,.s-i2 { color: #00d4ff; } .s-n { color: #ffd700; }
.s-m2 { color: #4caf50; } .s-a { color: #2196f3; } .s-l { color: #9c27b0; }

.side-section { padding: 12px 0; }
.side-label { font-size: 10px; color: #ff6b35; padding: 8px 16px 4px; letter-spacing: 2px; font-weight: 600; }
.side-item {
  padding: 8px 16px; font-size: 13px; color: #8b949e; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
  transition: background .15s; border-left: 2px solid transparent;
}
.side-item:hover { background: #1c2128; color: #c9d1d9; }
.side-item.active { background: #1c2128; color: #ff6b35; border-left-color: #ff6b35; }
.cat-count { font-size: 10px; color: #484f58; background: #21262d; padding: 1px 6px; border-radius: 10px; }

/* MAIN */
.main-area { flex:1; margin-left:0; width:100%; }

/* TOPBAR */
.topbar {
  display: flex; align-items: center; gap: 10px; padding: 8px 12px;
  background: #161b22; border-bottom: 1px solid #21262d;
  position: sticky; top:0; z-index:10;
}
.menu-btn { display: flex; flex-direction: column; gap:4px; cursor: pointer; padding: 4px; }
.menu-btn span { display: block; width: 20px; height: 2px; background: #c9d1d9; border-radius: 1px; }

.top-logo { font-size: 18px; font-weight: 800; letter-spacing: -1px; }
.t-m { color: #ff6b35; } .t-i,.t-i2 { color: #00d4ff; } .t-n { color: #ffd700; }
.t-m2 { color: #4caf50; } .t-a { color: #2196f3; } .t-ll { color: #9c27b0; }

.top-right { display: flex; align-items: center; gap: 8px; margin-left: auto; }
.search-mini {
  display: flex; align-items: center; background: #0d1117; border: 1px solid #30363d;
  border-radius: 4px; padding: 3px 8px;
}
.search-mini input {
  background: none; border: none; outline: none; color: #c9d1d9;
  font-size: 12px; width: 100px;
}
.search-mini input::placeholder { color: #484f58; }
.search-icon { color: #484f58; cursor: pointer; font-size: 14px; }
.user-btn { color: #8b949e; font-size: 18px; cursor: pointer; }

/* GRID */
.goods-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: #21262d;
  border: 1px solid #21262d;
  margin: 12px 16px;
}
.loading-wrap { display: flex; justify-content: center; padding: 80px 0; }
.spinner {
  width: 32px; height: 32px; border: 3px solid #21262d;
  border-top-color: #ff6b35; border-radius: 50%; animation: spin .8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.empty { text-align: center; padding: 80px 0; color: #484f58; font-size: 13px; }
.pagination-wrap { padding: 16px 0 32px; }
.pagination-wrap :deep(.van-pagination__item) { background:#161b22; color:#8b949e; }
</style>
