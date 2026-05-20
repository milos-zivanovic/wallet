from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .forms import ExerciseForm
from .models import Exercise


class ExerciseListView(ListView):
    model = Exercise
    template_name = "exercises/exercise_list.html"
    context_object_name = "exercises"


class ExerciseCreateView(CreateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "exercises/exercise_form.html"
    success_url = reverse_lazy("exercise_list")


class ExerciseUpdateView(UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "exercises/exercise_form.html"
    success_url = reverse_lazy("exercise_list")


class ExerciseDeleteView(DeleteView):
    model = Exercise
    template_name = "exercises/exercise_confirm_delete.html"
    success_url = reverse_lazy("exercise_list")
