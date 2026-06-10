from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Food
from .forms import FoodForm


def food_list(request):
    foods = Food.objects.all()
    return render(request, 'foods/food_list.html', {
        'foods': foods,
    })


def food_create(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('food_list')
    else:
        form = FoodForm()
    return render(request, 'foods/food_form.html', {'form': form})


def food_edit(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('food_list')
    else:
        form = FoodForm(instance=food)
    return render(request, 'foods/food_form.html', {'form': form})


def food_delete(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        food.delete()
        return redirect('food_list')
    return render(request, 'foods/food_confirm_delete.html', {'food': food})
