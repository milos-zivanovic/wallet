from django.urls import path
from . import views

app_name = 'sales_receipts'


urlpatterns = [
    path('qr-scan/', views.qr_scan, name='qr_scan'),
    path('qr-upload/', views.qr_upload, name='qr_upload'),
]
