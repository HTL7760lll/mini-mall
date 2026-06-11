<template>
  <div class="detail-page" v-if="!loading">
    <header class="topbar">
      <div class="back-btn" @click="$router.back()">
        <span class="back-arrow">&#8592;</span>
        <span class="back-text">返回</span>
      </div>
      <span class="title">商品详情</span>
    </header>

    <template v-if="goods">
      <div class="detail-body">
        <!-- 左侧: 大图 -->
        <div class="left-panel">
          <img :src="`https://picsum.photos/400/400?random=${goods.id}`" class="main-img" />
        </div>

        <!-- 右侧: 信息 + 购买 -->
        <div class="right-panel">
          <div class="info-section">
            <!-- 标签 -->
            <div class="tags">
              <span v-if="goods.is_hot" class="tag-hot">HOT</span>
              <span v-if="goods.is_new" class="tag-new">NEW</span>
              <span class="tag-cat" v-if="goods.category_name">{{ goods.category_name }}</span>
            </div>

            <!-- 名称 -->
            <h1 class="p-name">{{ goods.name }}</h1>
            <p class="p-sub" v-if="goods.subtitle">{{ goods.subtitle }}</p>

            <!-- 价格 -->
            <div class="p-price">
              <span class="price-now">¥{{ selectedSku ? selectedSku.price : goods.price }}</span>
              <span class="price-old" v-if="goods.original_price">¥{{ goods.original_price }}</span>
            </div>

            <!-- 库存 -->
            <div class="p-stock">
              库存:
              <span :class="selectedSku?.stock > 0 ? 'in' : 'out'">
                {{ selectedSku ? selectedSku.stock : goods.stock }} 件
              </span>
              <span class="sold" v-if="goods.sales"> | 已售 {{ goods.sales }}</span>
            </div>
          </div>

          <!-- SKU -->
          <div class="sku-section" v-if="goods.skus?.length">
            <div class="sku-label">规格</div>
            <div class="sku-list">
              <div
                v-for="sku in goods.skus" :key="sku.id"
                class="sku-box"
                :class="{sel: selectedSku?.id === sku.id, off: sku.stock <= 0}"
                @click="selectSku(sku)"
              >
                {{ sku.specs }}
                <span class="sku-diff" v-if="sku.price !== goods.price">{{ sku.price > goods.price ? '+' : '' }}¥{{ (sku.price - goods.price).toFixed(0) }}</span>
              </div>
            </div>
          </div>

          <!-- 数量 + 加购 -->
          <div class="buy-row">
            <div class="qty-ctrl">
              <button class="q-btn" @click="qty = Math.max(1, qty - 1)">-</button>
              <span class="q-val">{{ qty }}</span>
              <button class="q-btn" @click="qty = Math.min(selectedSku?.stock || 1, qty + 1)">+</button>
            </div>
            <button class="add-cart-btn" :disabled="!selectedSku || selectedSku.stock <= 0" @click="handleAddCart">
              {{ !selectedSku ? '请选规格' : selectedSku.stock <= 0 ? '已售罄' : '加入购物车' }}
            </button>
          </div>

          <!-- 商品详情描述 -->
          <div class="desc-section" v-if="goods.detail">
            <div class="desc-title">商品详情</div>
            <div class="desc-content" v-html="goods.detail" />
          </div>
        </div>
      </div>
    </template>

    <div v-else class="empty">商品不存在</div>
  </div>

  <div v-else class="detail-page">
    <div class="loading"><div class="spin" /></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { showToast } from 'vant'
import request from '../../api/request'

const route = useRoute()
const goods = ref(null)
const loading = ref(true)
const selectedSku = ref(null)
const qty = ref(1)

const loadDetail = async () => {
  try {
    const data = await request.get(`/goods/detail/${route.params.id}/`)
    goods.value = data
    if (data.skus?.length) {
      const s = data.skus.find(x => x.stock > 0)
      if (s) selectedSku.value = s
    }
  } catch (e) { console.error(e); showToast('加载失败') }
  finally { loading.value = false }
}

const selectSku = (sku) => {
  if (sku.stock <= 0) return
  selectedSku.value = sku
  qty.value = 1
}

const handleAddCart = async () => {
  if (!selectedSku.value) return showToast('请选择规格')
  const token = localStorage.getItem('token')
  if (!token) return showToast('请先登录')
  try {
    await request.post('/cart/add/', {
      goods_id: goods.value.id,
      sku_id: selectedSku.value.id,
      quantity: qty.value,
    })
    showToast('已加入购物车')
  } catch (e) { console.error(e) }
}

onMounted(loadDetail)
</script>

<style scoped>
.detail-page { min-height: 100vh; background: #1b2838; }

.topbar {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  background: #16202d; border-bottom: 1px solid #1e2f40;
  position: sticky; top: 0; z-index: 10;
}
.back-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 14px; background: rgba(103,193,245,.08);
  border: 1px solid #1e2f40; border-radius: 4px;
  cursor: pointer; transition: all .15s;
}
.back-btn:hover { border-color: #67c1f5; background: rgba(103,193,245,.12); }
.back-arrow { font-size: 18px; color: #67c1f5; }
.back-text { font-size: 13px; color: #67c1f5; }
.title { color: #acb7c3; font-size: 14px; font-weight: 600; }

.loading { display: flex; justify-content: center; padding: 120px 0; }
.spin { width: 32px; height: 32px; border: 2px solid #1e2f40; border-top-color: #ff6b35; border-radius: 50%; animation: s .8s linear infinite; }
@keyframes s { to{transform:rotate(360deg)} }

.empty { text-align: center; padding: 80px 0; color: #4f6378; }

/* 左右两栏 */
.detail-body {
  display: flex; gap: 24px; padding: 20px; max-width: 960px;
  margin: 0 auto;
}
.left-panel { flex-shrink: 0; width: 360px; }
.main-img { width: 100%; border-radius: 6px; background: #0e1a26; display: block; }

.right-panel { flex: 1; min-width: 0; }

.info-section { margin-bottom: 20px; }
.tags { display: flex; gap: 6px; align-items: center; margin-bottom: 8px; }
.tag-hot { background: #eb6f22; color: #1b2838; font-size: 10px; padding: 2px 7px; border-radius: 2px; font-weight: 700; }
.tag-new { background: #67c1f5; color: #1b2838; font-size: 10px; padding: 2px 7px; border-radius: 2px; font-weight: 700; }
.tag-cat { font-size: 11px; color: #4f6378; background: #1a2a3a; padding: 2px 8px; border-radius: 2px; }

.p-name { font-size: 20px; color: #e6e6e6; font-weight: 700; line-height: 1.3; }
.p-sub { font-size: 13px; color: #7a8a9a; margin-top: 6px; }
.p-price { display: flex; align-items: baseline; gap: 10px; margin-top: 16px; }
.price-now { font-size: 26px; color: #a4d007; font-weight: 700; }
.price-old { font-size: 14px; color: #4f6378; text-decoration: line-through; }
.p-stock { font-size: 13px; color: #7a8a9a; margin-top: 8px; }
.in { color: #a4d007; } .out { color: #eb6f22; }
.sold { color: #4f6378; }

/* SKU */
.sku-section { margin-bottom: 20px; }
.sku-label { font-size: 13px; color: #acb7c3; font-weight: 600; margin-bottom: 8px; }
.sku-list { display: flex; flex-wrap: wrap; gap: 8px; }
.sku-box {
  padding: 7px 14px; border: 1px solid #1e2f40; border-radius: 4px;
  font-size: 13px; color: #acb7c3; cursor: pointer; transition: all .15s;
  background: #16202d;
}
.sku-box:hover { border-color: #67c1f5; }
.sku-box.sel { border-color: #67c1f5; color: #67c1f5; background: rgba(103,193,245,.08); }
.sku-box.off { color: #3d4f5f; border-color: #1e2f40; cursor: not-allowed; text-decoration: line-through; opacity: .5; }
.sku-diff { font-size: 11px; color: #a4d007; margin-left: 4px; }

/* 购买 */
.buy-row { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
.qty-ctrl { display: flex; align-items: center; border: 1px solid #1e2f40; border-radius: 4px; overflow: hidden; }
.q-btn {
  width: 34px; height: 34px; background: #1a2a3a; border: none;
  color: #acb7c3; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center;
}
.q-btn:hover { background: #1e3348; }
.q-val { width: 44px; text-align: center; font-size: 15px; color: #acb7c3; font-weight: 600; }

.add-cart-btn {
  flex: 1; padding: 10px 0; background: linear-gradient(135deg, #a4d007, #5c7e10);
  border: none; border-radius: 4px; color: #1b2838; font-size: 15px; font-weight: 700;
  cursor: pointer; transition: opacity .15s;
}
.add-cart-btn:hover { opacity: .9; }
.add-cart-btn:disabled { opacity: .3; cursor: not-allowed; background: #1e2f40; color: #4f6378; }

/* 描述 */
.desc-section { border-top: 1px solid #1e2f40; padding-top: 20px; }
.desc-title { font-size: 14px; color: #acb7c3; font-weight: 600; margin-bottom: 12px; }
.desc-content { font-size: 13px; color: #7a8a9a; line-height: 1.8; }
.desc-content :deep(img) { max-width: 100%; border-radius: 4px; }
</style>
