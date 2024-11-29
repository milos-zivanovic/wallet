# Generated by Django 4.2.16 on 2024-11-28 23:52

from django.db import migrations


def fix_budget_data(apps, schema_editor):
    # Get models
    OldBudget = apps.get_model('transactions', 'Budget')
    NewBudget = apps.get_model('budgets', 'Budget')
    NewCategory = apps.get_model('categories', 'Category')

    # Drop current data
    NewBudget.objects.all().delete()

    # Copy data from old to new table
    for old_budget in OldBudget.objects.all():
        category = NewCategory.objects.filter(
            name=old_budget.category.name,
            category_group__name=old_budget.category.category_group.name
        ).first()
        if not category:
            raise ValueError('Something is wrong.')

        NewBudget.objects.create(
            category_id=category.id,
            start_date=old_budget.start_date,
            end_date=old_budget.end_date,
            amount=old_budget.amount
        )


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0002_auto_20241129_0020'),
    ]

    operations = [
        migrations.RunPython(fix_budget_data),
    ]