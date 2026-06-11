<template>
  <div class="goods-card" @click="$emit('click')">
    <div class="card-img">
      <img :src="imgSrc" :alt="goods.name" />
      <span v-if="goods.is_hot" class="badge badge-hot">H</span>
      <span v-if="goods.is_new" class="badge badge-new">N</span>
    </div>
    <div class="card-meta">
      <div class="card-name">{{ goods.name }}</div>
      <div class="card-row">
        <span class="card-price">¥{{ goods.price }}</span>
        <span class="card-sales" v-if="goods.sales">{{ fmtSales(goods.sales) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ goods: { type: Object, required: true } })
defineEmits(['click'])

const imgSrc = computed(() => `https://picsum.photos/200/200?random=${props.goods.id}`)
const fmtSales = (n) => {
  if (n >= 10000) return (n/10000).toFixed(1)+'w'
  if (n >= 1000) return (n/1000).toFixed(1)+'k'
  return n
}
</script>

<style scoped>
.goods-card {
  background: #0d1117;
  cursor: pointer;
  transition: background .15s;
  overflow: hidden;
}
.goods-card:hover { background: #161b22; }

.card-img {
  position: relative;
  background: #161b22;
}
.card-img img {
  width: 100%; aspect-ratio: 1; object-fit: cover; display: block;
}

.badge {
  position: absolute; top: 4px; left: 4px;
  font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 2px;
}
.badge-hot { background: #ff6b35; color: #0d1117; }
.badge-new { background: #00d4ff; color: #0d1117; left: auto; right: 4px; }

.card-meta { padding: 6px 8px 8px; }

.card-name {
  font-size: 12px; color: #c9d1d9; line-height: 1.3;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.card-row { display: flex; justify-content: space-between; align-items: baseline; margin-top: 4px; }
.card-price { font-size: 14px; color: #ff6b35; font-weight: 700; }
.card-sales { font-size: 10px; color: #484f58; }
</style>
