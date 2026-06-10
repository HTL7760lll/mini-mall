<template>
  <div class="goods-card" @click="$emit('click')">
    <div class="card-image">
      <van-image
        :src="goods.main_image || 'https://picsum.photos/seed/default/400/400'"
        fit="cover"
        width="100%"
        height="180"
        lazy-load
      />
      <!-- 热卖/新品标签 -->
      <div class="card-tags">
        <van-tag v-if="goods.is_hot" type="danger" size="small" round>Hot</van-tag>
        <van-tag v-if="goods.is_new" type="primary" size="small" round style="margin-left:4px">New</van-tag>
      </div>
    </div>
    <div class="card-body">
      <div class="card-name">{{ goods.name }}</div>
      <div class="card-subtitle" v-if="goods.subtitle">{{ goods.subtitle }}</div>
      <div class="card-bottom">
        <div class="card-price">
          <span class="price-symbol">¥</span>
          <span class="price-value">{{ goods.price }}</span>
          <span class="price-original" v-if="goods.original_price">¥{{ goods.original_price }}</span>
        </div>
        <div class="card-sales" v-if="goods.sales">
          已售 {{ goods.sales > 999 ? (goods.sales / 1000).toFixed(1) + 'k' : goods.sales }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  goods: { type: Object, required: true },
})
defineEmits(['click'])
</script>

<style scoped>
.goods-card {
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: transform 0.15s;
}
.goods-card:active {
  transform: scale(0.97);
}

.card-image {
  position: relative;
}
.card-tags {
  position: absolute;
  top: 6px;
  left: 6px;
  display: flex;
}

.card-body {
  padding: 10px;
}

.card-name {
  font-size: 14px;
  font-weight: 600;
  color: #222;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 38px;
}

.card-subtitle {
  font-size: 11px;
  color: #999;
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-top: 8px;
}

.card-price {
  display: flex;
  align-items: baseline;
}
.price-symbol {
  font-size: 12px;
  color: #ee0a24;
  font-weight: 700;
}
.price-value {
  font-size: 18px;
  color: #ee0a24;
  font-weight: 700;
  line-height: 1;
}
.price-original {
  font-size: 11px;
  color: #ccc;
  text-decoration: line-through;
  margin-left: 4px;
}

.card-sales {
  font-size: 10px;
  color: #bbb;
}
</style>
