from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    opening_time = models.TimeField(blank=True)
    closing_time = models.TimeField(blank=True)
    FSSAI_licence = models.FileField(upload_to='media',blank=True)
    GSTIN_certificate = models.FileField(upload_to='media', blank=True)
    photos = models.FileField(upload_to='media', blank=True)
    verify = models.BooleanField(default=False)
