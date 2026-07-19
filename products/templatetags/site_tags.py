from django import template
from django.utils.timezone import now
from products.models import Product

register = template.Library()

@register.simple_tag
def current_year():
    return now().year

@register.simple_tag
def product_count():
    return Product.objects.count()