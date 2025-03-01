from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
   
    class Meta:
        model = ShippingAddress
        fields = ["address1", "address2", "city", "state", "zipcode", "country"]
        exclude = ["id", "user", "date_created"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

