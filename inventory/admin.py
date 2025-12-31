from django.contrib import admin
from .models import Product, StockLog

admin.site.register(Product)
admin.site.register(StockLog)
