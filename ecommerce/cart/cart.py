from decimal import Decimal
from store.models import Product
from copy import deepcopy


class Cart:
    def __init__(self, request):
        self.session = request.session
        
        if "session_details" not in self.session:
            self.session["session_details"] = {}

        self._cart_validation()


    def _cart_validation(self):
        
        self.shopping_cart = self.session.get("session_details", {})

        all_product_keys = self.shopping_cart.keys()
        products = Product.objects.filter(id__in=all_product_keys, show=True)

        for product in products:
            self.shopping_cart[str(product.id)]["product"] = product
            self.shopping_cart[str(product.id)]["total"] = str(Decimal(product.price) * self.shopping_cart[str(product.id)]["qty"])

        copy_of_cart = self.shopping_cart.copy()

        for key, value in copy_of_cart.items():
            try:
                value["product"]
            except KeyError as exc:
                del self.shopping_cart[key]

        self.session["session_details"] = deepcopy(self.shopping_cart)

        for key in self.session["session_details"]:
            try:
                del self.session["session_details"][key]["product"]
                del self.session["session_details"][key]["total"]
            except KeyError as exc:
                continue


    def add_update_cart(self, product_id, product_qty):
        dict_to_add = {product_id: {"qty": product_qty}}
        self.session["session_details"].update(dict_to_add)
        return dict_to_add


    def delete_from_cart(self, product_id=None):
        if not product_id:
            del self.session["session_details"]
        else:
            try:
                del self.session["session_details"][product_id]
            except KeyError as exc:
                pass


    @property
    def cart_total_amount(self):
        return f"{round(sum((Decimal(value["total"]) for value in self.shopping_cart.values())), 2):.2f}"


    def __len__(self):
        return sum((value["qty"] for value in self.shopping_cart.values()))


    def __iter__(self):
        yield from self.shopping_cart.values()
 