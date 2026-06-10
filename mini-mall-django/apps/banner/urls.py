from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.banner_list, name='banner_list'),
]
