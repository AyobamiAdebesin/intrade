from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('carts/', views.CartCreation.as_view(), name='cart_list'),
    path('carts/<pk>', views.CartDetail.as_view(), name='cart_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>', views.category_detail, name='category_detail'),
] 