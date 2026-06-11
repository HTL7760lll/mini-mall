<template>
  <div class="page-dark">
    <header class="topbar">
      <span class="back" @click="$router.push('/')">&#8592;</span>
      <span class="title">我的订单</span>
    </header>
    <div class="order-list">
      <div v-for="o in orders" :key="o.id" class="order-item" @click="showDetail(o.id)">
        <div class="o-head">
          <span class="o-no">#{{ o.order_no }}</span>
          <span class="o-status">{{ o.order_status_desc }}</span>
        </div>
        <div class="o-body">
          <div class="o-addr">{{ o.receiver_name }} / {{ o.receiver_phone }}</div>
          <div class="o-price">¥{{ o.pay_amount }}</div>
        </div>
        <div class="o-time">{{ o.created_at?.split('T')[0] }}</div>
      </div>
      <div v-if="!orders.length" class="empty">暂无订单</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api/request'

const orders = ref([])

onMounted(async () => {
  try { const d = await request.get('/order/page/'); orders.value = d.records || [] }
  catch (e) { console.error(e) }
})

const showDetail = (id) => { /* TODO */ }
</script>

<style scoped>
.page-dark { min-height:100vh; background:#1b2838; }
.topbar {
  display:flex; align-items:center; gap:12px; padding:12px 16px;
  background:#16202d; border-bottom:1px solid #1e2f40;
}
.back { color:#67c1f5; cursor:pointer; font-size:18px; }
.title { color:#acb7c3; font-size:15px; font-weight:600; }

.order-list { padding:8px 12px; }
.order-item {
  background:#16202d; border:1px solid #1e2f40; border-radius:4px;
  padding:12px; margin-bottom:6px; cursor:pointer;
}
.order-item:hover { border-color:#2a4a5e; }
.o-head { display:flex; justify-content:space-between; margin-bottom:8px; }
.o-no { font-size:11px; color:#4f6378; }
.o-status { font-size:12px; color:#67c1f5; }
.o-body { display:flex; justify-content:space-between; margin-bottom:4px; }
.o-addr { font-size:12px; color:#7a8a9a; }
.o-price { font-size:16px; color:#a4d007; font-weight:600; }
.o-time { font-size:10px; color:#3d4f5f; }
.empty { text-align:center; padding:60px 0; color:#4f6378; }
</style>
