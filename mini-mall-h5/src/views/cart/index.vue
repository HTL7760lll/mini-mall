<template>
  <div class="cart-page" v-if="!needLogin">
    <header class="topbar">
      <span class="back" @click="$router.push('/')">&#8592;</span>
      <span class="title">购物车</span>
      <span class="count" v-if="cartItems.length">{{ cartItems.length }} 件</span>
    </header>

    <!-- 加载 -->
    <div v-if="loading" class="loading"><div class="spin" /></div>

    <!-- 列表 -->
    <div v-else-if="cartItems.length" class="cart-list">
      <div class="cart-item" v-for="item in cartItems" :key="item.id">
        <img :src="`https://picsum.photos/120/120?random=${item.goods_id}`" class="ci-img" />
        <div class="ci-body">
          <div class="ci-name">{{ item.goods_name }}</div>
          <div class="ci-specs" v-if="item.sku_specs">{{ item.sku_specs }}</div>
          <div class="ci-meta">
            <span class="ci-price">¥{{ item.price }}</span>
            <span class="ci-subtotal">小计 ¥{{ (item.price * item.quantity).toFixed(2) }}</span>
          </div>
          <div class="ci-actions">
            <div class="qty-ctrl">
              <button class="qty-btn" @click="changeQty(item, item.quantity - 1)" :disabled="item.quantity <= 1">-</button>
              <span class="qty-val">{{ item.quantity }}</span>
              <button class="qty-btn" @click="changeQty(item, item.quantity + 1)">+</button>
            </div>
            <button class="del-btn" @click="removeItem(item)">删除</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 空 -->
    <div v-else class="empty">
      <div class="empty-icon">🛒</div>
      <div class="empty-text">购物车是空的</div>
      <button class="go-shop" @click="$router.push('/')">去逛逛</button>
    </div>

    <!-- 底部结算栏 -->
    <div class="footer-bar" v-if="cartItems.length">
      <div class="footer-total">
        <span>合计</span>
        <span class="total-price">¥{{ totalPrice.toFixed(2) }}</span>
      </div>
      <button class="submit-btn" @click="goSubmit">提交订单</button>
    </div>
  </div>

  <!-- 未登录 -->
  <div class="cart-page" v-else>
    <header class="topbar">
      <span class="back" @click="$router.push('/')">&#8592;</span>
      <span class="title">购物车</span>
    </header>
    <div class="empty">
      <div class="empty-icon">&#128274;</div>
      <div class="empty-text">请先登录查看购物车</div>
      <button class="go-shop" @click="$router.push('/login')">去登录</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import request from '../../api/request'

const router = useRouter()
const cartItems = ref([])
const loading = ref(false)
const needLogin = ref(false)

const totalPrice = computed(() =>
  cartItems.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
)

const loadCart = async () => {
  loading.value = true
  try {
    const data = await request.get('/cart/list/')
    cartItems.value = data?.records || []
  } catch (e) {
    if (e.response?.status === 401) {
      needLogin.value = true
    } else {
      console.error('加载购物车失败:', e)
    }
  } finally {
    loading.value = false
  }
}

const changeQty = async (item, newQty) => {
  if (newQty <= 0) return removeItem(item)
  try {
    await request.put('/cart/update/', { cart_id: item.id, quantity: newQty })
    item.quantity = newQty
  } catch (e) {
    showToast('修改失败')
  }
}

const removeItem = async (item) => {
  try {
    await request.delete(`/cart/remove/${item.id}/`)
    cartItems.value = cartItems.value.filter(c => c.id !== item.id)
    showToast('已删除')
  } catch (e) {
    console.error('删除失败:', e)
  }
}

const goSubmit = () => {
  showToast('订单提交功能开发中')
}

onMounted(loadCart)
</script>

<style scoped>
.cart-page { min-height: 100vh; background: #1b2838; padding-bottom: 80px; }

.topbar {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  background: #16202d; border-bottom: 1px solid #1e2f40;
  position: sticky; top: 0; z-index: 10;
}
.back { color: #67c1f5; cursor: pointer; font-size: 18px; }
.title { color: #acb7c3; font-size: 15px; font-weight: 600; }
.count { margin-left: auto; font-size: 12px; color: #4f6378; }

.loading { display: flex; justify-content: center; padding: 80px 0; }
.spin { width: 28px; height: 28px; border: 2px solid #1e2f40; border-top-color: #ff6b35; border-radius: 50%; animation: s .8s linear infinite; }
@keyframes s { to { transform: rotate(360deg); } }

/* 列表 */
.cart-list { padding: 8px 12px; }
.cart-item {
  display: flex; gap: 10px; background: #16202d; border: 1px solid #1e2f40;
  border-radius: 4px; padding: 10px; margin-bottom: 8px;
}
.ci-img { width: 90px; height: 90px; border-radius: 4px; object-fit: cover; background: #0e1a26; flex-shrink: 0; }
.ci-body { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.ci-name { font-size: 14px; color: #acb7c3; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ci-specs { font-size: 11px; color: #4f6378; margin-top: 2px; }
.ci-meta { display: flex; justify-content: space-between; align-items: baseline; margin-top: 8px; }
.ci-price { font-size: 14px; color: #a4d007; font-weight: 600; }
.ci-subtotal { font-size: 11px; color: #4f6378; }

.ci-actions { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; }

.qty-ctrl { display: flex; align-items: center; gap: 0; border-radius: 4px; overflow: hidden; border: 1px solid #1e2f40; }
.qty-btn {
  width: 30px; height: 28px; background: #1a2a3a; border: none;
  color: #acb7c3; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center;
}
.qty-btn:hover { background: #1e3348; }
.qty-btn:disabled { opacity: .3; cursor: not-allowed; }
.qty-val { width: 36px; text-align: center; color: #acb7c3; font-size: 14px; font-weight: 600; }

.del-btn { background: none; border: 1px solid #3d4f5f; color: #4f6378; padding: 5px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; }
.del-btn:hover { border-color: #eb6f22; color: #eb6f22; }

/* 空态 */
.empty { text-align: center; padding: 80px 20px; }
.empty-icon { font-size: 48px; margin-bottom: 12px; }
.empty-text { font-size: 14px; color: #4f6378; margin-bottom: 20px; }
.go-shop { background: #67c1f5; border: none; color: #1b2838; padding: 8px 32px; border-radius: 4px; font-size: 14px; font-weight: 600; cursor: pointer; }
.go-shop:hover { opacity: .85; }

/* 底部 */
.footer-bar {
  position: fixed; bottom: 0; left: 190px; right: 0;
  background: #16202d; border-top: 1px solid #1e2f40;
  padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;
  z-index: 20;
}
.footer-total { display: flex; gap: 12px; align-items: baseline; color: #acb7c3; font-size: 14px; }
.total-price { font-size: 20px; color: #a4d007; font-weight: 700; }
.submit-btn { background: linear-gradient(135deg, #67c1f5, #2f7798); border: none; color: #fff; padding: 10px 32px; border-radius: 4px; font-size: 14px; font-weight: 600; cursor: pointer; }
.submit-btn:hover { opacity: .9; }
</style>
