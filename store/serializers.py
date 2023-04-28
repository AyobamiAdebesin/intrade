"""
This module contains the serializers for the store app.

Each serializer class is used to convert the corresponding
model to JSON and they serve as the external API representation
of the each model.
"""

from rest_framework import serializers
from .models import ProductCatgeory
from .models import User

class UserSerializer(serializers.Serializer):
    """
    This class serializes the User model. 

    Attributes:
        id (int): The primary key for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email of the user.
        phone (str): The phone number of the user.
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone']


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    This class serializes the ProductCategory model.

    Attributes:
        id (int): The primary key for the product category.
        title (str): The title of the product category.
    """

    class Meta:
        model = ProductCatgeory
        fields = ['id', 'title']

class ProductSerializer(serializers.Serializer):
    """
    This class serializes the Product model.

    Attributes:
        id (int): The primary key for the product.
        title (str): The title of the product.
        unit_price (decimal): The unit price of the product.
    """
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    category = ProductCategorySerializer()
    #category = serializers.StringRelatedField()
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset = ProductCatgeory.objects.all()
    # )
