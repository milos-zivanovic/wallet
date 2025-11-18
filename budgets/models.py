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
        return (self.total_spent / self.amount) * 100

    @property
    def total_spent(self):
        total_spent = Transaction.objects.filter(
            category=self.category,
            transaction_type=Transaction.EXPENSE,
            created_at__date__gte=self.start_date,
            created_at__date__lte=self.end_date,
            is_deleted=False
        ).aggregate(amount=Sum('amount'))['amount']
        return Decimal(total_spent or 0)
