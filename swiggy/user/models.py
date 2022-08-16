from django.db import models
from django.contrib.auth.models import User
from restaurant.models import*

class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    