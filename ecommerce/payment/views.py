from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from payment.models import ShippingAddress, Order, OrderItem
from payment.forms import ShippingForm
from django.contrib import messages
from cart.cart import Cart
from django.db import transaction
from decimal import Decimal
from django.http import JsonResponse



def checkout(request):

    cart = Cart(request)
    if not len(cart):
        return redirect("dashboard")

    try:
        shipping_address = ShippingAddress.objects.filter(user=request.user.id).order_by("-date_created")[:1].get()
    except Exception as exc:
        shipping_address = None

    shipping_address_form = ShippingForm(instance=shipping_address)

    if request.method == "POST":

        shipping_address_form = ShippingForm(request.POST, instance=shipping_address)

        if shipping_address_form.is_valid():

            if request.user and request.user.is_authenticated and shipping_address_form.changed_data:
                shipping_address_form.instance.user = request.user
                shipping_address_form.save()

            form = shipping_address_form

            if request.user and request.user.is_authenticated:
                full_name = f"{request.user.first_name} {request.user.last_name}"
                email = request.user.email
            else:
                full_name = request.POST.get("full_name")
                email = request.POST.get("email")

            context = {"form": form, "full_name": full_name, "email": email}
            return render(request, "complete_order.html", context=context)

        else:
            messages.add_message(request, messages.ERROR, "Unable to proceed with checkout")

    form = shipping_address_form
    context = {"form": form}

    return render(request, "checkout.html", context=context)


def complete_order(request):
    cart = Cart(request)
    if not len(cart):
        return redirect("dashboard")
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")

        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")
        country = request.POST.get("country")

        shipping_address = f"{address1}\n{address2}\n{city}, {state}\n, {zipcode}, {country}"

        amount_to_pay = cart.cart_total_amount

        user = request.user if request.user.is_authenticated else None

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    full_name=full_name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=amount_to_pay,
                    user=user
                )

                for item in cart:
                    order_item = OrderItem.objects.create(
                        quantity=item.get("qty", 1),
                        price=Decimal(item.get("total", 0)),
                        order=order,
                        product=item.get("product")
                    )                    

        except Exception as exc:
            print(f"Error: {exc}")

        return JsonResponse({"success": True})

    return redirect("dashboard")
    


def payment_success(request):

    existing_cart = Cart(request)
    existing_cart.delete_from_cart()    

    return render(request, "payment_success.html")


def payment_fail(request):
    return render(request, "payment_fail.html")
