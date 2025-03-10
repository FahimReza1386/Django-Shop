from shop.models import ProductModel, ProductStatusType
from cart.models import CartModel, CartItemModel

class CartSession:
    total_payment_price = 0
    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart", {"items": []})

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
        
    def sync_cart_items_from_db(self, user):
        cart,created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)
        for cart_item in cart_items:
            for item in self._cart["items"]:
                if str(cart_item.product.id) == item["product_id"]:
                    cart_item.quantity = item["quantity"]
                    cart_item.save()    
                    break
            else:
                new_item = {"product_id":str(cart_item.product.id),"quantity" : cart_item.quantity}
                self._cart["items"].append(new_item)
        self.merge_session_cart_in_db(user=user)
        self.save()

    def merge_session_cart_in_db(self, user):
        cart,created = CartModel.objects.get_or_create(user=user)
        
        for item in self._cart["items"]:
            product_obj = ProductModel.objects.get(id=item["product_id"],status=ProductStatusType.publish.value)
            
            cart_items,created = CartItemModel.objects.get_or_create(cart=cart, product=product_obj)
            cart_items.quantity = item["quantity"]
            cart_items.save()

        session_product_ids = [item["product_id"] for item in self._cart["items"]]
        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()

    def save(self):
        self.session.modified = True