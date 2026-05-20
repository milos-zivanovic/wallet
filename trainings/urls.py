from django.urls import path
from . import views


urlpatterns = [
    path("", views.TrainingListView.as_view(), name="training_list"),
    path("create/", views.TrainingCreateView.as_view(), name="training_create"),
    path("<int:pk>/", views.TrainingDetailView.as_view(), name="training_detail"),
    path("<int:pk>/update/", views.TrainingUpdateView.as_view(), name="training_update"),
    path("<int:pk>/delete/", views.TrainingDeleteView.as_view(), name="training_delete"),
    path("<int:pk>/add-set/", views.TrainingAddSetView.as_view(), name="training_add_set"),
]