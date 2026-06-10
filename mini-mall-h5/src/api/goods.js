import request from './request'

/** 商品分页列表 */
export function getGoodsPage(params) {
  return request.get('/goods/page/', { params })
}

/** 商品详情 */
export function getGoodsDetail(id) {
  return request.get(`/goods/detail/${id}/`)
}

/** 分类树 */
export function getCategoryTree() {
  return request.get('/goods/category/tree/')
}

/** 热卖推荐 */
export function getHotGoods() {
  return request.get('/goods/hot/')
}

/** 新品推荐 */
export function getNewGoods() {
  return request.get('/goods/new/')
}

/** 加入购物车 */
export function addToCart(data) {
  return request.post('/cart/add/', data)
}
