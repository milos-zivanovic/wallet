from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'

    TRANSACTION_TYPES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES, default=EXPENSE)
    category = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        type_sign = '+' if self.transaction_type == self.INCOME else '-'
        return f'{type_sign}{str(self.amount)} {self.title}'
