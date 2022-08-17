from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from restaurant.models import*
from .forms import*
from.models import *
# Create your views here.

class UserHome(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            items = Restaurant.objects.all()
            price = Price.objects.all()
            return render(request, 'userhome.html', {'items':items})#, 'price':price})
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
        print(request.user)
        print(request.user.username)
        if first_name !='':
            User.objects.filter(username=request.user.username).update(first_name=first_name)
        if last_name!='':
            User.objects.filter(username=request.user.username).update(last_name=last_name)
        if email!='':
            User.objects.filter(username=request.user.username).update(email=email)
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

class RestaurantDetails(generic.View):
    def get(self, request,  *args, **kwargs):
        if request.user.is_authenticated:
            pk = kwargs['pk']
            res = Dish.objects.filter(restaurant__id=pk)
            return render(request,'dishesh.html',{'res':res})
        else:
            return redirect('login')

    def post(self, request,  *args, **kwargs):
        pk = kwargs['pk']
        res = Dish.objects.filter(restaurant__id=pk)
        dish = request.POST['dish']
        d=Dish.objects.get(id=dish)
        print(d)
        CartItems.objects.create(user=request.user,dish=d)
        return render(request,'dishesh.html',{'res':res})
        
class Cart(generic.View):
    def get(self, request, *args, **kwargs):
        quantity = 1
        if request.user.is_authenticated:
            items = CartItems.objects.filter(user=request.user)
            total = 0
            for i in items:
                total += int(i.dish.price_set.all().first().price_of_dish)
            return render(request, 'cart.html', {'res':items,'quantity':quantity,'total':total})
        else:
            return redirect('login')

    # def post(self, request, *args, **kwargs):
    #     # import pdb;pdb.set_trace()
    #     quantity = 1
    #     plus = request.POST['plus']
    #     # minus = request.POST['minus']
    #     if plus != '':
    #         quantity+=1
    #     # elif minus != '':
    #     #     quantity-=1
    #     else:
    #         quantity = 1

    #     items = CartItems.objects.all()
    #     return render(request, 'cart.html', {'res':items,'quantity':quantity})