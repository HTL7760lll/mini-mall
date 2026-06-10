from django.contrib import admin
from .models import GoodsCategory, Goods, GoodsSku


class GoodsSkuInline(admin.TabularInline):
    model = GoodsSku
    extra = 1


@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'sort', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name']
    ordering = ['sort']


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'stock', 'sales', 'status', 'is_hot', 'is_new', 'sort']
    list_filter = ['status', 'is_hot', 'is_new', 'category']
    search_fields = ['name', 'subtitle']
    list_editable = ['status', 'is_hot', 'is_new', 'sort']
    inlines = [GoodsSkuInline]


@admin.register(GoodsSku)
class GoodsSkuAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods', 'specs', 'price', 'stock', 'status']
    list_filter = ['status']
    search_fields = ['specs', 'goods__name']
