from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from .cart import CartSession
from django.http import JsonResponse

# Create your views here.


class SessionAddProductView(CreateView):
    
    def post(self, request, *args, **kwargs):
        cart = CartSession(session=self.request.session)
        product_id = self.request.POST.get("product_id")
        if product_id:
            cart.add_product(product_id)

        return JsonResponse({"cart":"s"})