<template>
  <div class="steam-layout">
    <!-- 左侧栏 -->
    <aside class="sidebar">
      <div class="side-logo">
        <span class="c-o">M</span><span class="c-c">i</span><span class="c-y">n</span><span class="c-c">i</span>
        <span class="c-g">M</span><span class="c-b">a</span><span class="c-p">ll</span>
      </div>
      <div class="side-label">SHOWING</div>
      <div class="side-item" :class="{sel: activeCategory===0}" @click="pickCat(0)">All Items</div>
      <div class="side-item" v-for="c in categories" :key="c.id"
        :class="{sel: activeCategory===c.id}" @click="pickCat(c.id)">
        {{ c.name }}
      </div>

      <div class="side-label" style="margin-top:16px">SORT BY</div>
      <div class="side-item" :class="{sel: sort===''}" @click="setSort('')">Default</div>
      <div class="side-item" :class="{sel: sort==='price_asc'}" @click="setSort('price_asc')">Price: Low to High</div>
      <div class="side-item" :class="{sel: sort==='price_desc'}" @click="setSort('price_desc')">Price: High to Low</div>
      <div class="side-item" :class="{sel: sort==='sales'}" @click="setSort('sales')">Best Selling</div>

      <div class="side-footer">
        <div class="user-entry" @click="goLogin">&#9786; SIGN IN</div>
      </div>
    </aside>

    <!-- 右侧主区 -->
    <div class="main">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <div class="search-inner">
          <span class="s-icon">&#8981;</span>
          <input v-model="keyword" placeholder="Search the market" @keyup.enter="onSearch" />
        </div>
        <div class="result-info">{{ total }} results</div>
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
const categories = ref([])
const activeCategory = ref(0)
const sort = ref('')
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
    if (sort.value) params.sort = sort.value
    const data = await getGoodsPage(params)
    goodsList.value = data.records || []
    total.value = data.total || 0
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

const pickCat = (id) => { activeCategory.value = id; currentPage.value = 1; loadGoods() }
const setSort = (s) => { sort.value = s; currentPage.value = 1; loadGoods() }
const onSearch = () => { currentPage.value = 1; loadGoods() }
const onPageChange = (p) => { currentPage.value = p; loadGoods() }
const goDetail = (id) => router.push(`/goods/${id}`)
const goLogin = () => router.push('/login')

onMounted(() => { loadCategories(); loadGoods() })
</script>

<style scoped>
.steam-layout { display: flex; min-height: 100vh; background: #1b2838; font-family: 'Motiva Sans', 'PingFang SC', sans-serif; }

/* ===== SIDEBAR ===== */
.sidebar {
  width: 190px; flex-shrink: 0; background: #16202d;
  border-right: 1px solid #1e2f40; padding: 16px 0;
  display: flex; flex-direction: column;
}
.side-logo { text-align: center; font-size: 18px; font-weight: 800; letter-spacing: -1px; margin-bottom: 18px; }
.c-o{color:#eb6f22}.c-c{color:#67c1f5}.c-y{color:#d4b83b}
.c-g{color:#5c7e10}.c-b{color:#2f7798}.c-p{color:#76428a}

.side-label { font-size: 10px; color: #eb6f22; padding: 0 14px 6px; letter-spacing: 2px; font-weight: 600; text-transform: uppercase; }
.side-item {
  padding: 6px 14px; font-size: 12px; color: #7a8a9a; cursor: pointer;
  border-left: 2px solid transparent; transition: all .12s;
}
.side-item:hover { color: #acb7c3; background: rgba(255,255,255,.03); }
.side-item.sel { color: #67c1f5; border-left-color: #67c1f5; background: rgba(103,193,245,.06); }

.side-footer { margin-top: auto; padding: 14px 14px 0; border-top: 1px solid #1e2f40; }
.user-entry { font-size: 11px; color: #4f6378; cursor: pointer; }
.user-entry:hover { color: #67c1f5; }

/* ===== MAIN ===== */
.main { flex: 1; display: flex; flex-direction: column; }

/* Search Bar - Steam style */
.search-bar {
  display: flex; align-items: center; padding: 12px 16px;
  background: #16202d; border-bottom: 1px solid #1e2f40;
}
.search-inner {
  display: flex; align-items: center; background: #1a2a3a;
  border: 1px solid #1e2f40; border-radius: 3px; padding: 5px 10px;
  flex: 1; max-width: 400px;
}
.search-inner:hover { border-color: #67c1f5; }
.s-icon { color: #4f6378; margin-right: 6px; font-size: 14px; }
.search-inner input {
  flex: 1; background: none; border: none; outline: none;
  color: #acb7c3; font-size: 13px;
}
.search-inner input::placeholder { color: #3d4f5f; }
.result-info { margin-left: 16px; font-size: 12px; color: #4f6378; white-space: nowrap; }

.loading { display: flex; justify-content: center; padding: 60px 0; }
.spin { width: 24px; height: 24px; border: 2px solid #1e2f40; border-top-color: #67c1f5; border-radius: 50%; animation: s .7s linear infinite; }
@keyframes s { to{transform:rotate(360deg)} }

/* ===== ITEM GRID ===== */
.item-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  padding: 12px;
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
