<template>
  <div class="goods-card" @click="$emit('click')">
    <div class="card-cover">
      <img :src="imgSrc" :alt="goods.name" />
      <span v-if="goods.is_hot" class="tag-hot">H</span>
      <span v-if="goods.is_new" class="tag-new">N</span>
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
  `https://picsum.photos/120/120?random=${props.goods.id}`
)
</script>

<style scoped>
.goods-card {
  background: #fff;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.goods-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}
.goods-card:active { transform: scale(0.96); }

.card-cover {
  position: relative; background: #f2f2f2;
}
.card-cover img {
  width: 100%; aspect-ratio: 1; object-fit: cover; display: block;
}

.tag-hot, .tag-new {
  position: absolute; top: 3px; left: 3px;
  color: #fff; font-size: 9px; font-weight: 700;
  padding: 1px 4px; border-radius: 2px; line-height: 1.2;
}
.tag-hot { background: rgba(238,10,36,0.85); }
.tag-new { background: rgba(25,137,250,0.85); left: auto; right: 3px; }

.card-info { padding: 2px 4px 4px; }

.card-name {
  font-size: 9px; color: #333; line-height: 1.2;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.card-price {
  font-size: 11px; color: #ee0a24; font-weight: 700; margin-top: 1px; line-height: 1;
}
</style>
