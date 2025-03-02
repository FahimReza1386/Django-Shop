from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ProductModel, ProductCategoryModel, ProductStatusType, ProductImageModel
from django.core.exceptions import FieldError
from django.contrib import messages

# Create your views here.

class ShopProductGridView(ListView):
    template_name="Shop/product-grid.html"
    model=ProductModel
    paginate_by=16


    def get_paginate_by(self, queryset):
        return super().get_paginate_by(queryset)

    def get_queryset(self):
        queryset=ProductModel.objects.filter(status=ProductStatusType.publish.value)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)

        if search_q := self.request.GET.get('q'):
            queryset = queryset.filter(title__icontains=search_q)

        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)

        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)

        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                messages.error(self.request , ("خطا در وارد کردن فیلد"))

        return queryset
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["categories"] = ProductCategoryModel.objects.all()
        return context



class ShopProductDetailView(DetailView):
    template_name = "Shop/product-detail.html"
    queryset=ProductModel.objects.filter(status=ProductStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_img"] = ProductImageModel.objects.filter(product__slug=self.kwargs["slug"])
        return context