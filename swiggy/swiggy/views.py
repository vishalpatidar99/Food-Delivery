from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import*
from django.urls import reverse
from django.contrib import messages

class Home(generic.TemplateView):
    template_name = 'index.html'

class About(generic.TemplateView):
    template_name = 'about.html'
    
class Service(generic.TemplateView):
    template_name = 'service.html'
    
class Offer(generic.TemplateView):
    template_name = 'offer.html'
    
class UserRegistration(generic.View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'register.html',{'form':form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = UserCreationForm()
            return render(request, 'register.html',{'form':form})

class UserLogin(generic.View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request,'login.html',{'form':form})

    def post(self, request, *args, **kwargs):
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('user:userhome'))
        else:
            form = AuthenticationForm() 
            messages.error(request, 'Invalid Details, Try again')
            return render(request,'login.html',{'form':form})

class Logout(generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')