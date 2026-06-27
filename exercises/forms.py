from django import forms
from .models import Exercise


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "description", "muscle_group", "image_name"]
        labels = {
            'name': 'Naziv',
            'description': 'Opis',
            'muscle_group': 'Mišićna grupa',
            'image_name': 'Ime slike',
        }
