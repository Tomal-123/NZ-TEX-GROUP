from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from taskmanager.models import InventoryNew, InventoryAuditLog, Department, AssetCategory
from taskmanager.utils.permissions import is_admin
import logging

logger = logging.getLogger(__name__)


@login_required
def api_inventory_list(request):
    try:
        shed = request.GET.get('shed', 'shed1')
        inventories = InventoryNew.objects.filter(shed_name=shed).select_related('department', 'asset_category')
        
        data = [{
            'id': inv.id,
            'department': inv.department.name,
            'department_id': inv.department.id,
            'asset_category': inv.asset_category.name,
            'asset_category_id': inv.asset_category.id,
            'quantity': inv.quantity,
            'shed_name': inv.shed_name,
        } for inv in inventories]
        
        return JsonResponse({'inventory': data, 'total': len(data)})
    except Exception as e:
        logger.error(f"Error in api_inventory_list: {str(e)}")
        return JsonResponse({'inventory': [], 'total': 0, 'error': str(e)}, status=500)


@login_required
def api_inventory_update(request):
    try:
        if request.method == 'POST':
            import json
            data = json.loads(request.body)
            
            department_id = data.get('department_id')
            asset_category_id = data.get('asset_category_id')
            quantity = data.get('quantity', 0)
            shed_name = data.get('shed_name', 'shed1')
            
            department = Department.objects.get(id=department_id)
            asset_category = AssetCategory.objects.get(id=asset_category_id)
            
            inv, created = InventoryNew.objects.get_or_create(
                department=department,
                asset_category=asset_category,
                shed_name=shed_name,
                defaults={'quantity': 0}
            )
            
            old_quantity = inv.quantity
            inv.quantity = quantity
            inv.save()
            
            InventoryAuditLog.objects.create(
                department=department.name,
                asset_category=asset_category.name,
                old_quantity=old_quantity,
                new_quantity=quantity,
                shed_name=shed_name,
                action='update' if not created else 'create',
                changed_by=request.user
            )
            
            logger.info(f"Inventory updated: {department.name}/{asset_category.name} by {request.user.username}")
            return JsonResponse({
                'status': 'success',
                'message': 'Inventory updated',
                'old_quantity': old_quantity,
                'new_quantity': quantity
            })
        
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)
    except Department.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Department not found'}, status=404)
    except AssetCategory.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Asset category not found'}, status=404)
    except Exception as e:
        logger.error(f"Error in api_inventory_update: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def api_inventory_totals(request):
    try:
        shed = request.GET.get('shed', 'shed1')
        
        row_totals = {}
        column_totals = {}
        grand_total = 0
        
        inventories = InventoryNew.objects.filter(shed_name=shed)
        
        for inv in inventories:
            dept_name = inv.department.name
            cat_name = inv.asset_category.name
            
            row_totals[dept_name] = row_totals.get(dept_name, 0) + inv.quantity
            column_totals[cat_name] = column_totals.get(cat_name, 0) + inv.quantity
            grand_total += inv.quantity
        
        return JsonResponse({
            'row_totals': row_totals,
            'column_totals': column_totals,
            'grand_total': grand_total
        })
    except Exception as e:
        logger.error(f"Error in api_inventory_totals: {str(e)}")
        return JsonResponse({
            'row_totals': {},
            'column_totals': {},
            'grand_total': 0,
            'error': str(e)
        }, status=500)


@login_required
def api_departments_list(request):
    try:
        departments = Department.objects.filter(is_active=True)
        data = [{'id': d.id, 'name': d.name, 'code': d.code} for d in departments]
        return JsonResponse({'departments': data})
    except Exception as e:
        logger.error(f"Error in api_departments_list: {str(e)}")
        return JsonResponse({'departments': [], 'error': str(e)}, status=500)


@login_required
def api_asset_categories_list(request):
    try:
        categories = AssetCategory.objects.filter(is_active=True)
        data = [{'id': c.id, 'name': c.name, 'code': c.code, 'unit': c.unit} for c in categories]
        return JsonResponse({'asset_categories': data})
    except Exception as e:
        logger.error(f"Error in api_asset_categories_list: {str(e)}")
        return JsonResponse({'asset_categories': [], 'error': str(e)}, status=500)


@login_required
def api_audit_log(request):
    try:
        shed = request.GET.get('shed')
        logs = InventoryAuditLog.objects.all()
        if shed:
            logs = logs.filter(shed_name=shed)
        logs = logs.order_by('-changed_at')[:100]
        
        data = [{
            'id': log.id,
            'department': log.department,
            'asset_category': log.asset_category,
            'old_quantity': log.old_quantity,
            'new_quantity': log.new_quantity,
            'action': log.action,
            'changed_by': log.changed_by.username if log.changed_by else 'System',
            'changed_at': log.changed_at.strftime('%Y-%m-%d %H:%M:%S')
        } for log in logs]
        
        return JsonResponse({'audit_log': data})
    except Exception as e:
        logger.error(f"Error in api_audit_log: {str(e)}")
        return JsonResponse({'audit_log': [], 'error': str(e)}, status=500)


@login_required
@user_passes_test(is_admin)
def data_backup(request):
    try:
        import os
        import shutil
        from datetime import datetime
        from django.conf import settings
        
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        db_path = settings.DATABASES['default']['NAME']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'backup_{timestamp}.sqlite3'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        shutil.copy2(db_path, backup_path)
        
        messages.success(request, f'Backup created successfully: {backup_filename}')
        logger.info(f"Database backup created by {request.user.username}: {backup_filename}")
        return redirect('dashboard')
    except Exception as e:
        logger.error(f"Error creating backup: {str(e)}")
        messages.error(request, 'Failed to create backup.')
        return redirect('dashboard')