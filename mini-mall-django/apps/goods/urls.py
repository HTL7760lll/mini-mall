from django.urls import path
from . import views

urlpatterns = [
    path('category/tree/', views.category_tree, name='category_tree'),
    path('page/', views.goods_list, name='goods_list'),
    path('search/', views.goods_search, name='goods_search'),
    path('detail/<int:pk>/', views.goods_detail, name='goods_detail'),
    path('hot/', views.goods_hot, name='goods_hot'),
    path('new/', views.goods_new, name='goods_new'),
]
