from django import forms
from .models import Food


class FoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = ['name', 'protein', 'carbs', 'fat', 'calories', 'description']
        widgets = {
            'protein': forms.NumberInput(attrs={
                'inputmode': 'numeric',
                'style': 'appearance: none; -moz-appearance: textfield;',
            }),
            'carbs': forms.NumberInput(attrs={
                'inputmode': 'numeric',
                'style': 'appearance: none; -moz-appearance: textfield;',
            }),
            'fat': forms.NumberInput(attrs={
                'inputmode': 'numeric',
                'style': 'appearance: none; -moz-appearance: textfield;',
            }),
            'calories': forms.NumberInput(attrs={
                'inputmode': 'numeric',
                'style': 'appearance: none; -moz-appearance: textfield;',
            }),
        }

        labels = {
            'name': 'Naziv',
            'protein': 'Proteini',
            'carbs': 'Ugljeni hidrati',
            'fat': 'Masti',
            'calories': 'Kalorije',
            'description': 'Opis',
        }
