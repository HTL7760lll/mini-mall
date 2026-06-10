import uuid
from django.db import models
from apps.member.models import Member, Address
from apps.goods.models import Goods, GoodsSku


class Order(models.Model):
    """订单"""
    ORDER_STATUS = (
        (0, '待付款'),
        (1, '待发货'),
        (2, '待收货'),
        (3, '已完成'),
        (4, '已取消'),
        (5, '已退款'),
    )
    PAY_STATUS = (
        (0, '未支付'),
        (1, '已支付'),
    )
    order_no = models.CharField(max_length=32, unique=True, verbose_name='订单号')
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='orders', verbose_name='用户')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')
    freight = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='运费')
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实付金额')
    pay_type = models.IntegerField(default=1, verbose_name='支付方式')
    pay_status = models.IntegerField(default=0, choices=PAY_STATUS, verbose_name='支付状态')
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name='支付时间')
    order_status = models.IntegerField(default=0, choices=ORDER_STATUS, verbose_name='订单状态')
    # 地址快照
    receiver_name = models.CharField(max_length=30, verbose_name='收货人')
    receiver_phone = models.CharField(max_length=20, verbose_name='收货电话')
    receiver_address = models.CharField(max_length=300, verbose_name='收货地址')
    remark = models.CharField(max_length=500, blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'订单 {self.order_no}'


class OrderDetail(models.Model):
    """订单详情 (商品快照)"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details', verbose_name='订单')
    order_no = models.CharField(max_length=32, verbose_name='订单号(冗余)')
    goods = models.ForeignKey(Goods, on_delete=models.PROTECT, verbose_name='商品')
    sku = models.ForeignKey(GoodsSku, on_delete=models.PROTECT, verbose_name='SKU')
    goods_name = models.CharField(max_length=200, verbose_name='商品名称')
    goods_image = models.CharField(max_length=255, blank=True, null=True, verbose_name='商品主图')
    sku_specs = models.CharField(max_length=500, verbose_name='SKU规格')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    quantity = models.IntegerField(verbose_name='数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_detail'
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.goods_name} x{self.quantity}'
