from django.db import models


class Seller(models.Model):
    number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Receipt(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="receipts")
    image = models.ImageField(upload_to="receipts/")
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Receipt from {self.seller.name} - {self.total} RSD"


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} x{self.quantity} - {self.price} RSD"
