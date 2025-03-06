from django.contrib import admin
from .models import CartModel, CartItemModel
# Register your models here.

@admin.register(CartModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=("user", "created_date")

@admin.register(CartItemModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display=("cart", "product", "quantity", "created_date")
