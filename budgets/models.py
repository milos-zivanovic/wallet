from django.db import models
from django.core.validators import MinValueValidator
from categories.models import Category


class Budget(models.Model):
    category = models.ForeignKey(Category, related_name='test_budgets', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"Budget for {self.category} - {self.amount}"

    def percentage_spent(self, total_spent):
        return (total_spent / self.amount) * 100
