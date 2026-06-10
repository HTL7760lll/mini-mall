<template>
  <div class="goods-card" @click="$emit('click')">
    <div class="card-cover">
      <img :src="imgSrc" :alt="goods.name" />
      <div class="card-dur" v-if="goods.sales">{{ fmtSales(goods.sales) }}</div>
      <div class="card-tags">
        <span v-if="goods.is_hot" class="tag-hot">Hot</span>
        <span v-if="goods.is_new" class="tag-new">New</span>
      </div>
    </div>
    <div class="card-info">
      <div class="card-name">{{ goods.name }}</div>
      <div class="card-price">¥{{ goods.price }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ goods: { type: Object, required: true } })
defineEmits(['click'])

const imgSrc = computed(() =>
  `https://picsum.photos/358/200?random=${props.goods.id}`
)

const fmtSales = (n) => {
  if (n >= 10000) return (n / 10000).toFixed(1) + 'w'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k'
  return n
}
</script>

<style scoped>
.goods-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.goods-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.goods-card:active { transform: scale(0.97); }

.card-cover {
  position: relative;
  background: #f0f0f0;
}
.card-cover img {
  width: 100%;
  aspect-ratio: 1.75;
  object-fit: cover;
  display: block;
}

.card-dur {
  position: absolute; bottom: 6px; right: 6px;
  background: rgba(0,0,0,0.65); color: #fff;
  font-size: 10px; padding: 2px 6px; border-radius: 4px;
}

.card-tags {
  position: absolute; top: 4px; left: 4px; display: flex; gap: 4px;
}
.tag-hot {
  background: rgba(238,10,36,0.9); color: #fff; font-size: 10px;
  padding: 1px 6px; border-radius: 3px; font-weight: 600;
}
.tag-new {
  background: rgba(25,137,250,0.9); color: #fff; font-size: 10px;
  padding: 1px 6px; border-radius: 3px; font-weight: 600;
}

.card-info {
  padding: 6px 8px 10px;
}

.card-name {
  font-size: 13px;
  color: #18191c;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-price {
  font-size: 15px;
  color: #ee0a24;
  font-weight: 700;
  margin-top: 4px;
}
</style>
