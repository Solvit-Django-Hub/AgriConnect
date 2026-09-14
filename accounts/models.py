from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    FARMER = "FARMER"
    BUYER = "BUYER"

    ROLE_CHOICES = [
        (FARMER, "Farmer"),
        (BUYER, "Buyer"),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True,
    )

    def __str__(self):
        return self.username