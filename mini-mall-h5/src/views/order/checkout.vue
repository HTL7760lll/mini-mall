<template>
  <div class="checkout-page">
    <header class="topbar">
      <div class="back-btn" @click="$router.back()">
        <span class="back-arrow">&#8592;</span>
        <span class="back-text">返回</span>
      </div>
      <span class="title">确认订单</span>
    </header>

    <!-- 收货地址 -->
    <div class="section">
      <div class="sec-title">📍 收货地址</div>
      <div v-if="addresses.length" class="addr-list">
        <div class="addr-card" v-for="a in addresses" :key="a.id"
          :class="{sel: selectedAddr?.id === a.id}" @click="selectedAddr = a">
          <div class="addr-top">
            <span class="addr-name">{{ a.receiver_name }}</span>
            <span class="addr-phone">{{ a.receiver_phone }}</span>
            <span class="addr-tag" v-if="a.is_default">默认</span>
          </div>
          <div class="addr-detail">{{ a.province }}{{ a.city }}{{ a.district }} {{ a.detail }}</div>
          <div class="addr-check" v-if="selectedAddr?.id === a.id">✓</div>
        </div>
      </div>
      <div v-else class="no-addr">
        <p>暂无收货地址</p>
      </div>
      <button class="add-addr-btn" @click="showAddrForm = true">+ 新增地址</button>
    </div>

    <!-- 新增地址表单 -->
    <div class="modal-overlay" v-if="showAddrForm" @click.self="showAddrForm = false">
      <div class="modal-card">
        <div class="modal-title">新增收货地址</div>
        <input class="afield" v-model="newAddr.receiver_name" placeholder="收货人姓名" />
        <input class="afield" v-model="newAddr.receiver_phone" placeholder="联系电话" />
        <div class="afield-row">
          <input class="afield" v-model="newAddr.province" placeholder="省" />
          <input class="afield" v-model="newAddr.city" placeholder="市" />
          <input class="afield" v-model="newAddr.district" placeholder="区" />
        </div>
        <input class="afield" v-model="newAddr.detail" placeholder="详细地址" />
        <div class="modal-btns">
          <button class="btn-cancel" @click="showAddrForm = false">取消</button>
          <button class="btn-save" @click="saveAddress">保存</button>
        </div>
      </div>
    </div>

    <!-- 商品清单 -->
    <div class="section">
      <div class="sec-title">📦 商品信息</div>
      <div class="item" v-for="item in cartItems" :key="item.id">
        <img :src="`https://picsum.photos/60/60?random=${item.goods_id}`" class="item-img" />
        <div class="item-info">
          <div class="item-name">{{ item.goods_name }}</div>
          <div class="item-specs" v-if="item.sku_specs">{{ item.sku_specs }}</div>
        </div>
        <div class="item-right">
          <span class="item-price">¥{{ item.price }}</span>
          <span class="item-qty">x{{ item.quantity }}</span>
        </div>
      </div>
    </div>

    <!-- 备注 -->
    <div class="section">
      <div class="sec-title">📝 订单备注</div>
      <input class="remark-inp" v-model="remark" placeholder="选填" />
    </div>

    <!-- 合计 -->
    <div class="section">
      <div class="amount-row">
        <span>商品合计</span><span>¥{{ totalPrice.toFixed(2) }}</span>
      </div>
      <div class="amount-row total">
        <span>实付金额</span><span class="big">¥{{ totalPrice.toFixed(2) }}</span>
      </div>
    </div>

    <!-- 提交 -->
    <div class="submit-wrap">
      <button class="submit-btn" :disabled="!selectedAddr || submitting" @click="handleSubmit">
        {{ submitting ? '提交中...' : '提交订单' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import request from '../../api/request'

const router = useRouter()

const addresses = ref([])
const selectedAddr = ref(null)
const cartItems = ref([])
const remark = ref('')
const submitting = ref(false)
const showAddrForm = ref(false)
const newAddr = ref({ receiver_name: '', receiver_phone: '', province: '', city: '', district: '', detail: '' })

const totalPrice = computed(() =>
  cartItems.value.reduce((s, i) => s + i.price * i.quantity, 0)
)

const loadData = async () => {
  try {
    const [addrData, cartData] = await Promise.all([
      request.get('/member/address/'),
      request.get('/cart/list/'),
    ])
    addresses.value = addrData?.records || []
    cartItems.value = cartData?.records || []
    if (addresses.value.length) {
      selectedAddr.value = addresses.value.find(a => a.is_default) || addresses.value[0]
    }
  } catch (e) { console.error(e) }
}

const saveAddress = async () => {
  const a = newAddr.value
  if (!a.receiver_name || !a.receiver_phone || !a.province || !a.city || !a.detail) {
    return showToast('请填写完整地址信息')
  }
  try {
    await request.post('/member/address/', a)
    showAddrForm.value = false
    newAddr.value = { receiver_name: '', receiver_phone: '', province: '', city: '', district: '', detail: '' }
    const d = await request.get('/member/address/')
    addresses.value = d?.records || []
    if (addresses.value.length) selectedAddr.value = addresses.value[addresses.value.length - 1]
  } catch (e) { console.error(e) }
}

const handleSubmit = async () => {
  if (!selectedAddr.value) return showToast('请选择收货地址')
  submitting.value = true
  try {
    const data = await request.post('/order/submit/', {
      address_id: selectedAddr.value.id,
      remark: remark.value,
    })
    showToast('下单成功')
    router.replace(`/order/${data.order_id}`)
  } catch (e) {
    console.error(e)
  } finally {
    submitting.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.checkout-page { min-height: 100vh; background: #1b2838; padding-bottom: 80px; }

.topbar {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  background: #16202d; border-bottom: 1px solid #1e2f40; position: sticky; top: 0; z-index: 10;
}
.back-btn {
  display: flex; align-items: center; gap: 4px; padding: 4px 10px;
  background: rgba(103,193,245,.08); border: 1px solid #1e2f40; border-radius: 4px; cursor: pointer;
}
.back-btn:hover { border-color: #67c1f5; }
.back-arrow { font-size: 16px; color: #67c1f5; }
.back-text { font-size: 12px; color: #67c1f5; display: none; }
.title { color: #acb7c3; font-size: 15px; font-weight: 600; }

.section { margin: 12px; background: #16202d; border: 1px solid #1e2f40; border-radius: 6px; padding: 14px; }
.sec-title { font-size: 13px; color: #7a8a9a; margin-bottom: 10px; font-weight: 600; }

/* Address */
.addr-list { display: flex; flex-direction: column; gap: 8px; }
.addr-card {
  padding: 12px; border: 1px solid #1e2f40; border-radius: 4px;
  cursor: pointer; transition: border-color .15s; position: relative;
}
.addr-card:hover { border-color: #2a4a5e; }
.addr-card.sel { border-color: #67c1f5; background: rgba(103,193,245,.04); }
.addr-top { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.addr-name { font-size: 14px; color: #acb7c3; font-weight: 600; }
.addr-phone { font-size: 13px; color: #7a8a9a; }
.addr-tag { font-size: 10px; background: #eb6f22; color: #fff; padding: 1px 6px; border-radius: 2px; }
.addr-detail { font-size: 12px; color: #4f6378; }
.addr-check {
  position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
  color: #67c1f5; font-size: 20px; font-weight: 700;
}
.no-addr { text-align: center; padding: 16px 0; color: #4f6378; font-size: 13px; }
.add-addr-btn {
  margin-top: 10px; width: 100%; padding: 8px 0; background: none; border: 1px dashed #1e2f40;
  border-radius: 4px; color: #4f6378; font-size: 13px; cursor: pointer;
}
.add-addr-btn:hover { border-color: #67c1f5; color: #67c1f5; }

/* Address Form Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.6); z-index: 50; display: flex; align-items: center; justify-content: center; padding: 20px; }
.modal-card { background: #16202d; border: 1px solid #1e2f40; border-radius: 8px; padding: 20px; width: 100%; max-width: 400px; }
.modal-title { font-size: 16px; color: #acb7c3; font-weight: 700; margin-bottom: 16px; text-align: center; }
.afield {
  width: 100%; padding: 10px 12px; margin-bottom: 10px;
  background: #1a2a3a; border: 1px solid #1e2f40; border-radius: 4px;
  outline: none; color: #acb7c3; font-size: 13px;
}
.afield:focus { border-color: #67c1f5; }
.afield::placeholder { color: #3d4f5f; }
.afield-row { display: flex; gap: 6px; }
.afield-row .afield { flex: 1; }
.modal-btns { display: flex; gap: 8px; margin-top: 8px; }
.btn-cancel { flex: 1; padding: 10px 0; background: none; border: 1px solid #1e2f40; border-radius: 4px; color: #4f6378; font-size: 14px; cursor: pointer; }
.btn-save { flex: 1; padding: 10px 0; background: #67c1f5; border: none; border-radius: 4px; color: #1b2838; font-size: 14px; font-weight: 700; cursor: pointer; }
.btn-save:hover { opacity: .85; }

/* Items */
.item { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid #1e2f40; }
.item:last-child { border-bottom: none; }
.item-img { width: 56px; height: 56px; border-radius: 4px; object-fit: cover; background: #0e1a26; flex-shrink: 0; }
.item-info { flex: 1; min-width: 0; }
.item-name { font-size: 13px; color: #acb7c3; }
.item-specs { font-size: 11px; color: #4f6378; margin-top: 2px; }
.item-right { text-align: right; flex-shrink: 0; }
.item-price { font-size: 14px; color: #a4d007; font-weight: 600; }
.item-qty { font-size: 11px; color: #4f6378; margin-left: 8px; }

/* Remark */
.remark-inp {
  width: 100%; padding: 10px 12px; background: #1a2a3a; border: 1px solid #1e2f40;
  border-radius: 4px; outline: none; color: #acb7c3; font-size: 13px;
}
.remark-inp::placeholder { color: #3d4f5f; }
.remark-inp:focus { border-color: #67c1f5; }

/* Amount */
.amount-row { display: flex; justify-content: space-between; padding: 4px 0; font-size: 13px; color: #7a8a9a; }
.amount-row.total { border-top: 1px solid #1e2f40; margin-top: 6px; padding-top: 10px; font-size: 16px; color: #acb7c3; font-weight: 600; }
.big { color: #a4d007; font-size: 20px; }

/* Submit */
.submit-wrap { position: fixed; bottom: 0; left: 190px; right: 0; padding: 12px 16px; background: #16202d; border-top: 1px solid #1e2f40; z-index: 10; }
.submit-btn {
  width: 100%; padding: 14px 0; background: linear-gradient(135deg, #a4d007, #5c7e10);
  border: none; border-radius: 6px; color: #1b2838; font-size: 16px; font-weight: 700; cursor: pointer;
}
.submit-btn:hover { opacity: .9; }
.submit-btn:disabled { opacity: .3; cursor: not-allowed; }
</style>
