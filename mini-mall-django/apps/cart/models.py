from django.db import models
from apps.member.models import Member
from apps.goods.models import Goods, GoodsSku


class Cart(models.Model):
    """购物车"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='carts', verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    sku = models.ForeignKey(GoodsSku, on_delete=models.CASCADE, verbose_name='SKU')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    checked = models.BooleanField(default=True, verbose_name='是否选中')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ['member', 'sku']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.member.username} - {self.goods.name} x{self.quantity}'
