from django import forms
from .models import*

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        exclude = ['user','verify']