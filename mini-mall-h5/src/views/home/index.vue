<template>
  <div class="app-layout">
    <!-- 侧边栏: 常驻 -->
    <aside class="sidebar">
      <div class="side-logo">
        <span class="s-m">M</span><span class="s-i">i</span><span class="s-n">n</span><span class="s-i2">i</span>
        <span class="s-m2">M</span><span class="s-a">a</span><span class="s-ll">ll</span>
      </div>
      <div class="side-label">CATEGORY</div>
      <div class="side-item" :class="{active: activeCategory===0}" @click="pickCat(0)">ALL</div>
      <div class="side-item" v-for="c in categories" :key="c.id"
        :class="{active: activeCategory===c.id}" @click="pickCat(c.id)">
        {{ c.name }}
      </div>
      <div class="side-footer">
        <div class="user-entry" @click="goLogin">&#9786; LOGIN</div>
      </div>
    </aside>

    <!-- 主内容 -->
    <div class="content-area">
      <!-- 顶栏 -->
      <header class="topbar">
        <div class="search-box">
          <input v-model="keyword" placeholder="SEARCH" @keyup.enter="onSearch" />
          <span class="s-icon" @click="onSearch">&#8981;</span>
        </div>
      </header>

      <!-- 加载 -->
      <div v-if="loading" class="loading-wrap"><div class="spinner" /></div>

      <!-- 商品流 -->
      <div v-else class="goods-flow">
        <GoodsCard v-for="item in goodsList" :key="item.id" :goods="item" @click="goDetail(item.id)" />
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
import GoodsCard from '../../components/GoodsCard.vue'

const router = useRouter()
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

const pickCat = (id) => { activeCategory.value = id; currentPage.value = 1; loadGoods() }
const onSearch = () => { currentPage.value = 1; loadGoods() }
const onPageChange = (p) => { currentPage.value = p; loadGoods() }
const goDetail = (id) => router.push(`/goods/${id}`)
const goLogin = () => router.push('/login')

onMounted(() => { loadCategories(); loadGoods() })
</script>

<style scoped>
.app-layout { display: flex; min-height: 100vh; background: #0d1117; }

/* SIDEBAR - 常驻 */
.sidebar {
  width: 140px; flex-shrink: 0;
  background: #0d1117; border-right: 1px solid #21262d;
  padding: 20px 0; display: flex; flex-direction: column;
  position: sticky; top:0; height: 100vh; overflow-y: auto;
}
.side-logo { text-align: center; font-size: 18px; font-weight: 800; letter-spacing: -1px; margin-bottom: 20px; }
.s-m{color:#ff6b35}.s-i,.s-i2{color:#00d4ff}.s-n{color:#ffd700}
.s-m2{color:#4caf50}.s-a{color:#2196f3}.s-ll{color:#9c27b0}

.side-label { font-size: 9px; color: #ff6b35; padding: 0 12px 8px; letter-spacing: 2px; font-weight: 600; }
.side-item {
  padding: 7px 12px; font-size: 12px; color: #8b949e; cursor: pointer;
  border-left: 2px solid transparent; transition: all .15s;
}
.side-item:hover { color: #c9d1d9; background: #161b22; }
.side-item.active { color: #ff6b35; border-left-color: #ff6b35; background: rgba(255,107,53,.06); }

.side-footer { margin-top: auto; padding: 16px 12px; border-top: 1px solid #21262d; }
.user-entry { font-size: 11px; color: #484f58; cursor: pointer; }
.user-entry:hover { color: #c9d1d9; }

/* CONTENT */
.content-area { flex: 1; display: flex; flex-direction: column; }

.topbar { padding: 10px 14px; border-bottom: 1px solid #21262d; position: sticky; top:0; background: #0d1117; z-index:5; }
.search-box { display: flex; align-items: center; border-bottom: 1px solid #21262d; padding: 4px 0; }
.search-box input {
  flex:1; background: none; border: none; outline: none; color: #c9d1d9;
  font-size: 13px; letter-spacing: 1px;
}
.search-box input::placeholder { color: #30363d; }
.s-icon { color: #484f58; cursor: pointer; font-size: 15px; }

.loading-wrap { display: flex; justify-content: center; padding: 80px 0; }
.spinner { width: 28px; height: 28px; border: 2px solid #21262d; border-top-color: #ff6b35; border-radius: 50%; animation: spin .8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* 流式网格: 小格子自然排列填满 */
.goods-flow {
  display: flex; flex-wrap: wrap;
  padding: 8px;
}
.goods-flow :deep(.goods-card) {
  width: calc(25% - 4px);
  margin: 2px;
}

.pagination-wrap { padding: 16px 0 32px; }
</style>
