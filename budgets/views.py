from django.shortcuts import render, redirect
from transactions.models import Budget
from .forms import BudgetForm


def budget_list(request):
    budgets = Budget.objects.all().order_by('category__category_group_id', 'category_id')
    return render(request, 'budgets/budget_list.html', {'budgets': budgets})


def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'budgets/budget_form.html', {'form': form})
