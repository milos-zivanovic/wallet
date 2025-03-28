# Generated by Django 4.2.16 on 2024-10-25 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_transaction_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='transactions.categorygroup')),
            ],
        ),
    ]
