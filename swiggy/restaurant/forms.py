from django import forms
from .models import*

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        exclude = ['user','verify']

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        exclude = ['restaurant']

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = '__all__'