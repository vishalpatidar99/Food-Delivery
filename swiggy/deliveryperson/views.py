from django.shortcuts import render, redirect
from django.views import generic
# Create your views here.
class DeliveryPerson(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'deliveryperson.html')
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        return render(request, 'deliveryperson.html')
