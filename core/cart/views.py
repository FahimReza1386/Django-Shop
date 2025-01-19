from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from .cart import CartSession
from django.http import JsonResponse

# Create your views here.


class SessionAddProductView(CreateView):
    
    def post(self, request, *args, **kwargs):
        cart = CartSession(session=self.request.session)
        product_id = self.request.POST.get("product_id")
        qty = self.request.POST.get("quantity")
        if product_id and qty:
            cart.add_product(product_id, qty)

        return JsonResponse({"cart":cart.get_cart_dict(), "total_quantity":cart.get_total_quantity()})
    
class SessionCartSummaryView(TemplateView):
    template_name = "Cart/cart-summary.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(session=self.request.session)
        context["total_price"] = cart.get_total_payment_price
        context["cart_items"] = cart.get_cart_item()

        return context
