from django.contrib import admin
from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'link_type', 'sort', 'status', 'created_at']
    list_filter = ['status', 'link_type']
    list_editable = ['sort', 'status']
    search_fields = ['title']
