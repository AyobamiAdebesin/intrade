from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>', views.product_detail, name='product_detail')
]