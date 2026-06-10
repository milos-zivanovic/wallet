from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=255, unique=True)
    calories = models.DecimalField(max_digits=8, decimal_places=2)
    protein = models.DecimalField(max_digits=8, decimal_places=2)
    carbs = models.DecimalField(max_digits=8, decimal_places=2)
    fat = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Consumption(models.Model):
    food = models.ForeignKey(Food, on_delete=models.PROTECT, related_name="consumptions")
    quantity_grams = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    @property
    def calories(self):
        return self.food.calories * self.quantity_grams / 100

    @property
    def protein(self):
        return self.food.protein * self.quantity_grams / 100

    @property
    def carbs(self):
        return self.food.carbs * self.quantity_grams / 100

    @property
    def fat(self):
        return self.food.fat * self.quantity_grams / 100

    def __str__(self):
        return f"{self.food.name} ({self.quantity_grams}g)"
