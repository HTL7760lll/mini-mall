from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.cart_list, name='cart_list'),
    path('add/', views.cart_add, name='cart_add'),
    path('update/', views.cart_update, name='cart_update'),
    path('check/<int:pk>/', views.cart_check, name='cart_check'),
    path('remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('count/', views.cart_count, name='cart_count'),
]
