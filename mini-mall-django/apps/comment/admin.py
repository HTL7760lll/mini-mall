from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods', 'member', 'star', 'is_show', 'created_at']
    list_filter = ['is_show', 'star']
    list_editable = ['is_show']
    search_fields = ['content', 'goods__name', 'member__username']
