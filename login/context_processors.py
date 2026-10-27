

def cart_count(request):
    cart = request.session.get("cart", {})

    return {
        # Number of different products
        "cart_items_count": len(cart),

        # Total units across all products
        "cart_quantity_count": sum(
            int(quantity) for quantity in cart.values()
        ),
    }

