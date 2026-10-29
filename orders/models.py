
from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("ONLINE", "Online Payment"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )

    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )

    shipping_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    final_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default="COD"
    )

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.full_name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
