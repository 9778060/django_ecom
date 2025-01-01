from decimal import Decimal
from store.models import Product
from copy import deepcopy


class Cart:
    def __init__(self, request):
        self.session = request.session
        
        if "session_details" not in self.session:
            self.session["session_details"] = {}

        self.session_details = self.session.get("session_details")
       

    def add_to_cart(self, product_id, product_qty):
        dict_to_add = {str(product_id): {"qty": product_qty}}
        self.session_details.update(dict_to_add)
        self.session["session_details"] = self.session_details
        return dict_to_add


    @property
    def cart_total_amount(self):
        return f"{round(sum((Decimal(value["total"]) for value in self.session_details.values())), 2):.2f}"


    def __len__(self):
        return sum((value["qty"] for value in self.session_details.values()))


    def __iter__(self):
        all_product_keys = self.session_details.keys()
        products = Product.objects.filter(id__in=all_product_keys, show=True)
        ammended_cart = self.session_details.copy()

        for product in products:
            ammended_cart[str(product.id)]["product"] = product
            ammended_cart[str(product.id)]["price"] = Decimal(product.price)
            ammended_cart[str(product.id)]["total"] = str(ammended_cart[str(product.id)]["price"] * ammended_cart[str(product.id)]["qty"])

        copy_of_cart = ammended_cart.copy()

        for key, value in copy_of_cart.items():
            try:
                value["product"]
            except KeyError as exc:
                del ammended_cart[key]

        self.session_details = deepcopy(ammended_cart)
        
        for key in self.session_details:
            try:
                del self.session_details[key]["product"]
                del self.session_details[key]["price"]
            except KeyError as exc:
                continue

        self.session["session_details"] = self.session_details


        yield from ammended_cart.values()
 