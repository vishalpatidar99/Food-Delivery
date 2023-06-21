from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class DeliveryPerson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = PhoneNumberField()
    vehicle_number = models.CharField(max_length=100, blank=True)
    driving_licence_number = models.CharField(max_length=15, blank=True)
    id_proof = models.FileField(upload_to='media', blank=True)
    vehicle_document_photo = models.FileField(upload_to='media', blank=True)
    driving_licence_photo = models.FileField(upload_to='media', blank=True)
    verify = models.BooleanField(default=False)