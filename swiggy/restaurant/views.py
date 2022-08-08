from django.shortcuts import render, redirect
from .models import*
from django.views import generic
from django.urls import reverse

# Create your views here.
class RestaurantRegistration(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'restaurantregister.html')
        else:
            return redirect(reverse('restaurant:restaurant-login'))

    def post(self, request, *args, **kwargs):
        restaurant_name=request.POST['restaurant_name']
        phone = request.POST['phone']
        opening_time=request.POST['opening_time']
        closing_time=request.POST['closing_time']
        FSSAI_licence=request.FILES.get('fssai_licence')
        GSTIN_certificate=request.FILES.get('gstin_certificate')
        photos = request.FILES.getlist('photos')
        Restaurant.objects.create(user=request.user, restaurant_name=restaurant_name, phone=phone, opening_time=opening_time, closing_time=closing_time)
        return redirect(reverse('restaurant:restaurant-register'))