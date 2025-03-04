from django.contrib import admin
from .models import OrderModel, OrderItemsModel, CouponModel
# Register your models here.

@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=("user", "total_price", "coupon", "status", "address")

@admin.register(OrderItemsModel)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display=("order", "product", "quantity", "price")

@admin.register(CouponModel)
class CouponModelModelAdmin(admin.ModelAdmin):
    list_display=("code", "discount_percent", "max_limit_usage", "used_by_count","expiration_date")

    def used_by_count(self, obj):
        return obj.used_by.all().count()

