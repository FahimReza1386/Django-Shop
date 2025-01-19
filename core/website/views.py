from django.shortcuts import render
from django.views.generic import TemplateView
from cart.cart import CartSession
# Create your views here.


class IndexView(TemplateView):
    template_name="website/index.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        cart = CartSession(session=self.request.session)
        context["cart_items"] = cart.get_cart_item()
        context["total_price"] = cart.get_total_payment_price()
        
        return context

class AboutView(TemplateView):
    template_name="website/about.html"

class ContactView(TemplateView):
    template_name="website/contact.html"
