
import json
from decimal import Decimal
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from categories.models import Category
from products.models import Product


API_URL = "https://dummyjson.com/products?limit=100"


class Command(BaseCommand):
    help = "Import sample products from DummyJSON"

    def handle(self, *args, **options):
        request = Request(
            API_URL,
            headers={"User-Agent": "ProShopAI-Django"}
        )

        try:
            with urlopen(request, timeout=20) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )
        except Exception as exc:
            raise CommandError(
                f"Could not fetch products: {exc}"
            )

        imported = 0
        skipped = 0

        with transaction.atomic():
            for item in data.get("products", []):
                title = item.get("title", "").strip()

                if not title:
                    skipped += 1
                    continue

                category_name = (
                    item.get("category", "Other")
                    .replace("-", " ")
                    .title()
                )

                category, _ = Category.objects.get_or_create(
                    name=category_name,
                    defaults={
                        "description": f"Products in {category_name}"
                    }
                )

                if Product.objects.filter(name=title).exists():
                    skipped += 1
                    continue

                price = Decimal(str(item.get("price", 0)))

                if price <= 0:
                    skipped += 1
                    continue

                discount_percent = Decimal(
                    str(item.get("discountPercentage", 0))
                )

                discount_price = (
                    price * (
                        Decimal("1")
                        - discount_percent / Decimal("100")
                    )
                ).quantize(Decimal("0.01"))

                if discount_price <= 0 or discount_price >= price:
                    discount_price = None

                Product.objects.create(
                    category=category,
                    name=title[:200],
                    description=item.get("description", ""),
                    price=price.quantize(Decimal("0.01")),
                    discount_price=discount_price,
                    image_url=item.get("thumbnail", ""),
                    stock=max(0, int(item.get("stock", 0))),
                    is_active=True,
                )

                imported += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import finished. Added: {imported}, "
                f"skipped: {skipped}"
            )
        )
