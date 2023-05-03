from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4


class Promotion(models.Model):
    """
    This class represents a promotion in the store.

    Attributes:
        id (int): The primary key for the promotion.
        description (str): The description of the promotion.
        discount (float): The discount of the promotion.
    """
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    """
    This class represents a collection of products (product category) in the store.

    Attributes:
        id (int): The primary key for the product collection.
        title (str): The title of the product collection.
        featured_product (Product): The featured product of the product collection.
    """
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    """
    This class represents a product in the store.

    Attributes:
        id (int): The primary key for the product.
        title (str): The title of the product.
        slug (str): The slug of the product.
        description (str): The description of the product.
        unit_price (decimal): The unit price of the product.
        inventory (int): The number of the product in inventory.
        last_update (datetime): The date and time the product was last updated.
        collection (Collection): The product collection the product belongs to.
        promotions (Promotion): The promotions the product belongs to.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    """
    This class represents a customer in the store.

    Attributes:
        id (int): The primary key for the customer.
        phone (str): The phone number of the customer.
        birth_date (datetime): The birth date of the customer.
        membership (str): The membership status of the customer.
        user (User): The user the customer belongs to.
    """

    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]


class Order(models.Model):
    """ This class represents an order in the store.

    Attributes:
        id (int): The primary key for the order.
        placed_at (datetime): The date and time the order was placed.

        PAYMENT_STATUS_PENDING (str): The order is pending payment.
        PAYMENT_STATUS_COMPLETE (str): The order has been paid for.
        PAYMENT_STATUS_FAILED (str): The order payment failed.
        PAYMENT_STATUS_CHOICES (list): The list of payment status choices.
        
        payment_status (str): The payment status of the order.
        customer (Customer): The customer who placed the order.
    """
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]


class OrderItem(models.Model):
    """ This class represents an order item in the store.

    Attributes:
        id (int): The primary key for the order item.
        order (Order): The order the order item belongs to.
        product (Product): The product the order item belongs to.
        quantity (int): The quantity of the order item.
        unit_price (decimal): The unit price of the order item.
    """
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    """
    This class represents an address in the store.

    Attributes:
        id (int): The primary key for the address.
        street (str): The street of the address.
        city (str): The city of the address.
        customer (Customer): The customer the address belongs to.
    """
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    """
    This class represents a cart in the store.

    Attributes:
        id (uuid): The primary key for the cart. We use a UUIDField to generate a unique ID for a cart.
        This will act as a kind of security so that random users cannot access other users' carts.
        Since we are not tying the cart to a user, we will use a UUIDField instead of a AutoField.
        
        created_at (datetime): The date and time the cart was created.
    """
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    """
    This class represents a cart item in the store.

    Attributes:
        id (int): The primary key for the cart item.
        cart (Cart): The cart the cart item belongs to.
        product (Product): The product the cart item belongs to.
        quantity (int): The quantity of the cart item.
    """
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    """
    This class represents the review of a product in the store.

    Attributes:
        id (int): The primary key for the review.
        product (Product): The product the review belongs to.
        name (str): The name of the reviewer.
        description (str): The description of the review.
        date (datetime): The date the review was created.
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
