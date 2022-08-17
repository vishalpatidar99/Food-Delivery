from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    opening_time = models.TimeField(blank=True)
    closing_time = models.TimeField(blank=True)
    FSSAI_licence = models.FileField(upload_to='restaurant/fssai/',blank=True)
    GSTIN_certificate = models.FileField(upload_to='restaurant/gstin/', blank=True)
    photos = models.FileField(upload_to='restaurant/photo/', blank=True)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return self.restaurant_name

class Dish(models.Model):
    class MENU_TYPE_CHOICES(models.TextChoices):
        VEG = 'veg', _('Veg') 
        NONVEG = 'non', _('Nonveg') 

    class DISH_TYPE_CHOICES(models.TextChoices):
        STARTER = 'starter', _('Starter')
        BREAKFAST = 'break', _('Break Fast')
        MAINCOURSE = 'main', _('Main Course')
        FASTFOOD = 'Fast', _('Fast Food')
        DESSERT = 'Dessert', _('Dessert')

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dish_type = models.CharField(max_length=8, choices=DISH_TYPE_CHOICES.choices)
    menu_type = models.CharField(max_length=3, choices=MENU_TYPE_CHOICES.choices)
    photo = models.FileField(upload_to='dish')
    description = models.TextField()

    def __str__(self):
        return self.name

class Price(models.Model):
    class SIZE_CHOICES(models.TextChoices):
        FULL = 'f', _('Full')
        HALF = 'h', _('Half')
        NONE = 'n', _('None')

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES.choices, blank=True, null=True)
    price_of_dish = models.CharField(max_length=4)
 
    def __str__(self):
        return self.dish.name