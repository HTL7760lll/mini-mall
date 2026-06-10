from django.urls import path
from . import views

urlpatterns = [
    path('goods/<int:goods_id>/', views.goods_comments, name='goods_comments'),
    path('save/', views.comment_save, name='comment_save'),
]
