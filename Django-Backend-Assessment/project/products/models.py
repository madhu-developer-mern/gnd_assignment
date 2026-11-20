from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=60)
    brand = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percentage = models.PositiveSmallIntegerField(default=0)
    stock_quantity = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
