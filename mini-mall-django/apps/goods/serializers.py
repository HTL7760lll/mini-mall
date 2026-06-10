from rest_framework import serializers
from .models import GoodsCategory, Goods, GoodsSku


class GoodsSkuSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsSku
        fields = ['id', 'goods_id', 'specs', 'price', 'stock', 'image', 'status']


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    goods_count = serializers.SerializerMethodField()

    class Meta:
        model = GoodsCategory
        fields = ['id', 'parent_id', 'name', 'icon', 'sort', 'children', 'goods_count']

    def get_children(self, obj):
        children = obj.children.filter(status=1, deleted=False).order_by('sort')
        return CategorySerializer(children, many=True).data if children.exists() else []

    def get_goods_count(self, obj):
        return Goods.objects.filter(category=obj, status=1, deleted=False).count()


class GoodsListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Goods
        fields = ['id', 'category_id', 'category_name', 'name', 'subtitle',
                  'main_image', 'price', 'original_price', 'stock', 'sales',
                  'status', 'is_hot', 'is_new', 'sort', 'created_at']


class GoodsDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    skus = GoodsSkuSerializer(many=True, read_only=True)

    class Meta:
        model = Goods
        fields = ['id', 'category_id', 'category_name', 'name', 'subtitle',
                  'main_image', 'images', 'detail', 'price', 'original_price',
                  'stock', 'sales', 'is_hot', 'is_new', 'skus']
