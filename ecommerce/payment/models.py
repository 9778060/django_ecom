from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class ShippingAddress(models.Model):

    id = models.AutoField(primary_key=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250, null=True, blank=True)
    zipcode = models.CharField(max_length=50)
    country = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "shipping addresses"

    def __str__(self):
        return f"{self.address1}, {self.address2}, {self.city}, {self.state}, {self.zipcode}, {self.country}"


class Order(models.Model):

    id = models.AutoField(primary_key=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250, null=True, blank=True)
    zipcode = models.CharField(max_length=50)
    country = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "orders"

    def __str__(self):
        return f"{self.address1}, {self.address2}, {self.city}, {self.state}, {self.zipcode}, {self.country}"