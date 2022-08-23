from django.db import models
from django.contrib.auth.models import User
from restaurant.models import*

class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return self.dish.name

# class OrderDetails(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     dishesh = models.ManyToManyField(Dish)
#     date_time = models.DateTimeField(auto_now=True)

