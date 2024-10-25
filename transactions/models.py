from django.db import models
from django.core.validators import MinValueValidator


class CategoryGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    category_group = models.ForeignKey(CategoryGroup, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category_group} - {self.name}"


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'

    TRANSACTION_TYPES = [
        (INCOME, 'Prihod'),
        (EXPENSE, 'Trošak'),
    ]

    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES, default=EXPENSE)
    category = models.ForeignKey(Category, related_name='transactions', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    @property
    def type_sign(self):
        return '+' if self.transaction_type == self.INCOME else '-'

    @property
    def full_category_str(self):
        return f'{self.category.category_group.name} / {self.category.name}' if self.category else ''

    def __str__(self):
        return f'{self.type_sign}{str(self.amount)} {self.title}'
