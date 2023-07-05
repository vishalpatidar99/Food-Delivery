from django import forms
from .models import*
from django.contrib.auth.forms import AuthenticationForm
from food_delivery.models import*

# class RestaurantForm(forms.ModelForm):
#     class Meta:
#         model = Restaurant
#         exclude = ('verify','user')
#         widgets = {'opening_time':forms.TimeInput(),'closing_time':forms.TimeInput(),'photo':forms.ClearableFileInput(attrs={'multipul':True})}

# class RestaurantLoginForm(forms.ModelForm):
#     class Meta:
#         model = Restaurant
#         fields = ['email','password']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user','restaurant']