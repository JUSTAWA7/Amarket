from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from cart.models import Cart
from .models import Order, OrderItem


@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart")

    total = sum(item.total_price for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()

    return redirect("order_history")


@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders/history.html",
        {
            "orders": orders
        }
    )