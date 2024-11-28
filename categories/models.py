from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class CategoryGroup(models.Model):
    name = models.CharField(max_length=100)
    name_with_html = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name

    def current_budget(self):
        budgets = []
        for category in self.categories.all():
            category_budget = category.current_budget()
            if category_budget:
                budgets.append(category_budget)
        return budgets


class Category(models.Model):
    name = models.CharField(max_length=100)
    category_group = models.ForeignKey(CategoryGroup, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        cg = self.category_group
        return f'{cg.name_with_html if cg.name_with_html else cg.name} / {self.name}'

    def current_budget(self):
        today = now().date()
        budgets = self.budgets.filter(start_date__lte=today, end_date__gte=today)
        if budgets.count() > 1:
            raise ValidationError("Vise budzeta za ovu kategoriju.")
        return budgets.first()
