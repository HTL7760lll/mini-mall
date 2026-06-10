from django.contrib import admin
from .models import Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    readonly_fields = ['goods_name', 'goods_image', 'sku_specs', 'price', 'quantity', 'total_price']
    extra = 0
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_no', 'member', 'pay_amount', 'pay_status', 'order_status', 'receiver_name', 'receiver_phone', 'created_at']
    list_filter = ['order_status', 'pay_status']
    search_fields = ['order_no', 'member__username', 'receiver_name', 'receiver_phone']
    readonly_fields = ['order_no', 'created_at', 'updated_at']
    inlines = [OrderDetailInline]
    actions = ['ship_orders', 'refund_orders']

    @admin.action(description='发货')
    def ship_orders(self, request, queryset):
        for order in queryset.filter(order_status=1):
            order.order_status = 2
            order.save()

    @admin.action(description='退款')
    def refund_orders(self, request, queryset):
        for order in queryset.filter(pay_status=1):
            order.order_status = 5
            order.save()


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_no', 'goods_name', 'sku_specs', 'price', 'quantity', 'total_price']
    search_fields = ['order_no', 'goods_name']
