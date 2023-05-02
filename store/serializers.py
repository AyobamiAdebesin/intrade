"""
This module contains the serializers for the store app.

Each serializer class is used to convert the corresponding
model to JSON and they serve as the external API representation
of the each model.
"""

from rest_framework import serializers
from .models import ProductCatgeory
from .models import User, Product, Cart, CartItem


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
        fields = ['id', 'title', 'product_count']
        read_only_fields = ['product_count', 'id']

    product_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    """
    This class serializes the Product model.

    Attributes:
        id (int): The primary key for the product.
        title (str): The title of the product.
        unit_price (decimal): The unit price of the product.
    """

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_prce')
    class Meta:
        model = Product
        fields = ['title', 'description',
                  'price', 'inventory', 'category']
    # category = ProductCategorySerializer()
    # category = serializers.StringRelatedField()
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset = ProductCatgeory.objects.all()
    # )


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    """
    This class serializes the CartItem model.

    Attributes:
        id (int): The primary key for the cart item.
        created_at (datetime): The date and time the cart item was created.
        updated_at (datetime): The date and time the cart item was last updated.
        cart (Cart): The cart the cart item belongs to.
        product (Product): The product the cart item belongs to.
        quantity (int): The quantity of the product in the cart item.
    """
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    """
    This class serializes the Cart model.

    Attributes:
        id (int): The primary key for the cart.
        created_at (datetime): The date and time the cart was created.
        updated_at (datetime): The date and time the cart was last updated.
        user (User): The user that owns the cart.
        products (Product): The products in the cart.
    """
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id']

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])
