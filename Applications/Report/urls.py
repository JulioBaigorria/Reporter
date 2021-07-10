from django.urls import path
from django.urls.resolvers import URLPattern
from .views import (create_report_view, 
                    ReportDetailView, 
                    ReportListView, 
                    render_pdf_view, 
                    UploadTemplateView,
                    csv_upload_view
)

app_name = 'Report'

urlpatterns = [
    path('', ReportListView.as_view(), name='list'),
    path('from_file/', UploadTemplateView.as_view(), name='from-file'),
    path('upload/', csv_upload_view, name='upload'),
    path('details/<pk>', ReportDetailView.as_view(), name='detail'),
    path('save/', create_report_view, name='create'),
    path('<pk>/pdf/', render_pdf_view, name='pdf'),
    
]