from django import forms
from django_select2.forms import Select2Widget
from .models import Category, Transaction


class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.select_related('category_group').all())

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'title', 'amount', 'category', 'description']
        widgets = {
            'category': Select2Widget,
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
