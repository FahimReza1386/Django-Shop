class CartSession:

    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart", {
            "items": []
        })