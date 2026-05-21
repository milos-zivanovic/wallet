from django import forms
from exercises.models import Exercise
from .models import Training


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ["name", "date", "notes"]
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control datepicker',
                'placeholder': 'YYYY-MM-DD',
            }),
        }
        labels = {
            'name': 'Naziv',
            'date': 'Datum',
            'notes': 'Opis',
        }


class TrainingAddSetForm(forms.Form):
    exercise = forms.ModelChoiceField(
        queryset=Exercise.objects.all(),
        label='Vežba'
    )
    weight = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        required=True,
        label='Težina'
    )
    reps = forms.IntegerField(label='Broj ponavljanja')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["exercise"].label_from_instance = (
            lambda obj: f"({obj.primary_muscle}) {obj.name}"
        )