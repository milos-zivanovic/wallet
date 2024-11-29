# Generated by Django 4.2.16 on 2024-11-29 00:27

from django.db import migrations


def transfer_category_data(apps, schema_editor):
    # Get models
    NewCategory = apps.get_model('categories', 'Category')
    Transaction = apps.get_model('transactions', 'Transaction')

    for transaction in Transaction.objects.all():
        category = NewCategory.objects.filter(
            name=transaction.category.name,
            category_group__name=transaction.category.category_group.name
        ).first()
        if not category:
            raise ValueError('Something is wrong.')

        transaction.new_category_id = category.id
        transaction.save()


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0017_transaction_new_category'),
    ]

    operations = [
        migrations.RunPython(transfer_category_data),
    ]