from django.urls import path
from . import views


urlpatterns = [
    path("exercises/", views.ExerciseListView.as_view(), name="exercise_list"),
    path("exercises/create/", views.ExerciseCreateView.as_view(), name="exercise_create"),
    path("exercises/<int:pk>/update/", views.ExerciseUpdateView.as_view(), name="exercise_update"),
    path("exercises/<int:pk>/delete/", views.ExerciseDeleteView.as_view(), name="exercise_delete"),
]