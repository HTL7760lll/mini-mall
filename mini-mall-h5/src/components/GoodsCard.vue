<template>
  <div class="goods-card" @click="$emit('click')">
    <div class="card-cover">
      <img :src="imgSrc" :alt="goods.name" />
      <div class="card-tags">
        <van-tag v-if="goods.is_hot" type="danger" size="mini" round>Hot</van-tag>
        <van-tag v-if="goods.is_new" type="primary" size="mini" round style="margin-left:3px">New</van-tag>
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
</script>

<style scoped>
.goods-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.goods-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.goods-card:active { transform: scale(0.97); }

.card-cover {
  position: relative;
  width: 100%;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
  background: #f4f4f4;
}
.card-cover img {
  width: 100%;
  display: block;
  aspect-ratio: 1.8;
  object-fit: cover;
}
.card-tags {
  position: absolute; top: 6px; left: 6px; display: flex;
}

.card-info {
  padding: 8px 10px 12px;
}

.card-name {
  font-size: 13px;
  font-weight: 500;
  color: #18191c;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-price {
  font-size: 15px;
  font-weight: 600;
  color: #ee0a24;
  margin-top: 6px;
}
</style>
