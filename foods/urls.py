from django.urls import path
from . import views


urlpatterns = [
    path('', views.food_list, name='food_list'),
    path('create/', views.food_create, name='food_create'),
    path('edit/<int:pk>/', views.food_edit, name='food_edit'),
    path('delete/<int:pk>/', views.food_delete, name='food_delete'),
]
