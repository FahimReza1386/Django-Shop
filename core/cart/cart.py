from shop.models import ProductModel, ProductStatusType

class CartSession:
    total_payment_price = 0
    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart", {
            "items": []
        })

    def add_product(self, product_id, qty):
        quantity = int(qty)
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                plus_qty = int(item["quantity"]) + quantity
                if plus_qty <=10:
                    item["quantity"] += quantity
                    break
                else:
                    item["quantity"] = 10
                    break
        else:
            new_item = {
                "product_id":product_id,
                "quantity":int(qty)
            }


            self._cart["items"].append(new_item)
        
        self.save()

    def update_product_qty(self, product_id, qty):
        quantity = int(qty)
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] = quantity
                break
        else:
            return True

        self.save()


    def remove_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                self._cart["items"].remove(item)
                break
        else:
            return

        self.save()
    
    def get_total_payment_price(self):
        return self.total_payment_price
    
    def clear(self):
        self.session["cart"] = {
            "items": []
        }

        self.save()


    
    def get_total_quantity(self):
        total_qty = len(self._cart["items"])
        return total_qty
    
    def get_cart_dict(self):
        return self._cart
    
    def get_cart_item(self):
        cart_items = self._cart["items"]
        self.total_payment_price = 0
        for item in cart_items:
            product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            item["product_obj"] = product_obj
            total_price = int(item["quantity"]) * product_obj.get_price_after_sale()
            item["total_price"] = total_price
            self.total_payment_price += total_price

        return cart_items
        


    def save(self):
        self.session.modified = True