# Generated by Django 4.2.16 on 2024-11-29 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0019_remove_category_category_group_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='new_category',
            new_name='category',
        ),
    ]
