from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'title', 'amount', 'category', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'inputmode': 'numeric',
                'style': 'appearance: none; -moz-appearance: textfield;',
            })
        }
        labels = {
            'transaction_type': 'Tip',
            'title': 'Naslov',
            'amount': 'Iznos',
            'category': 'Kategorija',
            'description': 'Opis transakcije',
        }
