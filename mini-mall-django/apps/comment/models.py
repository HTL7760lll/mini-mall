from django.db import models
from apps.member.models import Member
from apps.goods.models import Goods


class Comment(models.Model):
    """商品评价"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='comments', verbose_name='商品')
    order = models.ForeignKey('order.Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='订单')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='用户')
    content = models.CharField(max_length=1000, verbose_name='评价内容')
    star = models.IntegerField(verbose_name='评分 1-5')
    images = models.TextField(blank=True, null=True, verbose_name='图片JSON')
    is_show = models.BooleanField(default=True, verbose_name='是否显示')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'comment'
        verbose_name = '商品评价'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.member.username} ★{self.star} — {self.goods.name}'
