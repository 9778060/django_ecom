from django.contrib import admin
from .models import ShippingAddress


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("address1", "address2", "city", "state", "zipcode", "country", "user", "date_created")
    list_display_links = ("address1", )
    readonly_fields = ("id", "date_created")
    fields = ("id", "address1", "address2", "city", "state", "zipcode", "country", "user", "date_created")
    search_fields = ("address1", "address2", "city", "state", "zipcode", "country")
    list_filter = ("address1", "address2", "city", "state", "zipcode", "country", "user", "date_created")
