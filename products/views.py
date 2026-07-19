from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.edit import FormMixin

from .models import (
    Product,
    Category,
    Brand,
    Wishlist,
    Review,
)
from .forms import (
    ProductForm,
    ReviewForm,
)

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(
            available=True
        ).select_related(
            "category",
            "brand"
        ).prefetch_related(
            "reviews"
        )

        search = self.request.GET.get("search")
        category = self.request.GET.get("category")
        brand = self.request.GET.get("brand")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            queryset = queryset.filter(
                category_id=category
            )

        if brand:
            queryset = queryset.filter(
                brand_id=brand
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()
        context["brands"] = Brand.objects.all()

        context["featured"] = Product.objects.filter(
            available=True
        ).select_related(
            "category",
            "brand"
        )[:4]

        context["new_products"] = Product.objects.filter(
            available=True
        ).select_related(
            "category",
            "brand"
        ).order_by("-id")[:8]

        return context


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    form_class = ReviewForm

    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.object

        if self.request.user.is_authenticated:
            context["is_in_wishlist"] = Wishlist.objects.filter(
                user=self.request.user,
                product=product
            ).exists()
        else:
            context["is_in_wishlist"] = False

        context["reviews"] = product.reviews.all()

        context["related_products"] = Product.objects.filter(
            category=product.category,
            available=True
        ).select_related(
            "category",
            "brand"
        ).exclude(
            id=product.id
        )[:4]

        context["form"] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        self.object = self.get_object()

        form = self.get_form()

        if form.is_valid():

            review = form.save(commit=False)

            review.user = request.user
            review.product = self.object

            review.save()

            messages.success(
                request,
                "Sharh muvaffaqiyatli qo'shildi."
            )

        return redirect(self.object.get_absolute_url())


class ProductCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    CreateView
):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(
            self.request,
            "Maxsulot muvaffaqiyatli yaratildi."
        )
        return super().form_valid(form)


class ProductUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(
            self.request,
            "Maxsulot muvaffaqiyatli yangilandi."
        )
        return super().form_valid(form)


class ProductDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Product
    template_name = "products/product_delete.html"
    success_url = reverse_lazy("product_list")

    slug_field = "slug"
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        messages.success(
            request,
            "Maxsulot muvaffaqiyatli o'chirildi."
        )
        return super().delete(request, *args, **kwargs)


@login_required
def wishlist(request):

    items = Wishlist.objects.filter(
        user=request.user
    ).select_related(
        "product"
    )

    return render(
        request,
        "products/wishlist.html",
        {
            "items": items
        }
    )


@login_required
def add_to_wishlist(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    messages.success(
        request,
        "Mahsulot sevimlilar ro'yxatiga qo'shildi."
    )

    return redirect(
        "product_detail",
        slug=product.slug
    )


@login_required
def remove_from_wishlist(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()

    messages.success(
        request,
        "Mahsulot sevimlilar ro'yxatidan o'chirildi."
    )

    return redirect(
        "product_detail",
        slug=product.slug
    )

