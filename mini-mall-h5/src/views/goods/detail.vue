<template>
  <div class="detail-page">
    <!-- 导航栏 -->
    <van-nav-bar title="商品详情" left-text="返回" left-arrow fixed placeholder @click-left="goBack" />

    <!-- 加载中 -->
    <div v-if="loading" class="loading-wrap">
      <van-loading size="24" vertical>加载中...</van-loading>
    </div>

    <template v-else-if="goods">
      <!-- 大图 -->
      <div class="main-image-wrap">
        <van-image
          :src="goods.main_image || 'https://picsum.photos/seed/default/400/400'"
          fit="cover"
          width="100%"
          height="320"
        />
      </div>

      <!-- 商品基本信息 -->
      <div class="info-section">
        <!-- 标签 -->
        <div class="info-tags">
          <van-tag v-if="goods.is_hot" type="danger" size="medium">Hot</van-tag>
          <van-tag v-if="goods.is_new" type="primary" size="medium" style="margin-left:6px">New</van-tag>
          <span class="info-category" v-if="goods.category_name">{{ goods.category_name }}</span>
        </div>

        <!-- 名称 -->
        <h1 class="info-name">{{ goods.name }}</h1>

        <!-- 副标题/描述 -->
        <p class="info-subtitle" v-if="goods.subtitle">{{ goods.subtitle }}</p>

        <!-- 价格 -->
        <div class="info-price">
          <span class="price-current">¥{{ selectedSku ? selectedSku.price : goods.price }}</span>
          <span class="price-original" v-if="goods.original_price">¥{{ goods.original_price }}</span>
        </div>

        <!-- 库存 -->
        <div class="info-stock">
          <span v-if="selectedSku">
            库存: <span :class="selectedSku.stock > 0 ? 'in-stock' : 'out-stock'">{{ selectedSku.stock }}</span> 件
          </span>
          <span v-else>总库存: {{ goods.stock }} 件</span>
          <span class="info-sales" v-if="goods.sales"> | 已售 {{ goods.sales }}</span>
        </div>
      </div>

      <!-- SKU 选择 -->
      <div class="sku-section" v-if="goods.skus && goods.skus.length > 0">
        <div class="section-title">选择规格</div>
        <div class="sku-list">
          <div
            v-for="sku in goods.skus"
            :key="sku.id"
            class="sku-item"
            :class="{ active: selectedSku?.id === sku.id, disabled: sku.stock <= 0 }"
            @click="selectSku(sku)"
          >
            <span>{{ sku.specs }}</span>
            <span class="sku-price" v-if="sku.price !== goods.price">¥{{ sku.price }}</span>
          </div>
        </div>
      </div>

      <!-- 商品详情（富文本） -->
      <div class="detail-section" v-if="goods.detail">
        <div class="section-title">商品详情</div>
        <div class="detail-content" v-html="goods.detail" />
      </div>

      <!-- 底部安全占位 -->
      <div style="height: 80px" />
    </template>

    <!-- 空状态 -->
    <van-empty v-else description="商品不存在" />

    <!-- 底部操作栏 -->
    <div class="bottom-bar" v-if="goods">
      <van-stepper v-model="quantity" :min="1" :max="selectedSku?.stock || 1" integer />
      <van-button
        type="danger"
        size="large"
        round
        block
        class="cart-btn"
        :disabled="!selectedSku || selectedSku.stock <= 0"
        @click="addCart"
      >
        加入购物车
      </van-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import { getGoodsDetail, addToCart } from '../../api/goods'

const route = useRoute()
const router = useRouter()

const goods = ref(null)
const loading = ref(false)
const selectedSku = ref(null)
const quantity = ref(1)

const loadDetail = async () => {
  loading.value = true
  try {
    const data = await getGoodsDetail(route.params.id)
    goods.value = data
    // 自动选第一个有库存的 SKU
    if (data.skus?.length) {
      const inStock = data.skus.find(s => s.stock > 0)
      if (inStock) selectedSku.value = inStock
    }
  } catch {
    showToast('加载失败')
  } finally {
    loading.value = false
  }
}

const selectSku = (sku) => {
  if (sku.stock <= 0) return
  selectedSku.value = sku
  quantity.value = 1
}

const addCart = async () => {
  if (!selectedSku.value) {
    showToast('请选择商品规格')
    return
  }
  const token = localStorage.getItem('token')
  if (!token) {
    showToast('请先登录')
    return
  }
  try {
    await addToCart({
      goods_id: goods.value.id,
      sku_id: selectedSku.value.id,
      quantity: quantity.value,
    })
    showToast('已加入购物车')
  } catch {
    // showToast already in interceptor
  }
}

const goBack = () => {
  router.back()
}

onMounted(loadDetail)
</script>

<style scoped>
.detail-page {
  background: #f5f5f5;
  min-height: 100vh;
}

.loading-wrap {
  display: flex;
  justify-content: center;
  padding: 80px 0;
}

/* 大图 */
.main-image-wrap {
  background: #fff;
}

/* 基本信息 */
.info-section {
  background: #fff;
  padding: 14px 16px;
  margin-bottom: 10px;
}

.info-tags {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}
.info-category {
  font-size: 11px;
  color: #999;
  margin-left: 8px;
  background: #f0f0f0;
  border-radius: 3px;
  padding: 1px 6px;
}

.info-name {
  font-size: 20px;
  font-weight: 700;
  color: #111;
  line-height: 1.4;
  margin-bottom: 6px;
}

.info-subtitle {
  font-size: 13px;
  color: #888;
  margin-bottom: 10px;
  line-height: 1.5;
}

.info-price {
  display: flex;
  align-items: baseline;
  margin-bottom: 8px;
}
.price-current {
  font-size: 26px;
  color: #ee0a24;
  font-weight: 700;
}
.price-original {
  font-size: 14px;
  color: #ccc;
  text-decoration: line-through;
  margin-left: 10px;
}

.info-stock {
  font-size: 13px;
  color: #666;
}
.in-stock { color: #07c160; }
.out-stock { color: #ee0a24; }
.info-sales { color: #bbb; }

/* SKU 选择 */
.sku-section {
  background: #fff;
  padding: 14px 16px;
  margin-bottom: 10px;
}
.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}
.sku-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.sku-item {
  padding: 6px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 13px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
  background: #fafafa;
}
.sku-item .sku-price {
  color: #ee0a24;
  margin-left: 6px;
  font-size: 12px;
}
.sku-item.active {
  border-color: #ee0a24;
  color: #ee0a24;
  background: #fff5f5;
}
.sku-item.disabled {
  color: #ccc;
  background: #f5f5f5;
  cursor: not-allowed;
}

/* 商品详情 */
.detail-section {
  background: #fff;
  padding: 14px 16px;
}
.detail-content {
  font-size: 14px;
  color: #555;
  line-height: 1.8;
}
.detail-content :deep(img) {
  max-width: 100%;
}

/* 底部操作栏 */
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.06);
  z-index: 100;
}
.cart-btn {
  flex: 1;
}
</style>
