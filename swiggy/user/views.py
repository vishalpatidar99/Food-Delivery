from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from restaurant.models import*
from .forms import*
from.models import *
from swiggy.models import*
from django.contrib import messages
# Create your views here.

class UserHome(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            filter_by = request.GET.get('filter_by')
            if filter_by:
                if filter_by=='veg' or filter_by=='non':
                    filtered_items = Dish.objects.filter(menu_type = filter_by)
                else:
                    filtered_items = Dish.objects.filter(dish_type = filter_by)

                final_res =[i.restaurant for i in filtered_items]
                final_res = set(final_res)
                items = Restaurant.objects.filter(verify=True).order_by('-total_rating')

                return render(request,'userhome.html',{'final_res':final_res,'cart_items':cart_items})
            else:
                cart_items = CartItems.objects.filter(user=request.user,paid=False)
                items = Restaurant.objects.filter(verify=True).order_by('-total_rating')
                return render(request, 'userhome.html', {'items':items,'cart_items':cart_items})
        else:
            return redirect('login')
    
    def post(self, request, *args, **kwargs):
        search_query = request.POST['query']
        searched_items = Dish.objects.filter(name__contains=search_query)
        searched_restaurants = Restaurant.objects.filter(restaurant_name__contains=search_query)

        final_res =[i.restaurant for i in searched_items]
        res = [i for i in searched_restaurants]
        final_res.extend(res)
        final_res = set(final_res)
        items = Restaurant.objects.filter(verify=True).oredr_by('-total_rating')
        cart_items = CartItems.objects.filter(user=request.user,paid=False)
        return render(request, 'userhome.html', {'final_res':final_res,'items':items,'cart_items':cart_items})

class EditProfile(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # user = User.objects.get(id=request.user.id)
            return render(request, 'editprofile.html')#,{'user':user})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        User.objects.filter(username=request.user.username).update(first_name=first_name,last_name=last_name,email=email)
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
            price_filter = request.GET.get('price_filter')
            pk = request.GET.get('pk')
            if price_filter:
                if price_filter=='low':
                    res = Dish.objects.filter(restaurant__id=pk).order_by('price__price_of_dish')
                    # import pdb;pdb.set_trace()
                else:
                    res = Dish.objects.filter(restaurant__id=pk).order_by('-price__price_of_dish')
            else:
                res = Dish.objects.filter(restaurant__id=pk)

            cart_items = CartItems.objects.filter(user=request.user,paid=False)
            return render(request,'restaurantmenu.html',{'res':res,'pk':pk,'cart_items':cart_items,'conf':cart_items[0]})
        else:
            return redirect('login')

    def post(self, request,  *args, **kwargs):
        pk = request.GET.get('pk')
        confirmation = request.POST.get('confirmation')
        res = Dish.objects.filter(restaurant__id=pk)
        dish_id = request.POST['dish']
        dish=Dish.objects.get(id=dish_id)
        res_2 = []
        restau = CartItems.objects.filter(user=request.user).first()
        
        if confirmation == 'Yes':
            CartItems.objects.all().delete()
            CartItems.objects.create(user=request.user, dish=dish,price=dish.price_set.all().first().price_of_dish)
            cart_items = CartItems.objects.filter(user=request.user,paid=False)
            return render(request,'restaurantmenu.html',{'res':res,'cart_items':cart_items,'conf':cart_items[0]})

        else:
            if restau is not None:
                if dish.restaurant.id == restau.dish.restaurant.id:
                    for i in CartItems.objects.filter(user=request.user).values_list('dish_id'):
                        for j in i:
                            res_2.append(j)
                    if int(dish_id) not in res_2 or restau.user.id != request.user.id:
                        CartItems.objects.create(user=request.user,dish=dish,price=dish.price_set.all().first().price_of_dish)
                        messages.success(request,'Item added successfully')
                    else:
                        messages.success(request,'Item is already availabel in cart')
                        # return redirect(reverse('user:cart'))

                    cart_items = CartItems.objects.filter(user=request.user,paid=False)
                    return render(request,'restaurantmenu.html',{'res':res,'cart_items':cart_items,'conf':cart_items[0]})
                else:
                    cart_items = CartItems.objects.filter(user=request.user,paid=False)
                    return render(request,'restaurantmenu.html',{'res':res,'cart_items':cart_items,'conf':cart_items[0]})

            else:
                CartItems.objects.create(user=request.user,dish=dish,price=dish.price_set.all().first().price_of_dish)
                messages.success(request,'Item added successfully')
                cart_items = CartItems.objects.filter(user=request.user,paid=False)
                return render(request,'restaurantmenu.html',{'res':res,'cart_items':cart_items,'conf':cart_items[0]})

        
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
                
            user_address = Address.objects.filter(user=request.user)
            items = CartItems.objects.filter(user=request.user,paid=False)
            total_price = 0
            for i in items:
                total_price += i.price

            if len(items)>0:
                tax = total_price/10
                to_pay = total_price + 25 + tax
            else:
                to_pay = 0
                tax = 0

            return render(request, 'cart.html', {'res':items,'user_address':user_address,'total':total_price,'to_pay':to_pay,'tax':tax})
        else:
            return redirect('login')
        
    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     return render(request, 'cart.html')#, {'res':items,'user_address':user_address,'total':total_price,'to_pay':to_pay})

    # def post(self, request, *args, **kwargs):

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
        q = request.POST['q']
        if form.is_valid():
            print(request.POST)
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Address Saved Successfully')
            if q:
                return redirect(reverse('user:cart'))
            else:
                return redirect(reverse('user:address'))
        else:
            messages.error(request, 'form is invalid')
            return render(request,'address.html')

class RatingView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request,'rating.html')
    
# class PlaceOrder(generic.View):
#     def get(self, request, *args, **kwargs):
#         items = CartItems.objects.filter(user=request.user,paid=False)
#         total_price = 0

#         for i in items:
#             total_price += i.price

#         to_pay = total_price + 50
#         user_address = Address.objects.filter(user=request.user)
#         return render(request, 'placeorder.html',{'res':items,'total':total_price,'user_address':user_address,'to_pay':to_pay})
    
#     def post(self,request,*args,**kwargs):
#         print(request.POST)
#         items = CartItems.objects.filter(user=request.user,paid=False)
#         total_price = 0
#         for i in items:
#             total_price += i.price

#         to_pay = total_price + 50
#         user_address = Address.objects.filter(user=request.user)
#         return render(request, 'placeorder.html',{'res':items,'total':total_price,'user_address':user_address,'to_pay':to_pay})
