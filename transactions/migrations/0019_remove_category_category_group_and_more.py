# Generated by Django 4.2.16 on 2024-11-29 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0018_auto_20241129_0127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_group',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
        migrations.DeleteModel(
            name='Budget',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='CategoryGroup',
        ),
    ]
