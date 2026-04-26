from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from taskmanager.views import (
    home, dashboard, profile, organogram, team, erp_service, network_diagram,
    create_task, task_list, edit_task, delete_task, update_task_status,
    approve_task, add_comment, export_tasks_csv, import_tasks_csv,
    inventory, add_item, inventory_smart, export_shed_csv, export_shed_excel,
    import_shed_csv, save_shed_inventory, add_shed_row, add_shed_column,
    manage_shed, manage_department, manage_category,
    contact, get_contacts, notifications, create_notification,
    mark_notification_read, delete_notification, get_notifications,
    api_inventory_list, api_inventory_update, api_inventory_totals,
    api_departments_list, api_asset_categories_list, api_audit_log,
    data_backup, register
)
from taskmanager.admin_views import admin_dashboard, admin_users, admin_roles, admin_modules, admin_assign_role

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/export/', export_tasks_csv, name='export_tasks_csv'),
    path('dashboard/import/', import_tasks_csv, name='import_tasks_csv'),
    path('profile/', profile, name='profile'),
    path('organogram/', organogram, name='organogram'),
    path('network/', network_diagram, name='network_diagram'),
    path('team/', team, name='team'),
    path('erp/', erp_service, name='erp_service'),
    
    path('inventory/', inventory, name='inventory'),
    path('inventory/add-item/', add_item, name='add_item'),
    path('inventory/shed-1/', inventory_smart, {'shed': 'shed1'}, name='inventory_shed1'),
    path('inventory/shed-2/', inventory_smart, {'shed': 'shed2'}, name='inventory_shed2'),
    path('inventory/shed-3/', inventory_smart, {'shed': 'shed3'}, name='inventory_shed3'),
    path('inventory/shed3/', inventory_smart, {'shed': 'shed3'}, name='inventory_shed3_alt'),
    path('inventory/shed2/', inventory_smart, {'shed': 'shed2'}, name='inventory_shed2_alt'),
    path('inventory/shed1/', inventory_smart, {'shed': 'shed1'}, name='inventory_shed1_alt'),
    path('inventory/it-stock/', inventory_smart, {'shed': 'it_stock'}, name='inventory_it_stock'),
    path('inventory/all-it/', inventory_smart, {'shed': 'all_it'}, name='inventory_all_it'),
    path('inventory/it-department/', inventory_smart, {'shed': 'it_department'}, name='inventory_it_department'),
    path('inventory/manage-shed/', manage_shed, name='manage_shed'),
    path('inventory/manage-department/', manage_department, name='manage_department'),
    path('inventory/manage-category/', manage_category, name='manage_category'),
    
    path('inventory/shed-1/export/', export_shed_csv, {'shed': 'shed1'}, name='export_shed1_csv'),
    path('inventory/shed-1/export-excel/', export_shed_excel, {'shed': 'shed1'}, name='export_shed1_excel'),
    path('inventory/shed-2/export/', export_shed_csv, {'shed': 'shed2'}, name='export_shed2_csv'),
    path('inventory/shed-2/export-excel/', export_shed_excel, {'shed': 'shed2'}, name='export_shed2_excel'),
    path('inventory/shed-3/export/', export_shed_csv, {'shed': 'shed3'}, name='export_shed3_csv'),
    path('inventory/shed-3/export-excel/', export_shed_excel, {'shed': 'shed3'}, name='export_shed3_excel'),
    path('inventory/it-department/export/', export_shed_csv, {'shed': 'it_department'}, name='export_it_department_csv'),
    path('inventory/it-department/export-excel/', export_shed_excel, {'shed': 'it_department'}, name='export_it_department_excel'),
    path('inventory/it-stock/export/', export_shed_csv, {'shed': 'it_stock'}, name='export_it_stock_csv'),
    path('inventory/it-stock/export-excel/', export_shed_excel, {'shed': 'it_stock'}, name='export_it_stock_excel'),
    path('inventory/all-it/export/', export_shed_csv, {'shed': 'all_it'}, name='export_all_it_csv'),
    path('inventory/all-it/export-excel/', export_shed_excel, {'shed': 'all_it'}, name='export_all_it_excel'),
    
    path('inventory/shed-1/import/', import_shed_csv, {'shed': 'shed1'}, name='import_shed1_csv'),
    path('inventory/shed-2/import/', import_shed_csv, {'shed': 'shed2'}, name='import_shed2_csv'),
    path('inventory/shed-3/import/', import_shed_csv, {'shed': 'shed3'}, name='import_shed3_csv'),
    path('inventory/it-stock/import/', import_shed_csv, {'shed': 'it_stock'}, name='import_it_stock_csv'),
    path('inventory/all-it/import/', import_shed_csv, {'shed': 'all_it'}, name='import_all_it_csv'),
    path('inventory/it-department/import/', import_shed_csv, {'shed': 'it_department'}, name='import_it_department_csv'),
    
    path('inventory/shed-1/save/', save_shed_inventory, {'shed': 'shed1'}, name='save_shed1_inventory'),
    path('inventory/shed-2/save/', save_shed_inventory, {'shed': 'shed2'}, name='save_shed2_inventory'),
    path('inventory/shed-3/save/', save_shed_inventory, {'shed': 'shed3'}, name='save_shed3_inventory'),
    path('inventory/it-stock/save/', save_shed_inventory, {'shed': 'it_stock'}, name='save_it_stock_inventory'),
    path('inventory/all-it/save/', save_shed_inventory, {'shed': 'all_it'}, name='save_all_it_inventory'),
    path('inventory/it-department/save/', save_shed_inventory, {'shed': 'it_department'}, name='save_it_department_inventory'),
    
    path('inventory/shed-1/add-row/', add_shed_row, {'shed': 'shed1'}, name='add_shed1_row'),
    path('inventory/shed-2/add-row/', add_shed_row, {'shed': 'shed2'}, name='add_shed2_row'),
    path('inventory/shed-3/add-row/', add_shed_row, {'shed': 'shed3'}, name='add_shed3_row'),
    path('inventory/it-stock/add-row/', add_shed_row, {'shed': 'it_stock'}, name='add_it_stock_row'),
    path('inventory/all-it/add-row/', add_shed_row, {'shed': 'all_it'}, name='add_all_it_row'),
    path('inventory/it-department/add-row/', add_shed_row, {'shed': 'it_department'}, name='add_it_department_row'),
    
    path('inventory/shed-1/add-column/', add_shed_column, {'shed': 'shed1'}, name='add_shed1_column'),
    path('inventory/shed-2/add-column/', add_shed_column, {'shed': 'shed2'}, name='add_shed2_column'),
    path('inventory/shed-3/add-column/', add_shed_column, {'shed': 'shed3'}, name='add_shed3_column'),
    path('inventory/it-stock/add-column/', add_shed_column, {'shed': 'it_stock'}, name='add_it_stock_column'),
    path('inventory/all-it/add-column/', add_shed_column, {'shed': 'all_it'}, name='add_all_it_column'),
    path('inventory/it-department/add-column/', add_shed_column, {'shed': 'it_department'}, name='add_it_department_column'),
    
    path('admin_custom/', admin_dashboard, name='admin_dashboard'),
    path('admin_custom/users/', admin_users, name='admin_users'),
    path('admin_custom/roles/', admin_roles, name='admin_roles'),
    path('admin_custom/modules/', admin_modules, name='admin_modules'),
    path('admin_custom/users/<int:user_id>/assign-role/', admin_assign_role, name='admin_assign_role'),
    
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('register/', register, name='register'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/<int:task_id>/status/', update_task_status, name='update_task_status'),
    path('tasks/<int:task_id>/comment/', add_comment, name='add_comment'),
    path('tasks/<int:task_id>/approve/', approve_task, name='approve_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('tasks/<int:task_id>/edit/', edit_task, name='edit_task'),
    
    path('contact/', contact, name='contact'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/create/', create_notification, name='create_notification'),
    path('notifications/<int:notif_id>/read/', mark_notification_read, name='mark_notification_read'),
    path('notifications/<int:notif_id>/delete/', delete_notification, name='delete_notification'),
    
    path('api/notifications/', get_notifications, name='get_notifications'),
    path('api/contacts/', get_contacts, name='get_contacts'),
    path('api/inventory/list/', api_inventory_list, name='api_inventory_list'),
    path('api/inventory/update/', api_inventory_update, name='api_inventory_update'),
    path('api/inventory/totals/', api_inventory_totals, name='api_inventory_totals'),
    path('api/inventory/departments/', api_departments_list, name='api_departments_list'),
    path('api/inventory/categories/', api_asset_categories_list, name='api_asset_categories_list'),
    path('api/inventory/audit-log/', api_audit_log, name='api_audit_log'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)