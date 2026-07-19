from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart
from products.models import Product


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    messages.success(
    request,
    "Mahsulot savatga qoshildi"
    )
    return redirect("cart")



@login_required
def cart_view(request):

    items = Cart.objects.filter(user=request.user)

    total = sum(item.total_price for item in items)

    return render(
        request,
        "cart/cart.html",
        {
            "items": items,
            "total": total
        }
    )
    


@login_required
def remove_from_cart(request, pk):

    item = get_object_or_404(
        Cart,
        pk=pk,
        user=request.user
    )

    item.delete()
    
    messages.warning(
    request,
    " Mahsulot savatdan o'chirildi."
    )
    return redirect("cart")



@login_required
def increase_quantity(request, pk):

    item = get_object_or_404(
        Cart,
        pk=pk,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect("cart")



@login_required
def decrease_quantity(request, pk):

    item = get_object_or_404(
        Cart,
        pk=pk,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")