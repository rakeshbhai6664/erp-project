from django.urls import path
from . import views

urlpatterns = [
    path('stock/', views.stock_entry, name='stock_entry'),
]
