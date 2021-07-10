from django.urls import path
# from .views import home_view
from .views import HomeListView, SaleListView, SaleDetailView

app_name = 'Sale'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('list/', SaleListView.as_view(), name='list'),
    path('detail/<pk>/', SaleDetailView.as_view(), name='detail'),
]

