from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .models import Product, ProductCatgeory
from .serializers import UserSerializer, ProductSerializer
from .serializers import ProductCategorySerializer

# Create your views here.


class ProductList(APIView):
    """
    This class handles the request to list all products.
    """

    def get(self, request):
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserList(APIView):
    """
    This class handles the request to list all users.
    """

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    """
    This class handles the request to retrieve a user.
    """

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ProductDetail(APIView):
    """
    This class handles the request to retrieve a product.
    """

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.order_items.count() > 0:
            return Response({'error': 'Product cannot be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


@api_view(['GET', 'POST'])
def category_list(request):
    """ Fetch all categories from the database """
    if request.method == 'GET':
        categories = ProductCatgeory.objects.annotate(
            product_count=Count('products')).all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(ProductCatgeory.objects.annotate(
        products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = ProductCategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ProductCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    elif request.method == 'DELETE':
        if category.products.count() > 0:
            return Response({'error': 'Category cannot be deleted.'})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
