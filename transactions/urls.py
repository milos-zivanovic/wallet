from django.urls import path
from . import views


urlpatterns = [
    path('', views.transaction_overview, name='transaction_overview'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('edit/<int:pk>/', views.transaction_edit, name='transaction_edit'),
    path('delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
]
