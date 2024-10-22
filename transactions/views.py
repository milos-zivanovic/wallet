from django.shortcuts import render, redirect, get_object_or_404
# from .models import Transaction
from .forms import TransactionForm
# from django.db.models import Sum


# def transaction_list(request):
#     transactions = Transaction.objects.all().order_by('-date')
#     total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
#     total_expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
#     balance = total_income - total_expense
#
#     return render(request, 'transactions/transaction_list.html', {
#         'transactions': transactions,
#         'total_income': total_income,
#         'total_expense': total_expense,
#         'balance': balance,
#     })


def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})


# def transaction_edit(request, pk):
#     transaction = get_object_or_404(Transaction, pk=pk)
#     if request.method == 'POST':
#         form = TransactionForm(request.POST, instance=transaction)
#         if form.is_valid():
#             form.save()
#             return redirect('transaction_list')
#     else:
#         form = TransactionForm(instance=transaction)
#     return render(request, 'transactions/transaction_form.html', {'form': form})
#
#
# def transaction_delete(request, pk):
#     transaction = get_object_or_404(Transaction, pk=pk)
#     if request.method == 'POST':
#         transaction.delete()
#         return redirect('transaction_list')
#     return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})
