from django.db.models import F, Sum, ExpressionWrapper, IntegerField
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import timedelta
from .models import Consumption
from .forms import ConsumptionForm


def consumption_list(request):
    # Prepare current week dates
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Prepare expressions for filtering
    protein_expr = ExpressionWrapper(F("food__protein") * F("quantity_grams") / 100, output_field=IntegerField())
    carbs_expr = ExpressionWrapper(F("food__carbs") * F("quantity_grams") / 100, output_field=IntegerField())
    fat_expr = ExpressionWrapper(F("food__fat") * F("quantity_grams") / 100, output_field=IntegerField())
    calories_expr = ExpressionWrapper(F("food__calories") * F("quantity_grams") / 100, output_field=IntegerField())

    summary = (
        Consumption.objects
        .filter(date__gte=start_of_week, date__lte=end_of_week)
        .values("date")
        .annotate(
            protein=Sum(protein_expr),
            carbs=Sum(carbs_expr),
            fat=Sum(fat_expr),
            calories=Sum(calories_expr),
        )
        .order_by("date")
    )

    return render(request, "consumptions/consumption_list.html", {
        'consumptions': Consumption.objects.all(),
        "start_of_week": start_of_week,
        "end_of_week": end_of_week,
        "today": today,
        "summary": summary,
    })


def consumption_create(request):
    if request.method == 'POST':
        form = ConsumptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consumption_list')
    else:
        form = ConsumptionForm()
    return render(request, 'consumptions/consumption_form.html', {'form': form})


def consumption_edit(request, pk):
    consumption = get_object_or_404(Consumption, pk=pk)
    if request.method == 'POST':
        form = ConsumptionForm(request.POST, instance=consumption)
        if form.is_valid():
            form.save()
            return redirect('consumption_list')
    else:
        form = ConsumptionForm(instance=consumption)
    return render(request, 'consumptions/consumption_form.html', {'form': form})


def consumption_delete(request, pk):
    consumption = get_object_or_404(Consumption, pk=pk)
    if request.method == 'POST':
        consumption.delete()
        return redirect('consumption_list')
    return render(request, 'consumptions/consumption_confirm_delete.html', {'consumption': consumption})
