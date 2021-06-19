from django.urls import path
from .views import home_view
from .views import SaleListView
from .views import SaleDetailView

app_name = 'Sale'

urlpatterns = [
    path('', home_view, name='home'),
    path('list/', SaleListView.as_view(), name='list'),
    path('detail/<pk>/', SaleDetailView.as_view(), name='detail'),
]

