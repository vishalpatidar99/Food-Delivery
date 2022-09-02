from email.policy import default
from urllib import request
from django.db import models
from django.contrib.auth.models import User
from restaurant.models import*
from django.utils.translation import gettext_lazy as _
from deliveryperson.models import*

class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return self.dish.name

class OrderDetails(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=10)
    total_amount = models.FloatField(default=0)
    address = models.CharField(max_length=150,blank=True, null=True)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE, blank=True, null=True)
    paid_status = models.BooleanField(default=False)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    orders = models.ManyToManyField(OrderDetails)
    tax_and_charges = models.FloatField(default=0)
    delivery_charges = models.IntegerField(default=25)
    date_time = models.DateTimeField(auto_now=True)
    total_amount = models.FloatField(default=0)
    bill_to_pay = models.FloatField(default=0)

class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True)
    offer_in_percentage = models.CharField(max_length=2)
    validity = models.DateTimeField(blank=True)
    promocode = models.CharField(max_length=15)
    description = models.CharField(max_length=100, blank=True)
    terms_and_condition = models.TextField(blank=True)
