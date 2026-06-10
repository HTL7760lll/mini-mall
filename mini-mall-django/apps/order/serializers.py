from rest_framework import serializers
from .models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['id', 'goods_id', 'sku_id', 'goods_name', 'goods_image',
                  'sku_specs', 'price', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    pay_status_desc = serializers.SerializerMethodField()
    order_status_desc = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_no', 'member_id', 'total_price', 'freight',
                  'pay_amount', 'pay_type', 'pay_status', 'pay_status_desc',
                  'pay_time', 'order_status', 'order_status_desc',
                  'receiver_name', 'receiver_phone', 'receiver_address',
                  'remark', 'created_at']

    def get_pay_status_desc(self, obj):
        return '已支付' if obj.pay_status == 1 else '未支付'

    def get_order_status_desc(self, obj):
        return dict(Order.ORDER_STATUS).get(obj.order_status, '未知')


class OrderSubmitSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    remark = serializers.CharField(required=False, allow_blank=True)
