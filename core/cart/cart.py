class CartSession:
    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart", {
            "items": []
        })

    def add_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] += 1
                break
        else:
            new_item = {
                "product_id":product_id,
                "quantity":1
            }

            self._cart["items"].append(new_item)
        
        self.save()

    
    def get_total_quantity(self):
        total_qty = len(self._cart["items"])
        return total_qty


    def save(self):
        self.session.modified = True