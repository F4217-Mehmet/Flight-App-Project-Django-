from django.shortcuts import render
from rest_framework import viewsets
from .serializers import FlightSerializer
from .models import Flight
from rest_framework.permissions import IsAdminUser

# Create your views here.
class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminUser,)  #tuple olduğu belli olsun diye sonuna virgül koyduk 