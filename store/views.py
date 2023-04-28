from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .models import Product
from .serializers import UserSerializer, ProductSerializer

# Create your views here.

@api_view(['GET'])
def user_list(request):
    """
    This function handles the request to list all users.
    """
    users = User.objects.all()[:5]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view()
def user_detail(request, pk):
    """
    This function handles the request to retrieve a user.
    """
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view()
def product_list(request):
    try:
        products = Product.objects.select_related('category').all()
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view()
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

# @api_view(['GET'])
# def get_products_by_category(request, pk):
#     """
#     Get all the products in the producst category
#     table by category_id = pk
#     """

#     products = Product.objects.select_related('category').filter(category_id=pk)
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)