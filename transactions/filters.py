import django_filters
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr='gte',
        label="Početni datum",
        method='filter_from_date',
        widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD'})
    )
    to_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr='lte',
        label="Krajni datum",
        method='filter_to_date',
        widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD'})
    )

    class Meta:
        model = Transaction
        fields = ['from_date', 'to_date']

    def filter_from_date(self, queryset, name, value):
        start_datetime = timezone.make_aware(datetime.combine(value, datetime.min.time()))
        return queryset.filter(**{f"{name}__gte": start_datetime})

    def filter_to_date(self, queryset, name, value):
        end_datetime = timezone.make_aware(datetime.combine(value, datetime.max.time()))
        return queryset.filter(**{f"{name}__lte": end_datetime})
