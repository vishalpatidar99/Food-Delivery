from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import*
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['email','password']
