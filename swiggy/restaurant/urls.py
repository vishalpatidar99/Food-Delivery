from django.urls import path
from . import views
import restaurant

app_name = 'restaurant'
urlpatterns=[
    path('',views.RestaurantRegistration.as_view(), name='register'),
    path('login/',views.RestaurantRegistration.as_view(), name='login'),
    ]