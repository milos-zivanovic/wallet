from django.db import models
from exercises.models import Exercise


class Training(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.name} ({self.date})"


class TrainingItem(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="items")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="training_items")
    order = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["exercise__primary_muscle", "exercise__name"]

    def __str__(self):
        return f"{self.training} - {self.exercise}"


class TrainingSet(models.Model):
    training_item = models.ForeignKey(TrainingItem, on_delete=models.CASCADE, related_name="sets")
    set_number = models.PositiveIntegerField()
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )
    reps = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["set_number"]
        unique_together = ("training_item", "set_number")

    def __str__(self):
        return (
            f"{self.training_item.exercise} - "
            f"Set {self.set_number}: "
            f"{self.weight}kg x {self.reps}"
        )
