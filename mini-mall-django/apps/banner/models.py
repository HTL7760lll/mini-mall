from django.db import models


class Banner(models.Model):
    """轮播图"""
    LINK_TYPES = (
        (1, '不跳转'),
        (2, '商品详情'),
        (3, '分类列表'),
    )
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='标题')
    image_url = models.URLField(max_length=255, verbose_name='图片URL')
    link_url = models.URLField(max_length=255, blank=True, null=True, verbose_name='跳转链接')
    link_type = models.IntegerField(default=1, choices=LINK_TYPES, verbose_name='跳转类型')
    link_target = models.CharField(max_length=100, blank=True, null=True, verbose_name='跳转参数')
    sort = models.IntegerField(default=0, verbose_name='排序')
    status = models.IntegerField(default=1, verbose_name='1启用 0禁用')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.title or f'Banner #{self.id}'
