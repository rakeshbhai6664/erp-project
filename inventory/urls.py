from django.urls import path
from . import views
from .views import stock_entry, daily_stock_report
from .views import current_stock_summary
from .views import stock_entry_form
from .views import dashboard
from django.contrib.auth import views as auth_views
from .views import backup_database





urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('stock/', views.stock_entry, name='stock_entry'),
    path('daily-stock-report/', daily_stock_report, name='daily_stock_report'),
    path('current-stock/', current_stock_summary, name='current_stock'),
    path('stock-entry-form/', stock_entry_form, name='stock_entry_form'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('backup-db/', backup_database, name='backup_db'),




]

