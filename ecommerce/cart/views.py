from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse


def cart_summary(request):
    return render(request, "cart_summary.html")


def cart_add(request):
    response = JsonResponse({"empty": None})

    if request.POST.get("action") == "post":
        existing_cart = Cart(request)
        product_id = str(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))

        # if selected_product := get_object_or_404(Product, id=product_id, show=True):
        #     dict_to_add = existing_cart.add_to_cart(selected_product, product_qty)
        #     response = JsonResponse(dict_to_add)

        dict_to_add = existing_cart.add_update_cart(product_id, product_qty)
        response = JsonResponse(dict_to_add)

    return response


def cart_delete(request):
    response = JsonResponse({"empty": None})

    if request.POST.get("action") == "post":
        existing_cart = Cart(request)
        product_id = str(request.POST.get("product_id"))

        existing_cart.delete_from_cart(product_id)

    return response


def cart_update(request):
    response = JsonResponse({"empty": None})

    if request.POST.get("action") == "post":
        existing_cart = Cart(request)
        product_id = str(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))

        dict_to_update = existing_cart.add_update_cart(product_id, product_qty)
        response = JsonResponse(dict_to_update)

    return response
