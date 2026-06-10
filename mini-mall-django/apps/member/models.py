from django.contrib.auth.models import AbstractUser
from django.db import models


class Member(AbstractUser):
    """自定义用户模型"""
    ROLE_CHOICES = (
        ('USER', '普通用户'),
        ('ADMIN', '管理员'),
    )
    GENDER_CHOICES = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
    avatar = models.URLField(max_length=255, blank=True, null=True, verbose_name='头像')
    gender = models.IntegerField(default=0, choices=GENDER_CHOICES, verbose_name='性别')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    role = models.CharField(max_length=20, default='USER', choices=ROLE_CHOICES, verbose_name='角色')
    status = models.IntegerField(default=1, verbose_name='状态 1正常 0禁用')

    class Meta:
        db_table = 'member'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.nickname or self.username

    @property
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_staff


class Address(models.Model):
    """收货地址"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    receiver_name = models.CharField(max_length=30, verbose_name='收货人')
    receiver_phone = models.CharField(max_length=20, verbose_name='联系电话')
    province = models.CharField(max_length=20, verbose_name='省')
    city = models.CharField(max_length=20, verbose_name='市')
    district = models.CharField(max_length=50, verbose_name='区')
    detail = models.CharField(max_length=200, verbose_name='详细地址')
    is_default = models.BooleanField(default=False, verbose_name='默认地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'address'
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f'{self.receiver_name} / {self.receiver_phone}'
