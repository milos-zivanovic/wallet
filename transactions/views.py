from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator
from .models import Transaction
from .forms import TransactionForm
from .filters import TransactionFilter


def transaction_overview(request):
    # Filter transactions
    show = request.GET.get('show', 'table').lower()
    today = timezone.now()
    filterset = TransactionFilter(request.GET,
                                  queryset=Transaction.objects.filter(is_deleted=False).order_by('-created_at'))

    # Calculate totals
    total_income = filterset.qs.filter(transaction_type=Transaction.INCOME).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = filterset.qs.filter(transaction_type=Transaction.EXPENSE).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    template_data = {
        'show': show,
        'filterset': filterset,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'balance_class': 'income' if balance > 0 else 'expense',
        'current_date': today.strftime('%Y-%m-%d'),
    }

    # Prepare table data
    if show == 'table':
        page_number = request.GET.get('page', 1)
        paginator = Paginator(filterset.qs, 10)
        page_obj = paginator.get_page(page_number)
        query_params = ''.join([f'&{key}={value}' for key, value in request.GET.items() if key != 'page'])

        return render(request, 'transactions/transaction_overview.html', template_data | {
            'page_obj': page_obj,
            'query_params': query_params,
        })
    # Prepare chart data
    elif show == 'chart':
        grouped_data = (
            filterset.qs
            .filter(transaction_type=Transaction.EXPENSE)
            .values('category__category_group__name')
            .annotate(total_amount=Sum('amount'))
        )
        labels = [o['category__category_group__name'] for o in grouped_data]
        data = [float(o['total_amount']) for o in grouped_data]

        raise ValueError(template_data | {
            'labels': labels,
            'data': data,
        })
        return render(request, 'transactions/transaction_overview.html', template_data | {
            'labels': labels,
            'data': data,
        })
    else:
        raise NotImplemented()


def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_overview')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})


def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_overview')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/transaction_form.html', {'form': form})


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.is_deleted = True
        transaction.save()
        return redirect('transaction_overview')
    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})
