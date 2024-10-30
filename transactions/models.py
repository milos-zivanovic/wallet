from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


class CategoryGroup(models.Model):
    name = models.CharField(max_length=100)
    name_with_html = models.CharField(max_length=150, null=True, blank=True)

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
    category = models.ForeignKey(Category, related_name='transactions', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    @property
    def type_sign(self):
        return '+' if self.transaction_type == self.INCOME else '-'

    @property
    def full_category_str(self):
        if not self.category:
            return ''
        cg = self.category.category_group
        return f'{cg.name_with_html if cg.name_with_html else cg.name} / {self.category.name}'

    def __str__(self):
        return f'{self.type_sign}{str(self.amount)} {self.title}'
