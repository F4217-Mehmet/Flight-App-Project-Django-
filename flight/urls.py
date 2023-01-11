from django.urls import path
from .views import FlightView, ReservationView
from rest_framework import routers

router = routers.DefaultRouter()
router.register("flights", FlightView, basename='flights') #basename koyarsak endpoint değişse bile bunu dikkate alır
router.register("reservations", ReservationView)

urlpatterns = [
    
]
urlpatterns += router.urls