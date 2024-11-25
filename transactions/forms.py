from django import forms
from django_select2.forms import Select2Widget
from .models import Budget, Category, Transaction


class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.select_related('category_group').all(),
        widget=Select2Widget,
        label="Kategorija"
    )

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'title', 'amount', 'category', 'description', 'is_fixed']
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
            'description': 'Opis transakcije',
            'is_fixed': 'Fiksno',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customizing the category choices to show in 'Category Group / Category' format
        category_choices = []
        categories = Category.objects.select_related('category_group').all().order_by('category_group_id', 'id')

        for category in categories:
            choice_label = f"{category.category_group.name} / {category.name}"
            category_choices.append((category.id, choice_label))

        # Set the choices for the category field
        self.fields['category'].choices = category_choices


class BudgetForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.select_related('category_group').all(),
        widget=Select2Widget,
        label="Kategorija"
    )

    class Meta:
        model = Budget
        fields = ['category', 'start_date', 'end_date', 'amount']
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
        }
