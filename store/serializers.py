"""
This module contains the serializers for the store app.

Each serializer class is used to convert the corresponding
model to JSON and they serve as the external API representation
of the each model.
"""

from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .signals import order_created
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    """
    This class serializes the Collection model.

    Attributes:
        id (int): The primary key for the collection.
        title (str): The title of the collection.
        products_count (int): The number of products in the collection.
    """
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    """
    This class serializes the Product model.

    Attributes:
        id (int): The primary key for the product.
        title (str): The title of the product.
        description (str): The description of the product.
        slug (str): The slug of the product.
        inventory (int): The number of the product in inventory.
        unit_price (decimal): The unit price of the product.
        price_with_tax (decimal): The unit price of the product with tax.
        collection (Collection): The collection the product belongs to.
    """
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    """
    This class serializes the Review model.

    Attributes:
        id (int): The primary key for the review.
        date (datetime): The date and time the review was created.
        name (str): The name of the reviewer.
        description (str): The description of the review.
    """
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    """
    This class serializes the Product model.
    But only returns the id, title, and unit_price fields.

    Attributes:
        id (int): The primary key for the product.
        title (str): The title of the product.
        unit_price (decimal): The unit price of the product.
    """
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    """
    This class serializes the CartItem model.

    Attributes:
        id (int): The primary key for the cart item.
        product (SimpleProductSerializer): The product in the cart item.
        quantity (int): The quantity of the product in the cart item.
        total_price (decimal): The total price of the cart item.
    """
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    """
    This class serializes the Cart model.

    Attributes:
        id (uuid): The primary key for the cart.
        items (CartItemSerializer): The cart items in the cart.
        total_price (decimal): The total price of the cart.
    """
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    """
    This class serializes the CartItem model for adding a new cart item.

    Attributes:
        product_id (int): The primary key for the product.
        quantity (int): The quantity of the product in the cart item.
    """
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        """
        This method creates a new cart item or updates an existing one.
        """
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    """
    This class serializes the CartItem model for updating an existing cart item.

    Attributes:
        quantity (int): The quantity of the product in the cart item.
    """

    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    """
    This class serializes the Customer model.

    Attributes:
        id (int): The primary key for the customer.
        user_id (int): The primary key for the user.
        phone (str): The phone number of the customer.
        birth_date (date): The birth date of the customer.
        membership (str): The membership of the customer.
    """
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    """
    This class serializes the OrderItem model.

    Attributes:
        id (int): The primary key for the order item.
        product (SimpleProductSerializer): The product in the order item.
        unit_price (decimal): The unit price of the product in the order item.
        quantity (int): The quantity of the product in the order item.
    """
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """
    This class serializes the Order model.

    Attributes:
        id (int): The primary key for the order.
        customer (CustomerSerializer): The customer who placed the order.
        placed_at (datetime): The date and time the order was placed.
        payment_status (str): The payment status of the order.
        items (OrderItemSerializer): The order items in the order.
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
    """
    This class serializes the Order model for updating an existing order.

    Attributes:
        payment_status (str): The payment status of the order.
    """
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
    """
    This class serializes the Order model for creating a new order. It also
    validates the cart ID and checks if the cart is empty.

    Attributes:
        cart_id (uuid): The primary key for the cart.
    """
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']

            customer = Customer.objects.get(
                user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects \
                .select_related('product') \
                .filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order)

            return order
