from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, CategoryGroup
from .forms import TransactionForm
from django.utils import timezone
from django.db.models import Sum


def transaction_list(request):
    today = timezone.now()
    transactions = Transaction.objects.filter(
        created_at__year=today.year,
        created_at__month=today.month,
        is_deleted=False
    ).order_by('-created_at')

    total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    months = ["Januar", "Februar", "Mart", "April", "Maj", "Jun", "Jul", "Avgust", "Septembar", "Oktobar", "Novembar",
              "Decembar"]
    return render(request, 'transactions/transaction_list.html', {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'month': months[today.month - 1],
        'year': today.year
    })


def transaction_chart(request):
    labels, data, total = [], [], 0
    for cg in CategoryGroup.objects.all():
        labels.append(cg.name)
        cg_total = Transaction.objects.filter(
            category__category_group=cg, is_deleted=False
        ).aggregate(total_sum=Sum('amount'))['total_sum'] or 0
        cg_total = float(cg_total)
        data.append(cg_total)
        total += cg_total

    return render(request, 'transactions/transaction_chart.html', {
        'labels': labels,
        'data': data,
        'total': total,
    })


def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})


def transaction_edit(request, pk):
    raise NotImplemented()
    # transaction = get_object_or_404(Transaction, pk=pk)
    # if request.method == 'POST':
    #     form = TransactionForm(request.POST, instance=transaction)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('transaction_list')
    # else:
    #     form = TransactionForm(instance=transaction)
    # return render(request, 'transactions/transaction_form.html', {'form': form})


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.is_deleted = True
        transaction.save()
        return redirect('transaction_list')
    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})
