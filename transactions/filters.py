import django_filters
from django import forms
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from categories.models import CategoryGroup
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr='gte',
        label="Početni datum",
        method='filter_from_date',
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'YYYY-MM-DD',
            'readonly': 'readonly',
            'autocomplete': 'off'
        })
    )
    to_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr='lte',
        label="Krajni datum",
        method='filter_to_date',
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'YYYY-MM-DD',
            'readonly': 'readonly',
            'autocomplete': 'off'
        })
    )
    category_group = django_filters.ModelChoiceFilter(
        field_name='category__category_group',
        queryset=CategoryGroup.objects.all(),
        label='Kategorija'
    )
    is_agency_related = django_filters.BooleanFilter(
        label='Got. račun',
        widget=forms.Select(
            choices=[
                ('', '---------'),
                ('true', 'Da'),
                ('false', 'Ne')
            ]
        )
    )
    is_fixed = django_filters.BooleanFilter(
        label='Fiksno',
        widget=forms.Select(
            choices=[
                ('', '---------'),
                ('true', 'Da'),
                ('false', 'Ne')
            ]
        )
    )
    title = django_filters.CharFilter(
        method='filter_title_or_description',
        label='Pretraga'
    )

    class Meta:
        model = Transaction
        fields = ['from_date', 'to_date', 'category_group', 'is_agency_related', 'is_fixed', 'title']

    def filter_from_date(self, queryset, name, value):
        start_datetime = timezone.make_aware(datetime.combine(value, datetime.min.time()))
        return queryset.filter(**{f"{name}__gte": start_datetime})

    def filter_to_date(self, queryset, name, value):
        end_datetime = timezone.make_aware(datetime.combine(value, datetime.max.time()))
        return queryset.filter(**{f"{name}__lte": end_datetime})

    def filter_title_or_description(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
