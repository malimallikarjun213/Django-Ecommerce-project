from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
     path("address/", views.address_page, name="address"),
    path(
    "confirm/",
    views.confirm_details,
    name="confirm_details",
),

path("confirm/", views.confirm_details, name="confirm_details"),
 path("payment/", views.payment_page, name="payment"),

]

def payment_page(request):
    address = request.session.get("checkout_address")
    cart = request.session.get("cart", {})

    if not address or not cart:
        return redirect("orders:address")

    # Payment must start only after confirmation
    if request.session.get("checkout_step") != "confirm":
        return redirect("orders:confirm_details")

    total = Decimal("0.00")

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(
                pk=product_id,
                is_active=True
            )

            if isinstance(item, dict):
                quantity = int(item.get("quantity", 1))
            else:
                quantity = int(item)

            if quantity < 1:
                continue

            total += product.selling_price * quantity

        except (Product.DoesNotExist, ValueError, TypeError):
            continue

    if total <= 0:
        return redirect("products:cart")

    return render(
        request,
        "orders/payment.html",
        {
            "total": total,
            "payment_status": "pending",
        }
    )