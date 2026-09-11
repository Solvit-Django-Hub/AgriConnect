
from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("placed", "Placed"),
        ("confirmed", "Confirmed"),
        ("delivered", "Delivered"),
    ]

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        limit_choices_to={"role": "BUYER"},
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="placed",
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        "farmers.Product",
        on_delete=models.CASCADE,
        related_name="order_items",
    )

    quantity = models.PositiveIntegerField()

    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

