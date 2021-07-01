from django.shortcuts import render
from .models import Customer
from rest_framework import permissions
from rest_framework import viewsets

from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer