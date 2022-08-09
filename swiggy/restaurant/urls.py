from django.urls import path
from . import views

app_name = 'restaurant'
urlpatterns=[
    path('',views.RestaurantRegistration.as_view(), name='register'),
    # path('login/',views.RestaurantLogin.as_view(), name='login'),
    path('home/', views.RestaurantHome.as_view(), name='home'),
    path('dish/', views.Dish.as_view(), name='dish'),
    ]