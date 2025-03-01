from django.urls import path
from . import views


urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    # path("payment_success/", views.payment_success, name="payment_success"),
    # path("payment_fail/", views.payment_fail, name="payment_fail"),
]
