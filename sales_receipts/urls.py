from django.urls import path
from . import views

app_name = 'sales_receipts'


urlpatterns = [
    path('qr-url/', views.qr_url_form, name='qr_url_form'),
    path('qr-url/upload/', views.qr_url_upload, name='qr_url_upload'),
]
