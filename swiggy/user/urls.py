from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='user'
urlpatterns=[
    path('',views.UserHome.as_view(), name='userhome'),
    path('editprofile/',views.EditProfile.as_view(), name='edit-profile'),
    path('restaurant/', include('restaurant.urls', namespace='restaurant')),
    path('deliveryperson/', include('deliveryperson.urls', namespace='deliveryperson')),
    path('dishesh/<int:pk>/', views.RestaurantDetails.as_view(),name='dishesh'),
    path('cart/', views.Cart.as_view(),name='cart'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
