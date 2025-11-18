from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import Budget
from .forms import BudgetForm


def budget_list(request):
    # Get active budgets
    today = now().date()
    active_budgets = Budget.objects.filter(
        start_date__lte=today, end_date__gte=today
    ).order_by('category__category_group_id', 'category_id')
    active_budgets = sorted(active_budgets, key=lambda budget: budget.percentage_spent, reverse=True)

    # Get all budgets
    budgets = Budget.objects.all().order_by('start_date', 'category__category_group_id', 'category_id')

    return render(request, 'budgets/budget_list.html', {
        'active_budgets': active_budgets,
        'budgets': budgets
    })


def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'budgets/budget_form.html', {'form': form})
