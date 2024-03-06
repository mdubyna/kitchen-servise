from django.contrib.auth.models import AbstractUser
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Cook(AbstractUser):
    years_of_cooking = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    dish_type = models.ForeignKey(
        "DishType",
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    cooks = models.ManyToManyField("Cook", related_name="dishes")

    class Meta:
        verbose_name = "dish"
        verbose_name_plural = "dishes"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.price})"
