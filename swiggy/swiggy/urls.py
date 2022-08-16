"""swiggy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='swiggy'
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.Home.as_view(),name='home'),
    path("about/",views.About.as_view(),name='about'),
    path("service/",views.Service.as_view(),name='service'),
    path("offer/",views.Offer.as_view(),name='offer'),
    path("register/",views.UserRegistration.as_view(),name='register'),
    path("login/",views.UserLogin.as_view(),name='login'),
    path("logout/",views.Logout.as_view(),name='logout'),
    path('user/', include('user.urls', namespace='user')),
] + static(settings.MEDIA_URL, 
             document_root=settings.MEDIA_ROOT)
