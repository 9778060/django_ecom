
class Cart:
    def __init__(self, request):
        self.session = request.session
        
        if "session_details" not in self.session:
            self.session["session_details"] = {}

        self.session_details = self.session.get("session_details")
       

    def add_to_cart(self, product, product_qty):
        dict_to_add = {str(product.id): {"title": product.title, "url": product.get_absolute_url, "image_url": product.image.url, "price": float(product.price), "qty": product_qty}}
        self.session_details.update(dict_to_add)
        self.session.update(self.session_details)
        return dict_to_add
    

    @property
    def cart_total(self):
        return f"{sum((value["price"] * value["qty"] for value in self.session_details.values())):.2f}"
