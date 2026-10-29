
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from products.models import Product


from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product


def address_page(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        pincode = request.POST.get("pincode", "").strip()

        if not all([
            full_name, email, phone, address,
            city, state, pincode
        ]):
            messages.error(
                request, "Please fill in all address fields."
            )

        elif not phone.isdigit() or not 10 <= len(phone) <= 15:
            messages.error(request, "Enter a valid phone number.")

        elif not pincode.isdigit() or len(pincode) != 6:
            messages.error(request, "Enter a valid 6-digit pincode.")

        else:
            request.session["checkout_address"] = {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "address": address,
                "city": city,
                "state": state,
                "pincode": pincode,
            }

            request.session["checkout_step"] = "address"
            request.session.pop("payment_verified", None)

            return redirect("orders:confirm_details")

    return render(request, "orders/address.html")



def confirm_details(request):
    address = request.session.get("checkout_address")

    if not address:
        return redirect("orders:address")

    cart = request.session.get("cart", {})

    cart_items = []
    subtotal = Decimal("0.00")

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(
                pk=product_id,
                is_active=True
            )

            # FIX: Cart item integer किंवा dictionary असू शकतो
            if isinstance(item, dict):
                quantity = int(item.get("quantity", 1))
            else:
                quantity = int(item)

            if quantity < 1:
                continue

            price = product.selling_price
            item_subtotal = price * quantity
            subtotal += item_subtotal

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "price": price,
                "subtotal": item_subtotal,
            })

        except (Product.DoesNotExist, ValueError, TypeError):
            continue

    if not cart_items:
        return redirect("products:cart")

    discount = Decimal("0.00")
    shipping = Decimal("0.00")
    final_amount = subtotal - discount + shipping

    context = {
        "address": address,
        "cart_items": cart_items,
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "final_amount": final_amount,
    }
    request.session["checkout_step"] = "confirm"

    return render(
        request,
        "orders/confirm_details.html",
        context
    )
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