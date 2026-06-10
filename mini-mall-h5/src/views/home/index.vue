<template>
  <div class="home-page">
    <!-- 导航 + Logo -->
    <van-nav-bar fixed placeholder>
      <template #title>
        <div class="nav-logo">
          <span class="logo-m">M</span>
          <span class="logo-i">i</span>
          <span class="logo-n1">n</span>
          <span class="logo-i2">i</span>
          <span class="logo-space">&nbsp;</span>
          <span class="logo-m2">M</span>
          <span class="logo-a">a</span>
          <span class="logo-ll">ll</span>
        </div>
      </template>
      <template #right>
        <div class="login-btn" @click="goLogin">
          <van-icon name="user-o" size="18" />
          <span>登录</span>
        </div>
      </template>
    </van-nav-bar>

    <!-- 搜索栏 -->
    <div class="search-wrap">
      <van-search
        v-model="keyword"
        placeholder="搜索商品"
        shape="round"
        @search="onSearch"
        @clear="onClear"
      />
    </div>

    <!-- 分类标签 -->
    <div class="category-tabs">
      <van-tabs v-model:active="activeCategory" swipeable animated shrink @change="onCategoryChange">
        <van-tab title="全部" :name="0" />
        <van-tab v-for="cat in categories" :key="cat.id" :title="cat.name" :name="cat.id" />
      </van-tabs>
    </div>

    <!-- 加载 -->
    <div v-if="loading" class="loading-wrap">
      <van-loading size="24" vertical>加载中...</van-loading>
    </div>

    <!-- 商品网格 -->
    <div v-else-if="goodsList.length > 0" class="goods-grid">
      <GoodsCard
        v-for="item in goodsList"
        :key="item.id"
        :goods="item"
        @click="goDetail(item.id)"
      />
    </div>

    <van-empty v-else description="暂无商品" />

    <!-- 分页 -->
    <div v-if="total > pageSize" class="pagination-wrap">
      <van-pagination v-model="currentPage" :total-items="total" :items-per-page="pageSize" mode="simple" @change="onPageChange" />
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
const pageSize = 21
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
    const params = { page: currentPage.value, pageSize: pageSize }
    if (keyword.value) params.keyword = keyword.value
    if (activeCategory.value > 0) params.categoryId = activeCategory.value
    const data = await getGoodsPage(params)
    goodsList.value = data.records || []
    total.value = data.total || 0
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

const onSearch = () => { currentPage.value = 1; loadGoods() }
const onClear = () => { keyword.value = ''; currentPage.value = 1; loadGoods() }
const onCategoryChange = () => { currentPage.value = 1; loadGoods() }
const onPageChange = (p) => { currentPage.value = p; loadGoods() }
const goDetail = (id) => router.push(`/goods/${id}`)
const goLogin = () => router.push('/login')

onMounted(() => { loadCategories(); loadGoods() })
</script>

<style scoped>
.home-page { background: #f5f5f5; min-height: 100vh; }

/* 彩色 Logo */
.nav-logo {
  display: flex; align-items: center; font-weight: 800; font-size: 30px;
  letter-spacing: -1px; line-height: 1;
}
.logo-m  { color: #ee0a24; text-shadow: 2px 2px 0 #ffcccc; }
.logo-i  { color: #ff6b35; }
.logo-n1 { color: #f7931e; }
.logo-i2 { color: #00bcd4; }
.logo-space { width: 4px; }
.logo-m2 { color: #4caf50; text-shadow: 2px 2px 0 #c8e6c9; }
.logo-a  { color: #2196f3; }
.logo-ll { color: #9c27b0; }

.search-wrap { padding: 6px 12px; }
.search-wrap :deep(.van-search) { padding: 4px 0; }
.search-wrap :deep(.van-search__content) { background: #f7f8fa; }

.category-tabs { background: #fff; margin-bottom: 6px; }
.loading-wrap { padding: 80px 0; text-align: center; }

/* 4列固定 */
.goods-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
  padding: 6px 24px;
}

.login-btn {
  display: flex; align-items: center; gap: 3px;
  font-size: 11px; color: #666; cursor: pointer;
}
.pagination-wrap { padding: 20px 0 30px; }
</style>
