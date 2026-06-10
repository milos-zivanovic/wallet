from django.urls import path
from . import views


urlpatterns = [
    path('', views.consumption_list, name='consumption_list'),
    path('create/', views.consumption_create, name='consumption_create'),
    path('edit/<int:pk>/', views.consumption_edit, name='consumption_edit'),
    path('delete/<int:pk>/', views.consumption_delete, name='consumption_delete'),
]
