from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.order_submit, name='order_submit'),
    path('pay/', views.order_pay, name='order_pay'),
    path('cancel/<int:pk>/', views.order_cancel, name='order_cancel'),
    path('confirm/<int:pk>/', views.order_confirm, name='order_confirm'),
    path('page/', views.order_list, name='order_list'),
    path('detail/<int:pk>/', views.order_detail, name='order_detail'),
]
