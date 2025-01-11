from decimal import Decimal
from store.models import Product
from copy import deepcopy


class Cart:
    def __init__(self, request):
        self.session = request.session
        
        if "session_details" not in self.session:
            self.session["session_details"] = {}

        self.session_details = self.session.get("session_details")
        self._cart_validation()


    def _cart_validation(self):
        all_product_keys = self.session_details.keys()
        products = Product.objects.filter(id__in=all_product_keys, show=True)

        for product in products:
            self.session_details[str(product.id)]["product"] = product
            self.session_details[str(product.id)]["total"] = str(Decimal(product.price) * self.session_details[str(product.id)]["qty"])

        copy_of_cart = self.session_details.copy()

        for key, value in copy_of_cart.items():
            try:
                value["product"]
            except KeyError as exc:
                del self.session_details[key]

        for key in self.session_details:
            try:
                del self.session_details[key]["product"]
            except KeyError as exc:
                continue

        self.session["session_details"] = self.session_details


    def _cart_enhancement(self):
        all_product_keys = self.session_details.keys()
        products = Product.objects.filter(id__in=all_product_keys, show=True)
        ammended_cart = deepcopy(self.session_details)

        for product in products:
            ammended_cart[str(product.id)]["product"] = product
            ammended_cart[str(product.id)]["total"] = str(Decimal(product.price) * ammended_cart[str(product.id)]["qty"])

        copy_of_cart = ammended_cart.copy()

        for key, value in copy_of_cart.items():
            try:
                value["product"]
            except KeyError as exc:
                del ammended_cart[key]

        return ammended_cart


    def add_update_cart(self, product_id, product_qty):
        dict_to_add = {product_id: {"qty": product_qty}}
        self.session_details.update(dict_to_add)
        return dict_to_add


    def delete_from_cart(self, product_id):
        if product_id in self.session_details:
            del self.session_details[product_id]


    @property
    def cart_total_amount(self):
        return f"{round(sum((Decimal(value["total"]) for value in self.session_details.values())), 2):.2f}"


    def __len__(self):
        return sum((value["qty"] for value in self.session_details.values()))


    def __iter__(self):
        yield from self._cart_enhancement().values()
 