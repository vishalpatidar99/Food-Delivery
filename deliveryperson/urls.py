from django.urls import path
from . import views

app_name = 'deliverperson'
urlpatterns = [
    path('',views.DeliveryPerson.as_view(), name='deliveryperson'),
]