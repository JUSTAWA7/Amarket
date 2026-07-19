from django.urls import path
from . import views

urlpatterns = [

    path("", views.cart_view, name="cart"),

    path("add/<int:pk>/", views.add_to_cart, name="add_to_cart"),

    path("remove/<int:pk>/",
         views.remove_from_cart,
         name="remove_from_cart"),

    path("plus/<int:pk>/",
         views.increase_quantity,
         name="increase_quantity"),

    path("minus/<int:pk>/",
         views.decrease_quantity,
         name="decrease_quantity"),
]