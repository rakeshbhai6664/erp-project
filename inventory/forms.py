from django import forms
from .models import Product

class StockEntryForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label="Select Product"
    )

    STOCK_CHOICES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )

    stock_type = forms.ChoiceField(choices=STOCK_CHOICES)
    quantity = forms.IntegerField(min_value=1)
