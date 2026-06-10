<template>
  <div class="home-page">
    <!-- 顶部导航 -->
    <van-nav-bar title="Mini Mall" fixed placeholder>
      <template #right>
        <van-icon name="user-o" size="22" @click="goLogin" />
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
      <van-tabs
        v-model:active="activeCategory"
        swipeable animated shrink
        @change="onCategoryChange"
      >
        <van-tab title="全部" :name="0" />
        <van-tab v-for="cat in categories" :key="cat.id" :title="cat.name" :name="cat.id" />
      </van-tabs>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-wrap">
      <van-loading size="24" vertical>加载中...</van-loading>
    </div>

    <!-- 商品网格: 3列 -->
    <div v-else-if="goodsList.length > 0" class="goods-grid">
      <GoodsCard
        v-for="item in goodsList"
        :key="item.id"
        :goods="item"
        @click="goDetail(item.id)"
      />
    </div>

    <!-- 空 -->
    <van-empty v-else description="暂无商品" />

    <!-- 分页 -->
    <div v-if="total > pageSize" class="pagination-wrap">
      <van-pagination
        v-model="currentPage"
        :total-items="total"
        :items-per-page="pageSize"
        mode="simple"
        @change="onPageChange"
      />
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
    for (const parent of data) {
      if (parent.children?.length) {
        for (const child of parent.children) {
          if (child.goods_count > 0) flat.push(child)
        }
      }
      if (parent.goods_count > 0) flat.push(parent)
    }
    categories.value = flat
  } catch (e) { console.error('加载分类失败:', e) }
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
  } catch (e) {
    console.error('加载商品失败:', e)
  } finally {
    loading.value = false
  }
}

const onSearch = () => { currentPage.value = 1; loadGoods() }
const onClear = () => { keyword.value = ''; currentPage.value = 1; loadGoods() }
const onCategoryChange = () => { currentPage.value = 1; loadGoods() }
const onPageChange = (page) => { currentPage.value = page; loadGoods() }
const goDetail = (id) => router.push(`/goods/${id}`)
const goLogin = () => router.push('/login')

onMounted(() => { loadCategories(); loadGoods() })
</script>

<style scoped>
.home-page { background: #f5f5f5; min-height: 100vh; }

.search-wrap { padding: 6px 16px; background: #fff; }
.search-wrap :deep(.van-search__content) { background: #f7f8fa; }

.category-tabs { background: #fff; margin-bottom: 6px; }

.loading-wrap { display: flex; justify-content: center; padding: 80px 0; }

.goods-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  padding: 8px 10px;
}

.pagination-wrap {
  display: flex; justify-content: center; padding: 20px 0 30px;
}
</style>
