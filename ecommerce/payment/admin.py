from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("address1", "address2", "city", "state", "zipcode", "country", "user", "date_created")
    list_display_links = ("address1", )
    readonly_fields = ("id", "date_created")
    fields = ("id", "address1", "address2", "city", "state", "zipcode", "country", "user", "date_created")
    search_fields = ("address1", "address2", "city", "state", "zipcode", "country")
    list_filter = ("address1", "address2", "city", "state", "zipcode", "country", "user", "date_created")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "shipping_address", "amount_paid", "user", "date_ordered", "status")
    list_display_links = ("full_name", )
    readonly_fields = ("id", "date_ordered")
    fields = ("id", "full_name", "email", "shipping_address", "amount_paid", "user", "date_ordered", "status")
    search_fields = ("full_name", "email", "shipping_address")
    list_filter = ("full_name", "email", "shipping_address", "amount_paid", "user", "date_ordered", "status")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "price", "order")
    list_display_links = ("product", )
    readonly_fields = ("id", )
    fields = ("id", "product", "quantity", "price", "order")
    search_fields = ("product", "order")
    list_filter = ("product", "quantity", "price", "order")
