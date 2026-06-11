<template>
  <div class="steam-layout">
    <!-- 左侧栏 -->
    <aside class="sidebar">
      <div class="side-head">
        <div class="side-logo">
          <span class="c-o">M</span><span class="c-c">i</span><span class="c-y">n</span><span class="c-c">i</span>
          <span class="c-g">M</span><span class="c-b">a</span><span class="c-p">ll</span>
        </div>
        <div class="side-tagline">MARKET</div>
      </div>

      <div class="side-divider" />

      <!-- 分类折叠 -->
      <div class="sec-header" @click="showCat=!showCat">
        <span>📂 CATEGORY</span>
        <span class="sec-arrow" :class="{open: showCat}">▾</span>
      </div>
      <div class="sec-body" v-show="showCat">
        <div class="side-item" :class="{sel: activeCategory===0}" @click="pickCat(0)">All Items</div>
        <div class="side-item" v-for="c in topCategories" :key="c.id" :class="{sel: activeCategory===c.id}" @click="pickCat(c.id)">
          {{ c.name }}
        </div>
      </div>

      <div class="side-divider" />

      <!-- 品牌折叠 -->
      <div class="sec-header" @click="showBrand=!showBrand">
        <span>🏷️ BRAND</span>
        <span class="sec-arrow" :class="{open: showBrand}">▾</span>
      </div>
      <div class="sec-body" v-show="showBrand">
        <div class="side-item" v-for="c in brandCategories" :key="c.id" :class="{sel: activeCategory===c.id}" @click="pickCat(c.id)">
          {{ c.name }}
        </div>
      </div>

      <div class="side-divider" />

      <!-- 价格 -->
      <div class="sec-header" @click="showPrice=!showPrice">
        <span>💰 PRICE</span>
        <span class="sec-arrow" :class="{open: showPrice}">▾</span>
      </div>
      <div class="sec-body" v-show="showPrice">
        <div class="price-row">
          <input v-model="minPrice" placeholder="Min" class="price-inp" @keyup.enter="applyPrice" />
          <span class="price-dash">-</span>
          <input v-model="maxPrice" placeholder="Max" class="price-inp" @keyup.enter="applyPrice" />
        </div>
        <div class="price-actions">
          <button class="btn-sm" @click="applyPrice">Apply</button>
          <button class="btn-sm ghost" v-if="minPrice||maxPrice" @click="minPrice='';maxPrice='';applyPrice()">Reset</button>
        </div>
      </div>

      <div class="side-divider" />

      <!-- 排序 -->
      <div class="sec-header" @click="showSort=!showSort">
        <span>🔽 SORT</span>
        <span class="sec-arrow" :class="{open: showSort}">▾</span>
      </div>
      <div class="sec-body" v-show="showSort">
        <div class="side-item" :class="{sel: sort===''}" @click="setSort('')">Default</div>
        <div class="side-item" :class="{sel: sort==='price_asc'}" @click="setSort('price_asc')">Price ↑</div>
        <div class="side-item" :class="{sel: sort==='price_desc'}" @click="setSort('price_desc')">Price ↓</div>
        <div class="side-item" :class="{sel: sort==='sales'}" @click="setSort('sales')">Best Selling</div>
      </div>

      <div class="side-footer">
        <div class="copy">Mini Mall v1.0</div>
        <div class="copy-sub">© 2026</div>
      </div>
    </aside>

    <!-- 右侧主区 -->
    <div class="main">
      <!-- 顶栏: 搜索 + 用户菜单 -->
      <div class="search-bar">
        <div class="search-inner">
          <span class="s-icon">&#8981;</span>
          <input v-model="keyword" placeholder="Search the market" @keyup.enter="onSearch" />
        </div>
        <div class="result-info">{{ total }} results</div>
        <div class="user-menu" v-click-outside="closeMenu">
          <div class="user-trigger" @click="menuOpen=!menuOpen">
            <span class="u-icon">{{ userName ? '&#9786;' : '&#9787;' }}</span>
            <span class="u-label">{{ userName || 'LOGIN' }}</span>
          </div>
          <div class="user-drop" v-if="menuOpen">
            <template v-if="userName">
              <div class="drop-item" @click="goOrders">📋 我的订单</div>
              <div class="drop-item" @click="goCart">🛒 购物车</div>
              <div class="drop-divider" />
              <div class="drop-item logout" @click="handleLogout">↪ 退出登录</div>
            </template>
            <template v-else>
              <div class="drop-item" @click="goLogin">🔑 登录</div>
              <div class="drop-item" @click="goRegister">📝 注册</div>
            </template>
          </div>
        </div>
      </div>

      <!-- 加载 -->
      <div v-if="loading" class="loading"><div class="spin" /></div>

      <!-- 格子列表 -->
      <div v-else class="item-grid">
        <div class="grid-card" v-for="item in goodsList" :key="item.id" @click="goDetail(item.id)">
          <div class="gc-img">
            <img :src="`https://picsum.photos/160/120?random=${item.id}`" :alt="item.name" />
            <span v-if="item.is_hot" class="tag-hot">HOT</span>
            <span v-if="item.is_new" class="tag-new">NEW</span>
          </div>
          <div class="gc-info">
            <div class="gc-name">{{ item.name }}</div>
            <div class="gc-row">
              <span class="gc-price">¥{{ item.price }}</span>
              <span class="gc-sales" v-if="item.sales">{{ fmtSales(item.sales) }}</span>
            </div>
          </div>
        </div>
      </div>

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

const router = useRouter()
const keyword = ref('')
const topCategories = ref([])
const brandCategories = ref([])
const activeCategory = ref(0)
const sort = ref('')
const minPrice = ref('')
const maxPrice = ref('')
const goodsList = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = 20
const total = ref(0)

const fmtSales = (n) => {
  if (n >= 10000) return (n/10000).toFixed(1)+'w'
  if (n >= 1000) return (n/1000).toFixed(1)+'k'
  return n
}

const loadCategories = async () => {
  try {
    const data = await getCategoryTree()
    const tops = []
    const brands = []
    for (const p of data) {
      if (p.children?.length) {
        for (const c of p.children) {
          if (c.goods_count > 0) {
            if (c.children?.length) {
              // 有子分类 = 品牌级
              tops.push(c)
              for (const b of c.children) { if (b.goods_count > 0) brands.push(b) }
            } else {
              tops.push(c)
            }
          }
        }
      }
      if (p.goods_count > 0) tops.push(p)
    }
    topCategories.value = tops
    brandCategories.value = brands
  } catch (e) { console.error(e) }
}

const loadGoods = async () => {
  loading.value = true
  try {
    const params = { page: currentPage.value, pageSize }
    if (keyword.value) params.keyword = keyword.value
    if (activeCategory.value > 0) params.categoryId = activeCategory.value
    if (sort.value) params.sort = sort.value
    if (minPrice.value) params.minPrice = minPrice.value
    if (maxPrice.value) params.maxPrice = maxPrice.value
    const data = await getGoodsPage(params)
    goodsList.value = data.records || []
    total.value = data.total || 0
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

const applyPrice = () => { currentPage.value = 1; loadGoods() }

const pickCat = (id) => { activeCategory.value = id; currentPage.value = 1; loadGoods() }
const setSort = (s) => { sort.value = s; currentPage.value = 1; loadGoods() }
const onSearch = () => { currentPage.value = 1; loadGoods() }
const onPageChange = (p) => { currentPage.value = p; loadGoods() }
const goDetail = (id) => router.push(`/goods/${id}`)
const goLogin = () => { menuOpen.value = false; router.push('/login') }
const goRegister = () => { menuOpen.value = false; router.push('/register') }
const goOrders = () => { menuOpen.value = false; router.push('/orders') }
const goCart = () => { menuOpen.value = false; router.push('/cart') }
const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  userName.value = ''
  menuOpen.value = false
}

const menuOpen = ref(false)
const closeMenu = () => { menuOpen.value = false }

const showCat = ref(true)
const showBrand = ref(true)
const showPrice = ref(true)
const showSort = ref(true)

const userName = ref('')
const checkLogin = () => {
  const raw = localStorage.getItem('user')
  if (raw) {
    try { userName.value = JSON.parse(raw).nickname || JSON.parse(raw).email || '' }
    catch { userName.value = '' }
  }
}
onMounted(() => { loadCategories(); loadGoods(); checkLogin() })
</script>

<style scoped>
.steam-layout { display: flex; min-height: 100vh; background: #1b2838; font-family: 'Motiva Sans', 'PingFang SC', sans-serif; }

/* ===== SIDEBAR ===== */
.sidebar {
  width: 190px; flex-shrink: 0; background: linear-gradient(180deg, #16202d 0%, #141c28 100%);
  border-right: 1px solid #1e2f40;
  display: flex; flex-direction: column;
}
.side-logo { font-size: 20px; font-weight: 800; letter-spacing: -1px; margin-bottom: 4px; }
.c-o{color:#eb6f22}.c-c{color:#67c1f5}.c-y{color:#d4b83b}
.c-g{color:#5c7e10}.c-b{color:#2f7798}.c-p{color:#76428a}

.side-tagline { font-size: 10px; color: #4f6378; letter-spacing: 4px; text-transform: uppercase; }
.side-head { padding: 20px 16px 14px; text-align: center; background: linear-gradient(180deg, rgba(103,193,245,.05) 0%, transparent 100%); }
.side-divider { height: 1px; background: linear-gradient(90deg, transparent, #1e2f40 20%, #1e2f40 80%, transparent); }

.sec-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 14px 6px; cursor: pointer; user-select: none;
  font-size: 10px; color: #eb6f22; letter-spacing: 1.5px; font-weight: 600;
}
.sec-header:hover { color: #ff8a5c; }
.sec-arrow { font-size: 10px; color: #4f6378; transition: transform .2s; }
.sec-arrow.open { transform: rotate(180deg); }
.sec-body { padding-bottom: 4px; }

.side-item {
  padding: 7px 14px 7px 18px; font-size: 12px; color: #7a8a9a; cursor: pointer;
  border-left: 2px solid transparent; transition: all .15s;
}
.side-item:hover { color: #c9d1d9; background: rgba(103,193,245,.04); }
.side-item.sel { color: #67c1f5; border-left-color: #67c1f5; background: linear-gradient(90deg, rgba(103,193,245,.08) 0%, transparent 100%); }

.price-row { display: flex; align-items: center; gap: 6px; padding: 4px 14px; }
.price-inp { flex: 1; padding: 6px 8px; background: #1a2a3a; border: 1px solid #1e2f40; border-radius: 4px; color: #acb7c3; font-size: 11px; outline: none; min-width: 0; }
.price-inp:focus { border-color: #67c1f5; box-shadow: 0 0 0 2px rgba(103,193,245,.1); }
.price-inp::placeholder { color: #3d4f5f; }
.price-dash { color: #4f6378; font-size: 12px; flex-shrink: 0; }
.price-actions { display: flex; gap: 6px; padding: 6px 14px 2px; }
.btn-sm { flex: 1; padding: 5px 0; background: #67c1f5; border: none; border-radius: 4px; color: #1b2838; font-size: 11px; font-weight: 600; cursor: pointer; }
.btn-sm:hover { opacity: .85; }
.btn-sm.ghost { background: none; border: 1px solid #1e2f40; color: #4f6378; }
.btn-sm.ghost:hover { border-color: #4f6378; color: #acb7c3; }

.side-footer { margin-top: auto; padding: 14px 14px 0; border-top: 1px solid #1e2f40; }
.user-entry { font-size: 11px; color: #4f6378; cursor: pointer; }
.user-entry:hover { color: #67c1f5; }

/* ===== MAIN ===== */
.main { flex: 1; display: flex; flex-direction: column; height: 100vh; overflow-y: auto; }

/* Search Bar - Steam style */
.search-bar {
  display: flex; align-items: center; padding: 12px 16px;
  background: #16202d; border-bottom: 1px solid #1e2f40;
}
.search-inner {
  display: flex; align-items: center; background: #1a2a3a;
  border: 1px solid #1e2f40; border-radius: 3px; padding: 5px 10px;
  flex: 1; max-width: 600px;
}
.search-inner:hover { border-color: #67c1f5; }
.s-icon { color: #4f6378; margin-right: 6px; font-size: 14px; }
.search-inner input {
  flex: 1; background: none; border: none; outline: none;
  color: #acb7c3; font-size: 13px;
}
.search-inner input::placeholder { color: #3d4f5f; }
.result-info { margin-left: 16px; font-size: 12px; color: #4f6378; white-space: nowrap; }

/* User Menu */
.user-menu { position: relative; margin-left: auto; }
.user-trigger {
  display: flex; align-items: center; gap: 5px; padding: 4px 10px;
  background: #16202d; border: 1px solid #1e2f40; border-radius: 3px;
  cursor: pointer; white-space: nowrap;
}
.user-trigger:hover { border-color: #67c1f5; }
.u-icon { font-size: 14px; }
.u-label { font-size: 12px; color: #acb7c3; }

.user-drop {
  position: absolute; top: 100%; right: 0; margin-top: 4px;
  background: #16202d; border: 1px solid #1e2f40; border-radius: 4px;
  min-width: 150px; z-index: 50; overflow: hidden;
}
.drop-item {
  padding: 10px 16px; font-size: 13px; color: #acb7c3; cursor: pointer;
  transition: background .12s;
}
.drop-item:hover { background: #1e3348; color: #67c1f5; }
.drop-divider { height: 1px; background: #1e2f40; margin: 4px 0; }
.drop-item.logout { color: #eb6f22; }
.drop-item.logout:hover { color: #ff4444; }

.side-footer { margin-top: auto; padding: 16px 14px; text-align: center; background: linear-gradient(0deg, rgba(0,0,0,.2) 0%, transparent 100%); }
.copy { font-size: 10px; color: #4f6378; }
.copy-sub { font-size: 9px; color: #3d4f5f; margin-top: 2px; }

.loading { display: flex; justify-content: center; padding: 60px 0; }
.spin { width: 24px; height: 24px; border: 2px solid #1e2f40; border-top-color: #67c1f5; border-radius: 50%; animation: s .7s linear infinite; }
@keyframes s { to{transform:rotate(360deg)} }

/* ===== ITEM GRID ===== */
.item-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
  padding: 30px;
}

.grid-card {
  background: #1a2a3a;
  border: 1px solid #1e3348;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
}
.grid-card:hover {
  background: #1e3348;
  border-color: #67c1f5;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,.3);
}

.gc-img {
  position: relative;
  background: #0e1a26;
}
.gc-img img {
  width: 100%; aspect-ratio: 1.3; object-fit: cover; display: block;
}

.tag-hot {
  position: absolute; top: 5px; left: 5px;
  background: #eb6f22; color: #0d1117; font-size: 10px;
  padding: 2px 7px; border-radius: 2px; font-weight: 700;
}
.tag-new {
  position: absolute; top: 5px; right: 5px;
  background: #67c1f5; color: #0d1117; font-size: 10px;
  padding: 2px 7px; border-radius: 2px; font-weight: 700;
}

.gc-info { padding: 8px 10px 10px; }
.gc-name {
  font-size: 13px; color: #acb7c3; line-height: 1.35;
  display: -webkit-box; -webkit-line-clamp: 2;
  -webkit-box-orient: vertical; overflow: hidden;
  min-height: 34px;
}
.gc-row { display: flex; justify-content: space-between; align-items: baseline; margin-top: 6px; }
.gc-price { font-size: 15px; color: #a4d007; font-weight: 600; }
.gc-sales { font-size: 10px; color: #3d4f5f; }

.pagination-wrap { padding: 16px 0 32px; }
</style>
