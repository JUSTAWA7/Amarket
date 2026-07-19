from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

from django.views.generic import TemplateView
from django.contrib.auth.models import User

from products.models import Product
from orders.models import Order



class DashboardView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    TemplateView
):

    template_name = "core/dashboard.html"


    def test_func(self):
        return self.request.user.is_staff


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)


        context["product_count"] = Product.objects.count()

        context["user_count"] = User.objects.count()

        context["order_count"] = Order.objects.count()


        context["latest_orders"] = (
            Order.objects
            .order_by("-created_at")[:5]
        )


        context["latest_products"] = (
            Product.objects
            .order_by("-created_at")[:5]
        )


        return context