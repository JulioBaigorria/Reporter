from django.urls import path
from .views import my_profile_view

app_name = 'Profile'

urlpatterns = [
    path('', my_profile_view, name='my'),
]