from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.goods.models import Goods, GoodsSku
from .models import Cart
from .serializers import CartSerializer, CartAddSerializer, CartUpdateSerializer


@api_view(['GET'])
def cart_list(request):
    """购物车列表"""
    carts = Cart.objects.filter(member=request.user).select_related('goods', 'sku')
    serializer = CartSerializer(carts, many=True)
    return Response({'code': 200, 'msg': 'success',
        'data': {'records': serializer.data}})


@api_view(['POST'])
def cart_add(request):
    """加入购物车"""
    serializer = CartAddSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'code': 400, 'msg': str(serializer.errors)}, status=400)

    data = serializer.validated_data
    sku = GoodsSku.objects.get(id=data['sku_id'], goods_id=data['goods_id'])
    if sku.status == 0:
        return Response({'code': 400, 'msg': '该规格已下架'}, status=400)

    # 检查总数量是否超过库存
    existing = Cart.objects.filter(member=request.user, sku_id=data['sku_id']).first()
    total_qty = (existing.quantity if existing else 0) + data['quantity']
    if total_qty > sku.stock:
        return Response({'code': 3003, 'msg': '库存不足，请等待补货'}, status=400)

    cart, created = Cart.objects.get_or_create(
        member=request.user,
        sku_id=data['sku_id'],
        defaults={
            'goods_id': data['goods_id'],
            'quantity': data['quantity'],
            'checked': True,
        }
    )
    if not created:
        cart.quantity += data['quantity']
        cart.save()

    return Response({'code': 200, 'msg': '已加入购物车'})


@api_view(['PUT'])
def cart_update(request):
    """修改数量"""
    serializer = CartUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'code': 400, 'msg': str(serializer.errors)}, status=400)

    data = serializer.validated_data
    try:
        cart = Cart.objects.select_related('sku').get(id=data['cart_id'], member=request.user)
    except Cart.DoesNotExist:
        return Response({'code': 400, 'msg': '购物车项不存在'}, status=404)

    if data['quantity'] <= 0:
        cart.delete()
    else:
        if data['quantity'] > cart.sku.stock:
            return Response({'code': 3003, 'msg': '库存不足，请等待补货'}, status=400)
        cart.quantity = data['quantity']
        cart.save()

    return Response({'code': 200, 'msg': 'success'})


@api_view(['PUT'])
def cart_check(request, pk):
    """选中/取消选中"""
    try:
        cart = Cart.objects.get(id=pk, member=request.user)
    except Cart.DoesNotExist:
        return Response({'code': 400, 'msg': '购物车项不存在'}, status=404)

    checked = request.data.get('checked', True)
    cart.checked = checked
    cart.save()
    return Response({'code': 200, 'msg': 'success'})


@api_view(['DELETE'])
def cart_remove(request, pk):
    """删除购物车项"""
    try:
        cart = Cart.objects.get(id=pk, member=request.user)
    except Cart.DoesNotExist:
        return Response({'code': 400, 'msg': '购物车项不存在'}, status=404)
    cart.delete()
    return Response({'code': 200, 'msg': '删除成功'})


@api_view(['DELETE'])
def cart_clear(request):
    """清空已选中"""
    Cart.objects.filter(member=request.user, checked=True).delete()
    return Response({'code': 200, 'msg': '已清空'})


@api_view(['GET'])
def cart_count(request):
    """购物车数量"""
    count = Cart.objects.filter(member=request.user).count()
    return Response({'code': 200, 'msg': 'success', 'data': {'count': count}})
