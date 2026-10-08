from django.contrib import messages
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .forms import TrainingForm, TrainingAddSetForm
from .models import Training, TrainingItem, TrainingSet


class TrainingListView(ListView):
    model = Training
    template_name = "trainings/training_list.html"
    context_object_name = "trainings"


class TrainingDetailView(DetailView):
    model = Training
    template_name = "trainings/training_detail.html"
    context_object_name = "training"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_set_form"] = TrainingAddSetForm(training=self.object)
        return context


class TrainingCreateView(CreateView):
    model = Training
    form_class = TrainingForm
    template_name = "trainings/training_form.html"
    success_url = reverse_lazy("training_list")

    def get_initial(self):
        return {"date": timezone.now().date()}


class TrainingUpdateView(UpdateView):
    model = Training
    form_class = TrainingForm
    template_name = "trainings/training_form.html"
    success_url = reverse_lazy("training_list")


class TrainingDeleteView(DeleteView):
    model = Training
    template_name = "trainings/training_confirm_delete.html"
    success_url = reverse_lazy("training_list")


class TrainingAddSetView(View):

    def post(self, request, pk):
        training = get_object_or_404(Training, pk=pk)
        form = TrainingAddSetForm(request.POST, training=training)
        if not form.is_valid():
            messages.error(request, "Molimo Vas ispravite greske ispod.")
            return redirect("training_detail", pk=training.pk)

        exercise = form.cleaned_data["exercise"]
        weight = form.cleaned_data["weight"]
        reps = form.cleaned_data["reps"]

        training_item, _ = TrainingItem.objects.get_or_create(
            training=training,
            exercise=exercise,
            defaults={
                "order": training.items.count() + 1,
            }
        )

        next_set_number = 1
        last_set = training_item.sets.order_by(
            "-set_number"
        ).first()
        if last_set:
            next_set_number = last_set.set_number + 1

        TrainingSet.objects.create(
            training_item=training_item,
            set_number=next_set_number,
            weight=weight,
            reps=reps,
        )

        messages.success(request, "Kreiran set.")
        return redirect("training_detail",  pk=training.pk)
