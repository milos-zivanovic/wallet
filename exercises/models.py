from django.db import models


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="exercises/",
        blank=True,
        null=True,
    )
    primary_muscle = models.CharField(
        max_length=20,
        choices=[
            ("Grudi", "Grudi"),
            ("Leđa", "Leđa"),
            ("Ramena", "Ramena"),
            ("Biceps", "Biceps"),
            ("Triceps", "Triceps"),
            ("Noge", "Noge"),
            ("Stomak", "Stomak"),
            ("Kardio", "Kardio"),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
