from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "discount_price",
        "stock",
        "is_active",
    )

    list_filter = ("category", "is_active")
    search_fields = ("name",)
