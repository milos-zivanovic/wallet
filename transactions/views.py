from datetime import datetime
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
    category_group = request.GET.get('category_group', '')
    is_fixed = request.GET.get('is_fixed', '')
    today = timezone.now()
    from_date, to_date = '2023-12-31', '2029-01-01'
    if 'from_date' in request.GET and request.GET['from_date']:
        from_date = request.GET['from_date']
    if 'to_date' in request.GET and request.GET['to_date']:
        to_date = request.GET['to_date']
    filterset = TransactionFilter(request.GET,
                                  queryset=Transaction.objects.filter(is_deleted=False).order_by('-created_at'))

    # Calculate totals
    total_income = filterset.qs.filter(transaction_type=Transaction.INCOME).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = filterset.qs.filter(transaction_type=Transaction.EXPENSE).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    template_data = {
        'show': show,
        'filterset': filterset,
        'from_date': from_date,
        'to_date': to_date,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'balance_class': 'income' if balance > 0 else 'expense',
        'category_group': category_group,
        'is_fixed': is_fixed,
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

        # Collect labels and data for categories related to provided category group
        if category_group:
            tmp_grouped_data = (
                filterset.qs
                .filter(category__category_group_id=category_group, transaction_type=Transaction.EXPENSE)
                .values('category__name')
                .annotate(total_amount=Sum('amount'))
            )
            grouped_data = {}
            for o in tmp_grouped_data:
                if o['category__name'] in grouped_data:
                    grouped_data[o['category__name']] += o['total_amount']
                else:
                    grouped_data[o['category__name']] = o['total_amount']
            labels, data = [], []
            for name, amount in grouped_data.items():
                labels.append(name)
                data.append(float(amount))

        # Collect labels and data all category groups
        else:
            tmp_grouped_data = (
                filterset.qs
                .filter(transaction_type=Transaction.EXPENSE)
                .values('category__category_group__name')
                .annotate(total_amount=Sum('amount'))
            )
            grouped_data = {}
            for o in tmp_grouped_data:
                if o['category__category_group__name'] in grouped_data:
                    grouped_data[o['category__category_group__name']] += o['total_amount']
                else:
                    grouped_data[o['category__category_group__name']] = o['total_amount']
            labels, data = [], []
            for name, amount in grouped_data.items():
                labels.append(name)
                data.append(float(amount))

        # Reorder labels and data
        combined = list(zip(labels, data))
        combined.sort(key=lambda x: x[1], reverse=True)
        labels, data = zip(*combined or [('/', 0)])

        return render(request, 'transactions/transaction_overview.html', template_data | {
            'labels': list(labels),
            'data': list(data),
            'days_diff': (datetime.strptime(to_date, "%Y-%m-%d") - datetime.strptime(from_date, "%Y-%m-%d")).days + 1,
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
