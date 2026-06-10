from django.db import models


class GoodsCategory(models.Model):
    """商品分类"""
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name='父级分类')
    name = models.CharField(max_length=50, verbose_name='分类名称')
    icon = models.URLField(max_length=255, blank=True, null=True, verbose_name='图标')
    sort = models.IntegerField(default=0, verbose_name='排序')
    status = models.IntegerField(default=1, verbose_name='状态 1启用 0禁用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'goods_category'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.name


class Goods(models.Model):
    """商品 SPU"""
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='goods', verbose_name='分类')
    name = models.CharField(max_length=200, verbose_name='商品名称')
    subtitle = models.CharField(max_length=500, blank=True, null=True, verbose_name='副标题')
    main_image = models.URLField(max_length=255, blank=True, null=True, verbose_name='主图')
    images = models.TextField(blank=True, null=True, verbose_name='详情图列表(JSON)')
    detail = models.TextField(blank=True, null=True, verbose_name='商品详情HTML')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='最低售价')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='原价')
    stock = models.IntegerField(default=0, verbose_name='总库存')
    sales = models.IntegerField(default=0, verbose_name='销量')
    status = models.IntegerField(default=1, verbose_name='状态 1上架 0下架')
    is_hot = models.BooleanField(default=False, verbose_name='热卖')
    is_new = models.BooleanField(default=False, verbose_name='新品')
    sort = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        ordering = ['sort', '-created_at']

    def __str__(self):
        return self.name


class GoodsSku(models.Model):
    """商品 SKU"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='skus', verbose_name='商品')
    specs = models.CharField(max_length=500, verbose_name='规格描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='SKU价格')
    stock = models.IntegerField(default=0, verbose_name='SKU库存')
    image = models.URLField(max_length=255, blank=True, null=True, verbose_name='SKU配图')
    status = models.IntegerField(default=1, verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'goods_sku'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.goods.name} - {self.specs}'
