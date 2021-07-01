from django.urls import path
from django.urls.resolvers import URLPattern
from .views import create_report_view, ReportDetailView, ReportListView

app_name = 'Report'

urlpatterns = [
    path('', ReportListView.as_view(), name='list'),
    path('details/<pk>', ReportDetailView.as_view(), name='detail'),
    path('save/', create_report_view, name='create'),
    
]