from http.client import HTTPResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from restaurant.models import*
from .forms import*
from.models import *
from swiggy.models import*
# Create your views here.

class UserHome(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            items = Restaurant.objects.all()
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

class RestaurantMenu(generic.View):
    def get(self, request,  *args, **kwargs):
        if request.user.is_authenticated:
            pk = kwargs['pk']
            res = Dish.objects.filter(restaurant__id=pk)
            return render(request,'restaurantmenu.html',{'res':res,'restau':res[0]})
        else:
            return redirect('login')

    def post(self, request,  *args, **kwargs):
        pk = kwargs['pk']
        res = Dish.objects.filter(restaurant__id=pk)
        dish_id = request.POST['dish']
        dish=Dish.objects.get(id=dish_id)
        res_2 = []
        restau = CartItems.objects.filter(user=request.user).first()

        if restau is not None:
            if dish.restaurant.id == restau.dish.restaurant.id:
                for i in CartItems.objects.filter(user=request.user).values_list('dish_id'):
                    for j in i:
                        res_2.append(j)
                if int(dish_id) not in res_2 or restau.user.id != request.user.id:
                    CartItems.objects.create(user=request.user,dish=dish,price=dish.price_set.all().first().price_of_dish)
                else:
                    return redirect(reverse('user:cart'))
                return render(request,'restaurantmenu.html',{'res':res})
            else:
                return render(request,'restaurantmenu.html',{'res':res})
        else:
            CartItems.objects.create(user=request.user,dish=dish,price=dish.price_set.all().first().price_of_dish)
            return render(request,'restaurantmenu.html',{'res':res})

        
class Cart(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            status = request.GET.get('status')
            item_id = request.GET.get('id')
            q = request.GET.get('q')
                
            if status == 'plus':
                item = CartItems.objects.get(id=int(item_id))
                price = item.dish.price_set.all().first().price_of_dish
                quantity = item.quantity
                quantity+=1
                price = int(price)*quantity
                CartItems.objects.filter(id=int(item_id)).update(quantity=quantity,price=price)
            elif status == 'minus':
                item = CartItems.objects.get(id=int(item_id))
                price = item.dish.price_set.all().first().price_of_dish
                quantity = item.quantity
                quantity-=1
                price = int(price)*quantity
                CartItems.objects.filter(id=int(item_id)).update(quantity=quantity,price=price)

            if (status == 'del'or q == '1'):
                CartItems.objects.get(id=int(item_id)).delete()
                
            items = CartItems.objects.filter(user=request.user,paid=False)
            total_price = 0
            for i in items:
                total_price += i.price

            return render(request, 'cart.html', {'res':items,'total':total_price})
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

class AddAddress(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = AddressForm()
            return render(request,'address.html',{'form':form})
        else:
            return redirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()

            return redirect(reverse('user:userhome'))
        else:
            return render(request,'address.html')
    
class PlaceOrder(generic.View):
    def get(self, request, *args, **kwargs):

        items = CartItems.objects.filter(user=request.user,paid=False)
        total_price = 0
        for i in items:
            total_price += i.price
        
        user_address = Address.objects.filter(user=request.user)
        return render(request, 'placeorder.html',{'res':items,'total':total_price,'user_address':user_address})