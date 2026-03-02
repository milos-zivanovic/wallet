from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum
from decimal import Decimal
from categories.models import Category
from transactions.models import Transaction


class Budget(models.Model):
    category = models.ForeignKey(Category, related_name='budgets', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Budget for {self.category} - {self.amount}"

    @property
    def percentage_spent(self):
        # Return 0 if amount is invalid or budget is in the future
        if not self.amount or self.amount <= 0 or self.start_date > date.today():
            return 0

        return (self.total_spent / self.amount) * 100

    @property
    def total_spent(self):
        # Return 0 if the budget hasn't started or dates/category are invalid
        if not self.start_date or not self.end_date or not self.category:
            return Decimal(0)

        if self.start_date > date.today():
            return Decimal(0)

        total_spent = Transaction.objects.filter(
            category=self.category,
            transaction_type=Transaction.EXPENSE,
            created_at__date__gte=self.start_date,
            created_at__date__lte=self.end_date,
            is_deleted=False
        ).aggregate(amount=Sum('amount'))['amount']

        return Decimal(total_spent or 0)
