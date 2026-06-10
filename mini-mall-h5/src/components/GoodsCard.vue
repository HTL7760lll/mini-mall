<template>
  <div class="goods-card" @click="$emit('click')">
    <div class="card-cover">
      <img :src="imgSrc" :alt="goods.name" />
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
  `https://picsum.photos/200/200?random=${props.goods.id}`
)
</script>

<style scoped>
.goods-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  transition: transform 0.2s, box-shadow 0.2s;
}
.goods-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}
.goods-card:active { transform: scale(0.96); }

.card-cover {
  position: relative;
  background: #f5f5f5;
}
.card-cover img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  display: block;
}

.card-tags {
  position: absolute; top: 3px; left: 3px; display: flex; gap: 3px;
}
.tag-hot {
  background: #ee0a24; color: #fff; font-size: 10px; padding: 1px 5px;
  border-radius: 3px; font-weight: 600;
}
.tag-new {
  background: #1989fa; color: #fff; font-size: 10px; padding: 1px 5px;
  border-radius: 3px; font-weight: 600;
}

.card-info { padding: 5px 7px 8px; }

.card-name {
  font-size: 11px;
  color: #222;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-price {
  font-size: 13px;
  color: #ee0a24;
  font-weight: 700;
  margin-top: 3px;
}
</style>
