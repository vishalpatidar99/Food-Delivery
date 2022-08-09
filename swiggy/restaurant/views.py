from django.shortcuts import render, redirect
from .models import*
from django.views import generic
from django.urls import reverse
from .forms import*

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
        res = Restaurant.objects.filter(user=request.user).first()
        return render(request, 'restauranthome.html',{'res':res})

class Dish(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request,'dish.html')