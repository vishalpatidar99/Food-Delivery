from django.contrib import admin
from .models import *
from swiggy.models import*

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Price)
admin.site.register(Address)
admin.site.register(Rating)