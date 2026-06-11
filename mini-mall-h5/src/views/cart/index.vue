<template>
  <div class="page-dark">
    <header class="topbar">
      <span class="back" @click="$router.push('/')">&#8592;</span>
      <span class="title">购物车</span>
    </header>
    <div class="cart-list">
      <div v-for="c in cartItems" :key="c.id" class="cart-item">
        <img :src="`https://picsum.photos/80/80?random=${c.goods_id}`" class="ci-img" />
        <div class="ci-info">
          <div class="ci-name">{{ c.goods_name }}</div>
          <div class="ci-specs">{{ c.sku_specs }}</div>
          <div class="ci-price">¥{{ c.price }} x {{ c.quantity }}</div>
        </div>
      </div>
      <div v-if="!cartItems.length" class="empty">购物车是空的</div>
    </div>
    <div class="cart-footer" v-if="cartItems.length">
      <span>共 {{ cartItems.length }} 件</span>
      <button class="btn-checkout" disabled>去结算</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api/request'

const cartItems = ref([])

onMounted(async () => {
  try { const d = await request.get('/cart/list/'); cartItems.value = d || [] }
  catch (e) { console.error(e) }
})
</script>

<style scoped>
.page-dark { min-height:100vh; background:#1b2838; }
.topbar {
  display:flex; align-items:center; gap:12px; padding:12px 16px;
  background:#16202d; border-bottom:1px solid #1e2f40;
}
.back { color:#67c1f5; cursor:pointer; font-size:18px; }
.title { color:#acb7c3; font-size:15px; font-weight:600; }

.cart-list { padding:8px 12px; }
.cart-item {
  display:flex; gap:12px; background:#16202d; border:1px solid #1e2f40;
  border-radius:4px; padding:10px; margin-bottom:6px;
}
.ci-img { width:80px; height:80px; border-radius:4px; object-fit:cover; background:#0e1a26; }
.ci-info { flex:1; }
.ci-name { font-size:13px; color:#acb7c3; }
.ci-specs { font-size:11px; color:#4f6378; margin-top:4px; }
.ci-price { font-size:14px; color:#a4d007; font-weight:600; margin-top:8px; }
.empty { text-align:center; padding:60px 0; color:#4f6378; }

.cart-footer {
  position:fixed; bottom:0; left:190px; right:0;
  background:#16202d; border-top:1px solid #1e2f40;
  padding:12px 16px; display:flex; justify-content:space-between; align-items:center;
  color:#acb7c3; font-size:13px;
}
.btn-checkout {
  background:#a4d007; color:#1b2838; border:none; padding:8px 24px;
  border-radius:3px; font-weight:700; font-size:14px; cursor:pointer;
}
.btn-checkout:disabled { opacity:.3; }
</style>
