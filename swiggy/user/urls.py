from django.urls import path, include
from . import views

app_name='user'
urlpatterns=[
    path('',views.UserHome.as_view(), name='userhome'),
    path('editprofile/',views.EditProfile.as_view(), name='edit-profile'),
    path('restaurant/', include('restaurant.urls', namespace='restaurant')),
    path('deliveryperson/', include('deliveryperson.urls', namespace='deliveryperson')),
]