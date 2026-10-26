
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    selling_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "discount_price",
            "selling_price",
            "discount_percentage",
            "image_url",
            "stock",
            "is_active",
            "created_at",
        ]
