<template>
  <div class="order-page">
    <header class="topbar">
      <div class="back-btn" @click="$router.push('/')">
        <span class="back-arrow">&#8592;</span>
        <span class="back-text">返回</span>
      </div>
      <span class="title">我的订单</span>
    </header>

    <div v-if="loading" class="loading"><div class="spin" /></div>

    <!-- 状态Tab -->
    <div class="tabs" v-if="!loading">
      <div class="tab" :class="{sel: statusFilter===null}" @click="statusFilter=null; loadOrders()">全部</div>
      <div class="tab" :class="{sel: statusFilter===v}" v-for="(label, v) in STATUS_MAP" :key="v" @click="statusFilter=v; loadOrders()">{{ label }}</div>
    </div>

    <!-- 列表 -->
    <div v-if="orders.length" class="order-list">
      <div class="order-card" v-for="o in orders" :key="o.id" @click="goDetail(o.id)">
        <div class="oc-head">
          <span class="oc-no">#{{ o.order_no?.slice(-12) }}</span>
          <span class="oc-status" :class="'s-'+o.order_status">{{ o.order_status_desc }}</span>
        </div>
        <div class="oc-body">
          <div class="oc-info">
            <span>{{ o.receiver_name }}</span>
            <span class="oc-time">{{ fmtTime(o.created_at) }}</span>
          </div>
          <div class="oc-price">¥{{ o.pay_amount }}</div>
        </div>
        <div class="oc-actions" v-if="o.order_status === 0">
          <button class="btn-pay" @click.stop="handlePay(o.id)">立即付款</button>
          <button class="btn-cancel" @click.stop="handleCancel(o.id)">取消</button>
        </div>
      </div>
    </div>

    <div v-else-if="!loading" class="empty">暂无订单</div>

    <!-- 分页 -->
    <div class="pagination-wrap" v-if="total > pageSize">
      <van-pagination v-model="currentPage" :total-items="total" :items-per-page="pageSize" mode="simple" @change="onPageChange" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import request from '../../api/request'

const router = useRouter()
const orders = ref([])
const loading = ref(false)
const statusFilter = ref(null)
const currentPage = ref(1)
const pageSize = 10
const total = ref(0)

const STATUS_MAP = { 0: '待付款', 1: '待发货', 2: '待收货', 3: '已完成', 4: '已取消' }

const loadOrders = async () => {
  loading.value = true
  try {
    const params = { page: currentPage.value, pageSize }
    if (statusFilter.value !== null) params.orderStatus = statusFilter.value
    const data = await request.get('/order/page/', { params })
    orders.value = data.records || []
    total.value = data.total || 0
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

const handlePay = async (id) => {
  try {
    await request.post('/order/pay/', { orderId: id })
    showToast('支付成功')
    loadOrders()
  } catch (e) { console.error(e) }
}

const handleCancel = async (id) => {
  try {
    await request.put(`/order/cancel/${id}/`)
    showToast('已取消')
    loadOrders()
  } catch (e) { console.error(e) }
}

const goDetail = (id) => router.push(`/order/${id}`)
const onPageChange = (p) => { currentPage.value = p; loadOrders() }
const fmtTime = (t) => t ? t.split('T')[0] + ' ' + (t.split('T')[1]||'').slice(0,5) : ''

onMounted(loadOrders)
</script>

<style scoped>
.order-page { min-height: 100vh; background: #1b2838; padding-bottom: 40px; }

.topbar {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  background: #16202d; border-bottom: 1px solid #1e2f40; position: sticky; top: 0; z-index: 10;
}
.back-btn {
  display: flex; align-items: center; gap: 4px; padding: 4px 10px;
  background: rgba(103,193,245,.08); border: 1px solid #1e2f40; border-radius: 4px;
  cursor: pointer; transition: all .15s;
}
.back-btn:hover { border-color: #67c1f5; }
.back-arrow { font-size: 16px; color: #67c1f5; }
.back-text { font-size: 12px; color: #67c1f5; display: none; }
.title { color: #acb7c3; font-size: 15px; font-weight: 600; }

.loading { display: flex; justify-content: center; padding: 80px 0; }
.spin { width: 28px; height: 28px; border: 2px solid #1e2f40; border-top-color: #ff6b35; border-radius: 50%; animation: s .8s linear infinite; }
@keyframes s { to{transform:rotate(360deg)} }

.tabs { display: flex; gap: 2px; padding: 8px 12px; background: #16202d; border-bottom: 1px solid #1e2f40; }
.tab { padding: 5px 12px; border-radius: 3px; font-size: 12px; color: #7a8a9a; cursor: pointer; transition: all .12s; }
.tab:hover { color: #acb7c3; }
.tab.sel { background: #1a2a3a; color: #67c1f5; border: 1px solid #1e2f40; }

.order-list { padding: 8px 12px; }
.order-card {
  background: #16202d; border: 1px solid #1e2f40; border-radius: 4px;
  padding: 12px; margin-bottom: 8px; cursor: pointer; transition: border-color .15s;
}
.order-card:hover { border-color: #2a4a5e; }

.oc-head { display: flex; justify-content: space-between; margin-bottom: 8px; }
.oc-no { font-size: 12px; color: #4f6378; }
.oc-status { font-size: 12px; font-weight: 600; }
.s-0 { color: #eb6f22; } .s-1 { color: #67c1f5; } .s-2 { color: #ffd700; }
.s-3 { color: #a4d007; } .s-4 { color: #4f6378; } .s-5 { color: #ff4444; }

.oc-body { display: flex; justify-content: space-between; align-items: flex-end; }
.oc-info { font-size: 12px; color: #7a8a9a; }
.oc-time { margin-left: 8px; color: #4f6378; }
.oc-price { font-size: 18px; color: #a4d007; font-weight: 700; }

.oc-actions { display: flex; gap: 8px; margin-top: 10px; justify-content: flex-end; }
.btn-pay { padding: 5px 20px; background: #a4d007; border: none; border-radius: 3px; color: #1b2838; font-size: 13px; font-weight: 700; cursor: pointer; }
.btn-pay:hover { opacity: .85; }
.btn-cancel { padding: 5px 14px; background: none; border: 1px solid #3d4f5f; border-radius: 3px; color: #4f6378; font-size: 12px; cursor: pointer; }
.btn-cancel:hover { border-color: #eb6f22; color: #eb6f22; }

.empty { text-align: center; padding: 80px 0; color: #4f6378; font-size: 14px; }
.pagination-wrap { padding: 16px 0; }
</style>
