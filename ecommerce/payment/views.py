from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from payment.models import ShippingAddress
from payment.forms import ShippingForm
from django.contrib import messages



def checkout(request):

    try:
        shipping_address = ShippingAddress.objects.filter(user=request.user.id).order_by("-date_created")[:1].get()
    except Exception as exc:
        shipping_address = None

    shipping_address_form = ShippingForm(instance=shipping_address)

    if request.method == "POST":

        shipping_address_form = ShippingForm(request.POST, instance=shipping_address)

        if shipping_address_form.is_valid():

            if request.user and request.user.is_authenticated:
                shipping_address_form.instance.user = request.user
                shipping_address_form.save()
            
            messages.add_message(request, messages.SUCCESS, "Checkout completed")

            context = {}
            return render(request, "payment_success.html", context=context)

        else:
            messages.add_message(request, messages.ERROR, "Unable to proceed with checkout")
            # context = {}
            # return render(request, "payment_fail.html", context=context)

    form = shipping_address_form
    context = {"form": form}

    return render(request, "checkout.html", context=context)


def payment_success(request):
    return render(request, "payment_success.html")


def payment_fail(request):
    return render(request, "payment_fail.html")
