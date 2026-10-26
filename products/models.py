
from django.db import models
from django.core.validators import MinValueValidator
from categories.models import Category


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.01)]
    )

    image_url = models.URLField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def selling_price(self):
        if self.discount_price is not None:
            return self.discount_price
        return self.price

    @property
    def discount_percentage(self):
        if (
            self.discount_price is not None
            and self.price > 0
            and self.discount_price < self.price
        ):
            return round(
                (self.price - self.discount_price)
                / self.price * 100
            )
        return 0
from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    email = models.EmailField(default="")
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.rating} stars"