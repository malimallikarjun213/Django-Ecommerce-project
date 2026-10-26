
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from django.shortcuts import redirect


from .models import Category
from .serializers import CategorySerializer
from products.models import Product


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def category_page(request):
    categories = Category.objects.filter(is_active=True)

    return render(
        request,
        'categories/category_list.html',
        {'categories': categories}
    )


def category_detail(request, category_id):
    category = get_object_or_404(
        Category,
        id=category_id,
        is_active=True
    )

    products = Product.objects.filter(
        category=category,
        is_active=True
    ).select_related('category')

    return render(
        request,
        'categories/category_detail.html',
        {
            'category': category,
            'products': products,
        }
    )
def add_to_cart(request, id):
    product = get_object_or_404(
        Product,
        id=id,
        is_active=True
    )

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
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
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(
        request,
        'products/cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )