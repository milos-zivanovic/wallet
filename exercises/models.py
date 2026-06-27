from django.db import models


class MuscleGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_name = models.CharField(max_length=100, blank=True, null=True)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT, related_name="exercises", null=True,
                                     blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["muscle_group", "name"]

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image_name:
            return f"images/exercises/{self.image_name}"
        return None
