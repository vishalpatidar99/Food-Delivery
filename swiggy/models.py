from django.db import models
from django.contrib.auth.models import User
from restaurant.models import*

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,blank=True,null=True)
    State = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.IntegerField()
    address = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.rating}"