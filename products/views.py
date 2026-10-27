
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import generics

from categories.models import Category
from .models import Product, Review
from .serializers import ProductSerializer


# 1. Product List, Search and Category Filter
def product_list(request):
    products = Product.objects.filter(
        is_active=True
    ).select_related("category")

    categories = Category.objects.filter(is_active=True)
    category_id = request.GET.get("category", "")
    search = request.GET.get("q", "").strip()

    if category_id.isdigit():
        products = products.filter(category_id=int(category_id))

    if search:
        products = products.filter(name__icontains=search)

    return render(request, "products/product_list.html", {
        "products": products,
        "categories": categories,
        "selected_category": category_id,
        "search": search,
    })


# 2. Products by Category
def category_products(request, category_id):
    category = get_object_or_404(
        Category, id=category_id, is_active=True
    )

    products = Product.objects.filter(
        category=category,
        is_active=True
    ).select_related("category")

    return render(request, "products/product_list.html", {
        "products": products,
        "categories": Category.objects.filter(is_active=True),
        "current_category": category,
        "selected_category": str(category.id),
        "search": "",
    })


# 3. Product Details and Reviews
def product_detail(request, id):
    product = get_object_or_404(
        Product, id=id, is_active=True
    )

    reviews = product.reviews.select_related(
        "user"
    ).order_by("-created_at")

    return render(request, "products/product_detail.html", {
        "product": product,
        "reviews": reviews,
    })


# 4. Add Product Review
@login_required
def add_review(request, id):
    product = get_object_or_404(
        Product, id=id, is_active=True
    )

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        rating = request.POST.get("rating", "")
        comment = request.POST.get("comment", "").strip()

        try:
            validate_email(email)
        except ValidationError:
            messages.error(
                request, "Please enter a valid email address."
            )
            return redirect("product_detail", id=product.id)

        if not rating.isdigit() or not 1 <= int(rating) <= 5:
            messages.error(
                request, "Please select a rating from 1 to 5."
            )
        elif not comment:
            messages.error(
                request, "Please write your review."
            )
        else:
            Review.objects.create(
                product=product,
                user=request.user,
                email=email,
                rating=int(rating),
                comment=comment
            )
            messages.success(
                request, "Your review has been submitted!"
            )

    return redirect("product_detail", id=product.id)


# 5. Product API
class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.filter(
            is_active=True
        ).select_related("category")

        category_id = self.request.query_params.get("category")
        search = self.request.query_params.get("search", "").strip()

        if category_id and category_id.isdigit():
            products = products.filter(
                category_id=int(category_id)
            )

        if search:
            products = products.filter(
                name__icontains=search
            )

        return products

# 6. Add to Cart
def add_to_cart(request, id):
    product = get_object_or_404(
        Product, id=id, is_active=True
    )

    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect("product_list")

    cart = request.session.get("cart", {})
    product_id = str(product.id)

    current_quantity = cart.get(product_id, 0)

    if current_quantity >= product.stock:
        messages.warning(
            request, "You cannot add more than the available stock."
        )
    else:
        cart[product_id] = current_quantity + 1
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(
            request, f"{product.name} added to your cart."
        )

    return redirect("cart")


# 7. Shopping Cart
def cart_view(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(
                id=int(product_id),
                is_active=True
            )
        except (Product.DoesNotExist, ValueError):
            continue

        subtotal = product.selling_price * quantity
        total += subtotal

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    return render(request, "products/cart.html", {
        "cart_items": cart_items,
        "total": total,
    })


def update_cart_quantity(request, id):
    from django.views.decorators.http import require_POST

    if request.method != "POST":
        return redirect("cart")

    cart = request.session.get("cart", {})
    product_id = str(id)

    if product_id not in cart:
        return redirect("cart")

    product = get_object_or_404(Product, id=id, is_active=True)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        return redirect("cart")

    if quantity < 1:
        quantity = 1

    if quantity > product.stock:
        quantity = product.stock

    if quantity == 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, id):
    if request.method != "POST":
        return redirect("cart")

    cart = request.session.get("cart", {})
    cart.pop(str(id), None)

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")
