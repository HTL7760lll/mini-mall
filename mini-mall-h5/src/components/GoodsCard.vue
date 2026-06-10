<template>
  <div class="goods-card" @click="$emit('click')">
    <div class="card-image">
      <img :src="imgSrc" class="goods-img" :alt="goods.name" />
      <div class="card-tags">
        <van-tag v-if="goods.is_hot" type="danger" size="mini" round>Hot</van-tag>
        <van-tag v-if="goods.is_new" type="primary" size="mini" round style="margin-left:3px">New</van-tag>
      </div>
    </div>
    <div class="card-body">
      <div class="card-name">{{ goods.name }}</div>
      <div class="card-price">
        <span class="price-symbol">¥</span>
        <span class="price-value">{{ goods.price }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ goods: { type: Object, required: true } })
defineEmits(['click'])

const imgSrc = computed(() =>
  `https://picsum.photos/200/200?random=${props.goods.id}`
)
</script>

<style scoped>
.goods-card {
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: all 0.25s ease;
}
.goods-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.goods-card:active { transform: scale(0.96); }

.card-image {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  overflow: hidden;
  background: #f0f0f0;
}
.goods-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.card-tags {
  position: absolute; top: 4px; left: 4px; display: flex;
}

.card-body { padding: 6px 8px 10px; }

.card-name {
  font-size: 12px;
  font-weight: 600;
  color: #222;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-align: left;
}

.card-price {
  display: flex; align-items: baseline; margin-top: 4px;
}
.price-symbol { font-size: 11px; color: #ee0a24; font-weight: 700; }
.price-value { font-size: 15px; color: #ee0a24; font-weight: 700; line-height: 1; }
</style>
