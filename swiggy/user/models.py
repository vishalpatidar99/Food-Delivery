from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100, blank=True)
    owner_name = models.CharField(max_length=100, blank=True)
    owner_phone = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=35)
    password = models.CharField(max_length=25)
    opening_time = models.TimeField(blank=True)
    closing_time = models.TimeField(blank=True)
    photo = models.FileField(upload_to='media', blank=True)
    FSSAI_licence = models.FileField(upload_to='media', blank=True)
    GSTIN_certificate = models.FileField(upload_to='media',blank=True)
    verify = models.BooleanField(default=False)