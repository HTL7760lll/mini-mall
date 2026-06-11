<template>
  <div class="detail-page">
    <header class="topbar">
      <div class="back-btn" @click="$router.back()">
        <span class="back-arrow">&#8592;</span>
        <span class="back-text">返回</span>
      </div>
      <span class="title">订单详情</span>
    </header>

    <div v-if="loading" class="loading"><div class="spin" /></div>

    <template v-else-if="order">
      <!-- 状态卡片 + 进度条 -->
      <div class="status-card" :class="'sc-'+order.order_status">
        <div class="sc-no">订单号: {{ order.order_no }}</div>

        <!-- 进度条 (非取消态) -->
        <div class="stepper" v-if="order.order_status !== 4 && order.order_status !== 5">
          <div class="step" v-for="(s, i) in steps" :key="i" :class="{done: i <= currentStep}">
            <div class="step-dot">{{ i <= currentStep ? '✓' : i + 1 }}</div>
            <div class="step-label">{{ s }}</div>
          </div>
          <div class="stepper-line">
            <div class="line-fill" :style="{width: currentStep / (steps.length-1) * 100 + '%'}" />
          </div>
        </div>

        <!-- 已取消 -->
        <div class="sc-text cancel" v-else>订单已取消</div>
        <div class="sc-text" v-if="order.order_status < 4">{{ steps[currentStep] || order.order_status_desc }}</div>
      </div>

      <!-- 地址 -->
      <div class="section">
        <div class="sec-title">收货信息</div>
        <div class="sec-body">{{ order.receiver_name }} &nbsp; {{ order.receiver_phone }}</div>
        <div class="sec-sub">{{ order.receiver_address }}</div>
      </div>

      <!-- 商品明细 -->
      <div class="section">
        <div class="sec-title">商品明细</div>
        <div class="item" v-for="d in details" :key="d.id">
          <img :src="`https://picsum.photos/80/80?random=${d.goods_id}`" class="item-img" />
          <div class="item-info">
            <div class="item-name">{{ d.goods_name }}</div>
            <div class="item-specs" v-if="d.sku_specs">{{ d.sku_specs }}</div>
            <div class="item-meta">
              <span>¥{{ d.price }} x {{ d.quantity }}</span>
              <span class="item-total">¥{{ d.total_price }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 合计 -->
      <div class="section">
        <div class="sec-title">订单金额</div>
        <div class="amount-row">
          <span>商品合计</span><span>¥{{ order.total_price }}</span>
        </div>
        <div class="amount-row">
          <span>运费</span><span>¥{{ order.freight }}</span>
        </div>
        <div class="amount-row total">
          <span>实付金额</span><span class="big">¥{{ order.pay_amount }}</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="actions" v-if="order.order_status < 3">
        <button v-if="order.order_status === 0" class="btn-pay" @click="handlePay">💳 模拟支付</button>
        <button v-if="order.order_status > 0 && order.order_status < 3" class="btn-confirm" @click="handleConfirm">✅ 确认收货</button>
        <button class="btn-cancel" @click="handleCancel">取消订单</button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import request from '../../api/request'

const route = useRoute()
const router = useRouter()
const order = ref(null)
const details = ref([])
const loading = ref(false)

const steps = ['待付款', '待发货', '待收货', '已完成']
const currentStep = computed(() => {
  if (!order.value) return 0
  const s = order.value.order_status
  if (s === 0) return 0
  if (s === 1) return 1
  if (s === 2) return 2
  if (s === 3) return 3
  return 0
})

const loadDetail = async () => {
  loading.value = true
  try {
    const data = await request.get(`/order/detail/${route.params.id}/`)
    order.value = data
    details.value = data.details || []
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

const handlePay = async () => {
  try {
    await request.post('/order/pay/', { orderId: order.value.id })
    showToast('支付成功')
    loadDetail()
  } catch (e) { console.error(e) }
}

const handleConfirm = async () => {
  try {
    await request.put(`/order/confirm/${order.value.id}/`)
    showToast('已确认收货')
    loadDetail()
  } catch (e) { console.error(e) }
}

const handleCancel = async () => {
  try {
    await request.put(`/order/cancel/${order.value.id}/`)
    showToast('已取消')
    loadDetail()
  } catch (e) { console.error(e) }
}

onMounted(loadDetail)
</script>

<style scoped>
.detail-page { min-height: 100vh; background: #1b2838; padding-bottom: 60px; }

.topbar {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  background: #16202d; border-bottom: 1px solid #1e2f40;
  position: sticky; top: 0; z-index: 10;
}
.back-btn {
  display: flex; align-items: center; gap: 4px; padding: 4px 10px;
  background: rgba(103,193,245,.08); border: 1px solid #1e2f40; border-radius: 4px;
  cursor: pointer;
}
.back-btn:hover { border-color: #67c1f5; }
.back-arrow { font-size: 16px; color: #67c1f5; }
.back-text { font-size: 12px; color: #67c1f5; display: none; }
.title { color: #acb7c3; font-size: 15px; font-weight: 600; }

.loading { display: flex; justify-content: center; padding: 80px 0; }
.spin { width: 28px; height: 28px; border: 2px solid #1e2f40; border-top-color: #ff6b35; border-radius: 50%; animation: s .8s linear infinite; }
@keyframes s { to{transform:rotate(360deg)} }

.status-card {
  margin: 12px; padding: 24px; border-radius: 6px; text-align: center;
  background: #16202d; border: 1px solid #1e2f40;
}
.sc-0 { border-color: #eb6f22; } .sc-1 { border-color: #67c1f5; }
.sc-2 { border-color: #ffd700; } .sc-3 { border-color: #a4d007; } .sc-4,.sc-5 { border-color: #3d4f5f; }
.sc-icon { font-size: 36px; margin-bottom: 6px; }
.sc-text { font-size: 18px; color: #acb7c3; font-weight: 700; }
.sc-text.cancel { color: #eb6f22; }
.sc-no { font-size: 12px; color: #4f6378; margin-bottom: 16px; }

/* 进度条 Stepper */
.stepper { position: relative; display: flex; justify-content: space-between; padding: 0 10px; margin-top: 8px; }
.step { display: flex; flex-direction: column; align-items: center; gap: 6px; z-index: 1; }
.step-dot {
  width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  background: #1a2a3a; border: 2px solid #1e2f40; color: #4f6378; font-size: 12px; font-weight: 700;
  transition: all .3s;
}
.step.done .step-dot { background: #a4d007; border-color: #a4d007; color: #1b2838; }
.step-label { font-size: 10px; color: #4f6378; }
.step.done .step-label { color: #a4d007; }

.stepper-line {
  position: absolute; top: 14px; left: 10px; right: 10px; height: 2px;
  background: #1e2f40; z-index: 0;
}
.line-fill { height: 100%; background: #a4d007; transition: width .5s ease; border-radius: 1px; }

.section {
  margin: 0 12px 12px; background: #16202d; border: 1px solid #1e2f40;
  border-radius: 6px; padding: 14px;
}
.sec-title { font-size: 13px; color: #7a8a9a; margin-bottom: 10px; font-weight: 600; }
.sec-body { font-size: 14px; color: #acb7c3; }
.sec-sub { font-size: 12px; color: #4f6378; margin-top: 4px; }

.item { display: flex; gap: 10px; padding: 8px 0; border-bottom: 1px solid #1e2f40; }
.item:last-child { border-bottom: none; }
.item-img { width: 64px; height: 64px; border-radius: 4px; object-fit: cover; background: #0e1a26; flex-shrink: 0; }
.item-info { flex: 1; min-width: 0; }
.item-name { font-size: 13px; color: #acb7c3; }
.item-specs { font-size: 11px; color: #4f6378; margin-top: 2px; }
.item-meta { display: flex; justify-content: space-between; margin-top: 6px; font-size: 13px; color: #7a8a9a; }
.item-total { color: #a4d007; font-weight: 600; }

.amount-row { display: flex; justify-content: space-between; padding: 4px 0; font-size: 13px; color: #7a8a9a; }
.amount-row.total { border-top: 1px solid #1e2f40; margin-top: 6px; padding-top: 10px; font-size: 15px; color: #acb7c3; font-weight: 600; }
.big { color: #a4d007; font-size: 18px; }

.actions { margin: 12px; display: flex; gap: 8px; }
.btn-pay { flex: 1; padding: 12px 0; background: #a4d007; border: none; border-radius: 6px; color: #1b2838; font-size: 16px; font-weight: 700; cursor: pointer; }
.btn-pay:hover { opacity: .85; }
.btn-confirm { flex: 1; padding: 12px 0; background: #67c1f5; border: none; border-radius: 6px; color: #1b2838; font-size: 16px; font-weight: 700; cursor: pointer; }
.btn-confirm:hover { opacity: .85; }
.btn-cancel { padding: 12px 20px; background: none; border: 1px solid #3d4f5f; border-radius: 6px; color: #4f6378; font-size: 14px; cursor: pointer; }
.btn-cancel:hover { border-color: #eb6f22; color: #eb6f22; }
</style>
