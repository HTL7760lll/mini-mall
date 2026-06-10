from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'member', 'goods', 'sku', 'quantity', 'checked', 'created_at']
    list_filter = ['checked']
    search_fields = ['member__username', 'goods__name']
