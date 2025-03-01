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
        return f"Shipping address: {self.address1}, {self.address2}, {self.city}, {self.state}, {self.zipcode}, {self.country}"


class Order(models.Model):

    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=250) 
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=1_000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "orders"

    def __str__(self):
        return f"Order #{self.id}: {self.full_name}, {self.email}, {self.amount_paid}"


class OrderItem(models.Model):

    id = models.AutoField(primary_key=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "order items"

    def __str__(self):
        return f"Order item #{self.id}: {self.order}, {self.product}, {self.price}, {self.quantity}"
