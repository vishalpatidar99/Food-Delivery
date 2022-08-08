from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import*
from django.contrib.auth import authenticate, login, logout
# from.models import *
# Create your views here.

class UserHome(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'userhome.html')
        else:
            return redirect('login')

class EditProfile(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'editprofile.html')
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        if first_name!='':
            User.objects.filter(username=request.user).update(first_name=first_name)
        if last_name!='':
            User.objects.filter(username=request.user).update(last_name=last_name)
        if email!='':
            User.objects.filter(username=request.user).update(email=email)
        return redirect(reverse('user:userhome'))

# class RestaurantLogin(generic.View):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             form = RestaurantLoginForm()
#             return render(request, 'restaurantlogin.html',{'form':form})
#         else:
#             return redirect('login')

#     def post(self, request, *args, **kwargs):
#         email = request.POST['email']
#         password = request.POST['password']
#         user = Restaurant.objects.filter(email=email,password=password)
#         print(user)
#         if user is not None:
#             print(user)
#             # login(request,user)
#             return redirect(reverse('user:restaurant-register'))
#         else:
#             return redirect(reverse('user:restaurant-login'))