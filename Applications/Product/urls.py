from django.urls import path
from .views import ProductListView, ProductCreateView

app_name = 'Product'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('create/', ProductCreateView.as_view(), name='create'),
]