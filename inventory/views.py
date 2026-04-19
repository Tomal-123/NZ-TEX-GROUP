from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
import csv
import io
from taskmanager.models import InventoryItem


@login_required
def inventory_management(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'import_csv':
            csv_file = request.FILES.get('csv_file')
            if csv_file:
                try:
                    decoded_file = csv_file.read().decode('utf-8')
                    reader = csv.reader(io.StringIO(decoded_file))
                    next(reader)
                    imported_count = 0
                    
                    for row in reader:
                        if len(row) >= 3:
                            department = row[0].strip().lower().replace(' ', '_').replace("'", '').replace('-', '_')
                            category = row[1].strip().lower().replace(' ', '_').replace('-', '_')
                            quantity = int(row[2]) if row[2].strip().isdigit() else 0
                            
                            valid_departments = ['computer_accessories', 'printer_and_scanner', 'others_it_product']
                            if department not in valid_departments:
                                department = 'computer_accessories'
                            
                            InventoryItem.objects.update_or_create(
                                department=department,
                                category=category,
                                defaults={'quantity': quantity}
                            )
                            imported_count += 1
                    messages.success(request, f'{imported_count} items imported successfully!')
                except Exception as e:
                    messages.error(request, f'Error importing CSV: {str(e)}')
        
        elif action == 'update_quantity':
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 0))
            item = InventoryItem.objects.get(id=item_id)
            item.quantity = quantity
            item.save()
            messages.success(request, 'Quantity updated successfully!')
        
        return redirect('inventory_management')
    
    items = InventoryItem.objects.all().order_by('department', 'category')
    total_quantity = sum(item.quantity for item in items)
    
    computer_accessories = items.filter(department='computer_accessories')
    printer_and_scanner = items.filter(department='printer_and_scanner')
    others_it_product = items.filter(department='others_it_product')
    
    return render(request, 'inventory/index.html', {
        'items': items,
        'total_quantity': total_quantity,
        'computer_accessories': computer_accessories,
        'printer_and_scanner': printer_and_scanner,
        'others_it_product': others_it_product,
    })


def get_inventory_data(request):
    items = InventoryItem.objects.all()
    data = []
    for item in items:
        data.append({
            'id': item.id,
            'department': item.department,
            'department_display': item.get_department_display(),
            'category': item.category,
            'category_display': item.get_category_display(),
            'quantity': item.quantity,
        })
    return JsonResponse(data, safe=False)


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Department', 'Category', 'Quantity'])
    
    for item in InventoryItem.objects.all().order_by('department', 'category'):
        writer.writerow([item.get_department_display(), item.get_category_display(), item.quantity])
    
    return response
