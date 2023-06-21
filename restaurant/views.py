from django.shortcuts import render, redirect
from .models import*
from django.views import generic
from django.urls import reverse
from .forms import*
from django.contrib import messages

# Create your views here.
class RestaurantRegistration(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = RestaurantForm()
            return render(request, 'restaurantregister.html', {'form':form})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(reverse('user:restaurant:home'))
        else:
            return redirect('login')

# class RestaurantLogin(generic.View):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return render(request, 'restaurantlogin.html')
#         else:
#             return redirect('login')

#     def post(self, request, *args, **kwargs):
#         email = request.POST['email']
#         password = request.POST['password']
#         print(request.user.password)
#         if email==request.user.email and password==request.user.password:
#             print('yes')
#         else:
#             print('No')
#         return render(request, 'restaurantlogin.html')

class RestaurantHome(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            res = Restaurant.objects.filter(user=request.user).first()
            return render(request, 'restauranthome.html',{'res':res})
        else:
            return redirect('login')

class Dish(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = DishForm()
            return render(request,'dish.html', {'form':form})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.restaurant = request.user.restaurant_set.get()
            form.save()
            messages.success(request, "Dish added successfully...")
            return redirect(reverse('user:restaurant:dishprice'))
        else:
            messages.error(request, "Invalid form")
            return render(request, 'dish.html')

class Price(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = PriceForm()
            return render(request,'price.html', {'form':form})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        form = PriceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Price added successfully...")
            return redirect(reverse('user:restaurant:dishprice'))
        else:
            messages.error(request, "Invalid form")
            return render(request, 'price.html')