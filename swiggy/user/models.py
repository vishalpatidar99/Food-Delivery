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
    class PAYMENT_METHOD_CHOICES(models.TextChoices):
        UPI = 'upi', _('UPI')
        DEBIT = 'deb', _('Debit Card')
        CREDIT = 'ced', _('Credit Card')
        COD = 'cod', _('Cash on Delivery')
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dishesh = models.ManyToManyField(Dish)
    date_time = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=3,choices=PAYMENT_METHOD_CHOICES.choices)
    total_amount = models.FloatField()
    address = models.CharField(max_length=150,blank=True, null=True)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE, blank=True, null=True)

