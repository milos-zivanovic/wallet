from django import forms
from exercises.models import Exercise
from .models import Training


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ["muscle_groups", "date", "notes"]
        widgets = {
            "muscle_groups": forms.CheckboxSelectMultiple(),
            'date': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control datepicker',
                'placeholder': 'YYYY-MM-DD',
            }),
        }
        labels = {
            'muscle_groups': 'Mišićne grupe',
            'date': 'Datum',
            'notes': 'Opis',
        }


class TrainingAddSetForm(forms.Form):
    exercise = forms.ModelChoiceField(
        queryset=Exercise.objects.none(),
        label='Vežba'
    )
    weight = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        required=True,
        label='Težina'
    )
    reps = forms.IntegerField(label='Broj ponavljanja')

    def __init__(self, *args, training=None, **kwargs):
        super().__init__(*args, **kwargs)

        if training:
            self.fields["exercise"].queryset = Exercise.objects.filter(
                muscle_group__in=training.muscle_groups.all()
            ).order_by("muscle_group__name", "name")

        self.fields["exercise"].label_from_instance = (
            lambda obj: f"({obj.muscle_group}) {obj.name}"
        )
