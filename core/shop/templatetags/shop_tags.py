from shop.models import ProductModel, ProductStatusType
from django import template


register = template.Library()


@register.inclusion_tag("includes/latest_products.html")
def show_latest_products():
    latest_products = ProductModel.objects.filter(status=ProductStatusType.publish.value).order_by("-created_date")[:6]
    return {"latest" : latest_products}

@register.inclusion_tag("includes/similar_products.html")
def show_similar_products(product):
    category_product = product.category.all()
    similar_products = ProductModel.objects.filter(status=ProductStatusType.publish.value, category__in=category_product).order_by("-created_date")[:6]
    return {"similar" : similar_products}

@register.inclusion_tag("includes/discount_products.html")
def show_discount_products():
    discount_products = ProductModel.objects.filter(status=ProductStatusType.publish.value).order_by("-discount_percent")[:6]
    return {"discount" : discount_products}