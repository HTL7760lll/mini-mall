from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    goods_image = serializers.CharField(source='goods.main_image', read_only=True)
    sku_specs = serializers.CharField(source='sku.specs', read_only=True)
    price = serializers.DecimalField(source='sku.price', max_digits=10, decimal_places=2, read_only=True)
    stock = serializers.IntegerField(source='sku.stock', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'goods_id', 'sku_id', 'goods_name', 'goods_image',
                  'sku_specs', 'price', 'quantity', 'checked', 'stock', 'created_at']


class CartAddSerializer(serializers.Serializer):
    goods_id = serializers.IntegerField()
    sku_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)


class CartUpdateSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
