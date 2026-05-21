from django.db import models


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_name = models.CharField(max_length=100, blank=True, null=True)
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
        ordering = ["primary_muscle", "name"]

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image_name:
            return f"images/exercises/{self.image_name}"
        return None
