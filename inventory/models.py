from django.db import models

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
    quantity = models.IntegerField()
    stock_type = models.CharField(max_length=3, choices=STOCK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.stock_type} - {self.quantity}"

    # ✅ SAVE METHOD CLASS KE ANDAR
    def save(self, *args, **kwargs):
        if not self.pk:  # sirf new entry par
            if self.stock_type == self.STOCK_IN:
                self.product.stock += self.quantity
            elif self.stock_type == self.STOCK_OUT:
                self.product.stock -= self.quantity

            self.product.save()

        super().save(*args, **kwargs)
