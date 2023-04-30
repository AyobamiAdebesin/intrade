""" This module contains the models for the store app. """
import uuid
from django.db import models



class ProductCatgeory(models.Model):
    """
    This class represents a product category in the store.

    Attributes:
        id (int): The primary key for the product category.
        title (str): The title of the product category.
        created_at (datetime): The date and time the product category was created.
        updated_at (datetime): The date and time the product category was last updated.
    """
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    class Meta:
        db_table = 'product_categories'
        ordering = ['title']


class Product(models.Model):
    """
    This class represents a product in the store.

    Attributes:
        id (int): The primary key for the product.
        created_at (datetime): The date and time the product was created.
        updated_at (datetime): The date and time the product was last updated.
        title (str): The title of the product.
        description (str): The description of the product.
        price (decimal): The price of the product.
        inventory (int): The number of the product in inventory.
        collection (ProductCatgeory): The product category the product belongs to.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    category = models.ForeignKey(ProductCatgeory, on_delete=models.PROTECT, related_name='products')

    class Meta:
        db_table = 'products'


class User(models.Model):
    """
    This class represents a user in the store.

    Attributes:
        id (int): The primary key for the user.
        created_at (datetime): The date and time the user was created.
        updated_at (datetime): The date and time the user was last updated.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email of the user.
        phone (str): The phone number of the user.
        password (str): The password of the user.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['id', 'first_name', 'last_name', 'email']),
        ]


class Order(models.Model):
    """
    This class represents an order in the store.

    Attributes:
        id (int): The primary key for the order.
        placed_at (datetime): The date and time the order was created.
        user (User): The user who placed the order.

        PAYMENT_STATUS_PENDING (str): The order is pending payment.
        PAYMENT_STATUS_COMPLETE (str): The order has been paid for.
        PAYMENT_STATUS_FAILED (str): The order payment failed.
        PAYMENT_STATUS_CHOICES (list): The list of payment status choices.
        payment_status (str): The payment status of the order.
    """
    placed_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    # This is an enum for the payment status of the order.
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model):
    """
    This class represents an order item in the store.

    Attributes:
        id (int): The primary key for the order item.
        order (Order): The order the order item belongs to.
        product (Product): The product the order item is for.
        quantity (int): The quantity of the product ordered.
        unit_price (decimal): The unit price of the product ordered.
    """
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'order_items'


class Cart(models.Model):
    """
    This class represents a cart in the store.

    Attributes:
        id (int): The primary key for the cart.
        created_at (datetime): The date and time the cart was created.
        updated_at (datetime): The date and time the cart was last updated.
        user (User): The user who owns the cart.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'


class CartItem(models.Model):
    """
    This class represents a cart item in the store.

    Attributes:
        id (int): The primary key for the cart item.
        cart (Cart): The cart the cart item belongs to.
        product (Product): The product the cart item is for.
        quantity (int): The quantity of the product ordered.
        unit_price (decimal): The unit price of the product ordered.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    

    class Meta:
        unique_together = [['cart', 'product']]

    class Meta:
        db_table = 'cart_items'
