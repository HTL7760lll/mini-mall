import uuid
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.member.models import Address
from apps.cart.models import Cart
from .models import Order, OrderDetail
from .serializers import OrderSerializer, OrderDetailSerializer, OrderSubmitSerializer


class OrderPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'pageSize'
    page_query_param = 'page'


@api_view(['POST'])
def order_submit(request):
    """提交订单"""
    serializer = OrderSubmitSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'code': 400, 'msg': str(serializer.errors)}, status=400)

    data = serializer.validated_data

    # 校验收货地址
    try:
        address = Address.objects.get(id=data['address_id'], member=request.user, deleted=False)
    except Address.DoesNotExist:
        return Response({'code': 4001, 'msg': '收货地址不存在'}, status=400)

    # 查询购物车选中项
    cart_items = Cart.objects.filter(member=request.user, checked=True).select_related('goods', 'sku')
    if not cart_items.exists():
        return Response({'code': 3004, 'msg': '请先选择商品'}, status=400)

    with transaction.atomic():
        total_price = Decimal('0')
        details = []

        for cart in cart_items:
            sku = cart.sku
            goods = cart.goods

            if goods.status == 0:
                return Response({'code': 400, 'msg': f'商品【{goods.name}】已下架'}, status=400)
            if sku.stock < cart.quantity:
                return Response({'code': 3003, 'msg': f'商品【{goods.name}】{sku.specs} 库存不足'}, status=400)

            item_total = sku.price * cart.quantity
            total_price += item_total

            detail = OrderDetail(
                goods=goods, sku=sku,
                goods_name=goods.name,
                goods_image=goods.main_image or '',
                sku_specs=sku.specs,
                price=sku.price,
                quantity=cart.quantity,
                total_price=item_total,
            )
            details.append(detail)

            # 扣库存
            sku.stock -= cart.quantity
            sku.save()
            goods.stock -= cart.quantity
            goods.sales = (goods.sales or 0) + cart.quantity
            goods.save()

        # 生成订单号
        order_no = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().int)[:6]

        # 创建订单
        order = Order.objects.create(
            order_no=order_no,
            member=request.user,
            total_price=total_price,
            freight=Decimal('0'),
            pay_amount=total_price,
            pay_type=1,
            pay_status=0,
            order_status=0,
            receiver_name=address.receiver_name,
            receiver_phone=address.receiver_phone,
            receiver_address=f'{address.province}{address.city}{address.district} {address.detail}',
            remark=data.get('remark', ''),
        )

        # 保存订单详情
        for detail in details:
            detail.order = order
            detail.order_no = order_no
        OrderDetail.objects.bulk_create(details)

        # 清空购物车选中项
        cart_items.delete()

    return Response({
        'code': 200, 'msg': '下单成功',
        'data': {'order_id': order.id, 'order_no': order_no, 'pay_amount': str(total_price)}
    })


@api_view(['POST'])
def order_pay(request):
    """模拟支付"""
    order_id = request.data.get('orderId')
    try:
        order = Order.objects.get(id=order_id, member=request.user)
    except Order.DoesNotExist:
        return Response({'code': 3001, 'msg': '订单不存在'}, status=404)

    if order.order_status != 0:
        return Response({'code': 3002, 'msg': '订单状态不正确'}, status=400)

    order.pay_status = 1
    order.pay_time = datetime.now()
    order.order_status = 1  # 待发货
    order.save()
    return Response({'code': 200, 'msg': '支付成功'})


@api_view(['PUT'])
def order_cancel(request, pk):
    """取消订单"""
    try:
        order = Order.objects.get(id=pk, member=request.user)
    except Order.DoesNotExist:
        return Response({'code': 3001, 'msg': '订单不存在'}, status=404)

    if order.order_status != 0:
        return Response({'code': 3002, 'msg': '订单状态不正确'}, status=400)

    order.order_status = 4
    order.save()
    # 恢复库存
    for detail in order.details.all():
        detail.sku.stock += detail.quantity
        detail.sku.save()
        detail.goods.stock += detail.quantity
        detail.goods.save()

    return Response({'code': 200, 'msg': '已取消'})


@api_view(['PUT'])
def order_confirm(request, pk):
    """确认收货"""
    try:
        order = Order.objects.get(id=pk, member=request.user)
    except Order.DoesNotExist:
        return Response({'code': 3001, 'msg': '订单不存在'}, status=404)

    if order.order_status != 2:
        return Response({'code': 3002, 'msg': '订单状态不正确'}, status=400)

    order.order_status = 3
    order.save()
    return Response({'code': 200, 'msg': '已确认收货'})


@api_view(['GET'])
def order_list(request):
    """订单列表"""
    queryset = Order.objects.filter(member=request.user, deleted=False)

    order_status = request.query_params.get('orderStatus')
    if order_status is not None:
        queryset = queryset.filter(order_status=order_status)

    paginator = OrderPagination()
    page = paginator.paginate_queryset(queryset.order_by('-created_at'), request)
    serializer = OrderSerializer(page, many=True)

    return Response({
        'code': 200, 'msg': 'success',
        'data': {
            'total': paginator.page.paginator.count,
            'pages': paginator.page.paginator.num_pages,
            'current': paginator.page.number,
            'size': paginator.page_size,
            'records': serializer.data,
        }
    })


@api_view(['GET'])
def order_detail(request, pk):
    """订单详情"""
    try:
        order = Order.objects.get(id=pk, member=request.user)
    except Order.DoesNotExist:
        return Response({'code': 3001, 'msg': '订单不存在'}, status=404)

    data = OrderSerializer(order).data
    data['details'] = OrderDetailSerializer(order.details.all(), many=True).data
    return Response({'code': 200, 'msg': 'success', 'data': data})
