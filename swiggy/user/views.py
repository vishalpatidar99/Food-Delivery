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
            cart_items = CartItems.objects.filter(user=request.user,paid=False)
            
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
        items = Restaurant.objects.filter(verify=True).order_by('-total_rating')
        cart_items = CartItems.objects.filter(user=request.user,paid=False)
        return render(request, 'userhome.html', {'final_res':final_res,'items':items,'cart_items':cart_items})

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
        User.objects.filter(username=request.user.username).update(first_name=first_name,last_name=last_name,email=email)
        messages.success(request, "Profile updated successfully")
        return redirect(reverse('user:userhome'))

class RestaurantMenu(generic.View):
    def get(self, request,  *args, **kwargs):
        if request.user.is_authenticated:
            price_filter = request.GET.get('price_filter')
            pk = request.GET.get('pk')
            follow = request.GET.get('follow')
            if follow == 'yes':
                Restaurant.objects.get(id=pk).followers.add(request.user)
                follow = Restaurant.objects.filter(id=pk,followers=request.user)
            elif follow == 'no':
                Restaurant.objects.get(id=pk).followers.remove(request.user)
                follow = Restaurant.objects.filter(id=pk,followers=request.user)
            else:
                follow = 'nothing'

            if price_filter:
                if price_filter=='low':
                    res = Dish.objects.filter(restaurant__id=pk).order_by('price__price_of_dish')
                else:
                    res = Dish.objects.filter(restaurant__id=pk).order_by('-price__price_of_dish')
            else:
                res = Dish.objects.filter(restaurant__id=pk)

            follow = Restaurant.objects.filter(id=pk,followers=request.user)
            cart_items = CartItems.objects.filter(user=request.user,paid=False)
            return render(request,'restaurantmenu.html',{'res':res,'pk':pk,'cart_items':cart_items,'follow':follow})
        else:
            return redirect('login')

    def post(self, request,  *args, **kwargs):
        pk = request.GET.get('pk')
        confirmation = request.POST.get('confirmation')

        res = Dish.objects.filter(restaurant__id=pk)
        dish_id = request.POST['dish']
        dish=Dish.objects.get(id=dish_id)
        res_2 = []
        cart_items = CartItems.objects.filter(user=request.user)

        if confirmation == 'Yes':
            CartItems.objects.all().delete()
            CartItems.objects.create(user=request.user, dish=dish,price=dish.price_set.all().first().price_of_dish)
            return render(request,'restaurantmenu.html',{'res':res,'cart_items':cart_items})

        if cart_items.first() is not None:
            if dish.restaurant.id == cart_items.first().dish.restaurant.id:
                for i in CartItems.objects.filter(user=request.user, paid=False).values_list('dish_id'):
                    for j in i:
                        res_2.append(j)
                if int(dish_id) not in res_2 or cart_items.first().user.id != request.user.id:
                    CartItems.objects.create(user=request.user,dish=dish,price=dish.price_set.all().first().price_of_dish)
                    messages.success(request,'Item added successfully')
                else:
                    messages.success(request,'Item is already availabel in cart')

                return render(request,'restaurantmenu.html',{'res':res,'cart_items':cart_items})
            else:
                return render(request,'restaurantmenu.html',{'res':res,'cart_items':cart_items})
        else:
            CartItems.objects.create(user=request.user,dish=dish,price=dish.price_set.all().first().price_of_dish)
            messages.success(request,'Item added successfully')
            return render(request,'restaurantmenu.html',{'res':res,'cart_items':cart_items})

        
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
        
    def post(self, request, *args, **kwargs):
        address_id = request.POST['address']
        payment_method = request.POST['payment']
        total_amount = request.POST['sub']
        confirmation = request.POST['conf']
        if confirmation == 'Yes':
            address = Address.objects.get(user=request.user,id=address_id)
            items = CartItems.objects.filter(user=request.user, paid=False)
            
            for i in items:
                OrderDetails.objects.create(user=request.user,dish=i.dish,restaurant=i.dish.restaurant, payment_method=payment_method,address=address.address,quantity=i.quantity,price=i.price)
            
            order = Order.objects.create(user=request.user,restaurant=items[0].dish.restaurant,bill_to_pay=total_amount)
            items.delete()
            orders = OrderDetails.objects.filter(user=request.user, paid_status=False)
            total_price = 0
            for o in orders:
                total_price += o.price
                order.orders.add(o)
            orders.update(paid_status=True)
            tax_and_charges = total_price/10
            order.tax_and_charges = tax_and_charges
            order.total_amount = total_price
            order.save()
            return redirect(reverse('user:rating'))

        else:
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
                messages.success(request, "Address added successfully")
                return redirect(reverse('user:address'))
        else:
            messages.error(request, 'form is invalid')
            return render(request,'address.html')

class RatingView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request,'rating.html')
    
class OrderDetailsView(generic.View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orderdetails.html',{'orders':orders})

class MyOffersView(generic.View):
    def get(self, request, *args, **kwargs):
        offers = Offer.objects.all()
        return render(request, 'myoffers.html', {'offers':offers})