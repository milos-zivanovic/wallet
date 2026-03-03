from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .managers import ActiveCategoryGroupManager, ActiveCategoryManager


class CategoryGroup(models.Model):
    name = models.CharField(max_length=100)

    objects = ActiveCategoryGroupManager()
    all_objects = models.Manager()

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

    # Date range when category is active (static / one time only)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Date range when category is active each year (dynamic / repeatedly)
    start_month = models.PositiveSmallIntegerField(null=True, blank=True)
    start_day = models.PositiveSmallIntegerField(null=True, blank=True)
    end_month = models.PositiveSmallIntegerField(null=True, blank=True)
    end_day = models.PositiveSmallIntegerField(null=True, blank=True)

    objects = ActiveCategoryManager()
    all_objects = models.Manager()

    def __str__(self):
        cg = self.category_group
        return f'{cg.name} / {self.name}'

    def current_budget(self):
        today = now().date()
        budgets = self.budgets.filter(start_date__lte=today, end_date__gte=today)
        if budgets.count() > 1:
            raise ValidationError("Vise budzeta za ovu kategoriju.")
        return budgets.first()
