from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class StockLog(models.Model):
    STOCK_IN = 'IN'
    STOCK_OUT = 'OUT'

    STOCK_CHOICES = [
        (STOCK_IN, 'Stock In'),
        (STOCK_OUT, 'Stock Out'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    stock_type = models.CharField(max_length=3, choices=STOCK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.stock_type} - {self.quantity}"

    # ✅ ADMIN-FRIENDLY VALIDATION
    def clean(self):
        if self.stock_type == self.STOCK_OUT:
            if self.product.stock < self.quantity:
                raise ValidationError({
                    'quantity': f'Available stock sirf {self.product.stock} hai'
                })


