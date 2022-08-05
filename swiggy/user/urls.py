from django.urls import path
from . import views

app_name='user'
urlpatterns=[
    path('',views.UserHome.as_view(), name='userhome'),
    path('editprofile/',views.EditProfile.as_view(), name='edit-profile'),
    path('restaurantregister/',views.RestaurantRegistration.as_view(), name='restaurant-register'),
    path('restaurantlogin/',views.RestaurantRegistration.as_view(), name='restaurant-login'),
]