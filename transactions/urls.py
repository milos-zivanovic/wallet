from django.urls import path
from . import views


urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('chart/', views.transaction_chart, name='transaction_chart'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('edit/<int:pk>/', views.transaction_edit, name='transaction_edit'),
    path('delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
]
