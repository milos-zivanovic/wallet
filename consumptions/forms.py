from django import forms
from django_select2.forms import Select2Widget
from foods.models import Food
from .models import Consumption


class ConsumptionForm(forms.ModelForm):
    food = forms.ModelChoiceField(
        queryset=Food.objects.all(),
        widget=Select2Widget,
        label="Namirnica"
    )

    class Meta:
        model = Consumption
        fields = ['food', 'quantity_grams', 'date']
        widgets = {
            'quantity_grams': forms.NumberInput(attrs={
                'inputmode': 'numeric',
                'style': 'appearance: none; -moz-appearance: textfield;',
            }),
            'date': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control datepicker',
                'placeholder': 'YYYY-MM-DD',
            }),
        }

        labels = {
            'quantity_grams': 'Količina (g)',
            'date': 'Darum',
        }
