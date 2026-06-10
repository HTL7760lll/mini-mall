from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('info/', views.profile, name='profile'),

    # 地址
    path('address/', views.address_list, name='address_list'),
    path('address/<int:pk>/', views.address_detail, name='address_detail'),
    path('address/<int:pk>/default/', views.address_set_default, name='address_default'),
]
