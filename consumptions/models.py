from django.db import models
from foods.models import Food


class Consumption(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="consumptions")
    quantity_grams = models.IntegerField()
    date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    @property
    def protein(self):
        return int(round(self.food.protein * self.quantity_grams / 100))

    @property
    def carbs(self):
        return int(round(self.food.carbs * self.quantity_grams / 100))

    @property
    def fat(self):
        return int(round(self.food.fat * self.quantity_grams / 100))

    @property
    def calories(self):
        return int(round(self.food.calories * self.quantity_grams / 100))

    def __str__(self):
        return f"{self.food.name} ({self.quantity_grams}g)"
