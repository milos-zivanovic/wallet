from django.db import models
from django.core.validators import MinValueValidator


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'

    TRANSACTION_TYPES = [
        (INCOME, 'Prihod'),
        (EXPENSE, 'Trošak'),
    ]

    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES, default=EXPENSE)
    category = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    @property
    def type_sign(self):
        return '+' if self.transaction_type == self.INCOME else '-'

    def __str__(self):
        return f'{self.type_sign}{str(self.amount)} {self.title}'
