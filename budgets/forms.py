from django import forms
from django_select2.forms import Select2Widget
from categories.models import Category
from .models import Budget


class BudgetForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.select_related('category_group').all(),
        widget=Select2Widget,
        label="Kategorija"
    )

    class Meta:
        model = Budget
        fields = ['category', 'start_date', 'end_date', 'amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'inputmode': 'numeric',
                'style': 'appearance: none; -moz-appearance: textfield;',
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control datepicker',
                'placeholder': 'YYYY-MM-DD',
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control datepicker',
                'placeholder': 'YYYY-MM-DD',
            })
        }
        labels = {
            'amount': 'Iznos',
            'start_date': 'Početni Datum',
            'end_date': 'Krajnji Datum',
            'description': 'Opis',
        }
