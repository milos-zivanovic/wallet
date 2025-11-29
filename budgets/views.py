from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from .models import Budget
from .forms import BudgetForm


def budget_list(request):
    # Get active budgets
    today = now().date()
    active_budgets = Budget.objects.filter(
        start_date__lte=today, end_date__gte=today
    ).order_by('category__category_group_id', 'category_id')
    total_amount = active_budgets.aggregate(total=Sum('amount'))['total'] or 0
    total_spent = sum(b.total_spent for b in active_budgets)
    active_budgets = sorted(active_budgets, key=lambda budget: budget.percentage_spent, reverse=True)

    # Get all budgets
    budgets = Budget.objects.exclude(
        start_date__lte=today, end_date__gte=today
    ).order_by('-start_date', 'category__category_group_id', 'category_id')

    return render(request, 'budgets/budget_list.html', {
        'active_budgets': active_budgets,
        'total_amount': total_amount,
        'total_spent': total_spent,
        'percentage_spent': (total_spent / total_amount) * 100,
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


def budget_edit(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'budgets/budget_form.html', {'form': form})


def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'budgets/budget_confirm_delete.html', {'budget': budget})
