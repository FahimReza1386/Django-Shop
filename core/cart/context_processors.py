from .cart import CartSession


def cart_prosessor(request):
    cart = CartSession(session=request.session)
    return {"cart" : cart}