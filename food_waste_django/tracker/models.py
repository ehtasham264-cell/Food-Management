from django.db import models
from django.utils import timezone


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    qty = models.FloatField()
    unit = models.CharField(max_length=20, default="kg")
    cost = models.FloatField(default=0, help_text="Cost per unit in rupees")
    expiry = models.DateField()

    class Meta:
        ordering = ["expiry"]

    def __str__(self):
        return f"{self.name} ({self.qty} {self.unit})"


class WasteEntry(models.Model):
    date = models.DateField(default=timezone.localdate)
    name = models.CharField(max_length=100)
    qty = models.FloatField()
    cost = models.FloatField(default=0, help_text="Total cost wasted in rupees")
    reason = models.CharField(max_length=50)

    class Meta:
        ordering = ["date", "id"]
        verbose_name_plural = "waste entries"

    def __str__(self):
        return f"{self.name} - {self.reason}"


class SurplusItem(models.Model):
    dish = models.CharField(max_length=100)
    portions = models.PositiveIntegerField()
    action = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.dish} ({self.portions})"
