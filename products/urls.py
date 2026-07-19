from django.urls import path
from .views import *

urlpatterns = [
    path(
        "",
        ProductListView.as_view(),
        name="product_list"
    ),

    path(
        "create/",
        ProductCreateView.as_view(),
        name="product_create"
    ),
    
    path(
        "wishlist/",
        wishlist,
        name="wishlist"
    ),

    path(
        "wishlist/add/<int:pk>/",
        add_to_wishlist,
        name="add_to_wishlist"
    ),
    
    path(
        "wishlist/remove/<int:pk>/",
        remove_from_wishlist,
        name="remove_from_wishlist"
    ),
    
    path(
        "<slug:slug>/",
        ProductDetailView.as_view(),
        name="product_detail"
    ),

    path(
        "<slug:slug>/update/",
        ProductUpdateView.as_view(),
        name="product_update"
    ),

    path(
        "<slug:slug>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete"
    ),
]