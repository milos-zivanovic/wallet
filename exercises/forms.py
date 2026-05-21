from django import forms
from .models import Exercise


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "description", "primary_muscle", "image"]
        labels = {
            'name': 'Naziv',
            'description': 'Opis',
            'primary_muscle': 'Mišićna grupa',
            'image': 'Slika',
        }
