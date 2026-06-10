from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member, Address


@admin.register(Member)
class MemberAdmin(UserAdmin):
    list_display = ['id', 'username', 'nickname', 'phone', 'role', 'status', 'is_staff', 'date_joined']
    list_filter = ['role', 'status', 'is_staff']
    search_fields = ['username', 'nickname', 'phone']
    ordering = ['-date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('额外信息', {'fields': ('nickname', 'avatar', 'gender', 'phone', 'role', 'status')}),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'member', 'receiver_name', 'receiver_phone', 'province', 'city', 'is_default', 'created_at']
    list_filter = ['is_default', 'province', 'city']
    search_fields = ['receiver_name', 'receiver_phone']
