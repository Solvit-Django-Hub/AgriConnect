from django.conf import settings
from django.db import models


class Farmer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="farmer_profile",
        limit_choices_to={"role": "FARMER"},
    )

    def __str__(self):
        return f"{self.user} (Farmer)"


class Product(models.Model):
    name = models.CharField(max_length=150)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        limit_choices_to={"role": "FARMER"},
    )

    category = models.ForeignKey(
        "orders.Category",
        on_delete=models.CASCADE,
        related_name="products",
    )

    def __str__(self):
        return self.name