from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Sum
from .models import Product
from .forms import StockEntryForm
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import StockLog
from django.contrib.auth.decorators import login_required
import subprocess
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
import os
from django.http import HttpResponse
from openpyxl import Workbook
from .models import StockLog
from django.contrib.auth.decorators import login_required




# Existing view (as it is)
def stock_entry(request):
    return HttpResponse("Stock Entry Page")


def daily_stock_report(request):
    today = now().date()

    total_in = StockLog.objects.filter(
        stock_type='IN',
        created_at__date=today
    ).aggregate(total=Sum('quantity'))['total'] or 0

    total_out = StockLog.objects.filter(
        stock_type='OUT',
        created_at__date=today
    ).aggregate(total=Sum('quantity'))['total'] or 0

    # ✅ CALCULATION BACKEND ME
    net_movement = total_in - total_out

    context = {
        'today': today,
        'total_in': total_in,
        'total_out': total_out,
        'net_movement': net_movement,
    }

    return render(request, 'daily_stock_report.html', context)

def current_stock_summary(request):
    products = Product.objects.all().order_by('name')

    context = {
        'products': products
    }

    return render(request, 'current_stock_summary.html', context)


def stock_entry_form(request):
    message = None

    if request.method == 'POST':
        form = StockEntryForm(request.POST)

        if form.is_valid():
            product = form.cleaned_data['product']
            stock_type = form.cleaned_data['stock_type']
            qty = form.cleaned_data['quantity']

            try:
                with transaction.atomic():
                    product = Product.objects.select_for_update().get(id=product.id)

                    if stock_type == 'OUT' and product.stock < qty:
                        raise ValidationError("Stock kam hai")

                    if stock_type == 'IN':
                        product.stock += qty
                    else:
                        product.stock -= qty

                    product.save()

                    StockLog.objects.create(
                        product=product,
                        quantity=qty,
                        stock_type=stock_type
                    )

                message = "Stock updated successfully"
                form = StockEntryForm()  # reset form

            except ValidationError as e:
                message = str(e)

    else:
        form = StockEntryForm()

    return render(request, 'stock_entry_form.html', {
        'form': form,
        'message': message
    })
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
def is_admin(user):
    return user.is_superuser  # simple & safe for backup


def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def backup_database(request):
    db_name = "erp_db"
    db_user = "postgres"
    db_password = "515154"   # same as your postgres password

    backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

    try:
        env = os.environ.copy()
        env["PGPASSWORD"] = db_password   # ⭐ KEY FIX

        process = subprocess.Popen(
            [
                r"C:\Program Files\PostgreSQL\18\bin\pg_dump.exe",
                "-U", db_user,
                db_name
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )

        output, error = process.communicate()

        if process.returncode != 0:
            return HttpResponse(f"Backup failed:<br><pre>{error.decode()}</pre>")

        response = HttpResponse(output, content_type="application/sql")
        response["Content-Disposition"] = f'attachment; filename="{backup_file}"'
        return response

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
@login_required
def today_stock(request):
    today = now().date()

    total_in = StockLog.objects.filter(
        stock_type='IN',
        created_at__date=today
    ).aggregate(total=Sum('quantity'))['total'] or 0

    total_out = StockLog.objects.filter(
        stock_type='OUT',
        created_at__date=today
    ).aggregate(total=Sum('quantity'))['total'] or 0

    return render(request, 'inventory/today_stock.html', {
        'total_in': total_in,
        'total_out': total_out
    })
def export_stock_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stock"

    ws.append(["ID", "Stock Type", "Quantity", "Date"])

    from .models import StockLog
    for log in StockLog.objects.all():
        ws.append([
            log.id,
            log.stock_type,
            log.quantity,
            log.created_at.strftime("%Y-%m-%d")
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=stock.xlsx'
    wb.save(response)

    return response