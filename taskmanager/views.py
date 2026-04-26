from .views import (
    home, dashboard, register, profile, organogram, team, erp_service, network_diagram,
    create_task, task_list, edit_task, delete_task, update_task_status,
    approve_task, add_comment, export_tasks_csv, import_tasks_csv,
    inventory, add_item, inventory_smart, export_shed_csv, export_shed_excel,
    import_shed_csv, save_shed_inventory, add_shed_row, add_shed_column,
    manage_shed, manage_department, manage_category,
    contact, get_contacts, notifications, create_notification,
    mark_notification_read, delete_notification, get_notifications,
    api_inventory_list, api_inventory_update, api_inventory_totals,
    api_departments_list, api_asset_categories_list, api_audit_log,
    data_backup
)

__all__ = [
    'home', 'dashboard', 'register', 'profile', 'organogram', 'team', 'erp_service', 'network_diagram',
    'create_task', 'task_list', 'edit_task', 'delete_task', 'update_task_status',
    'approve_task', 'add_comment', 'export_tasks_csv', 'import_tasks_csv',
    'inventory', 'add_item', 'inventory_smart', 'export_shed_csv', 'export_shed_excel',
    'import_shed_csv', 'save_shed_inventory', 'add_shed_row', 'add_shed_column',
    'manage_shed', 'manage_department', 'manage_category',
    'contact', 'get_contacts', 'notifications', 'create_notification',
    'mark_notification_read', 'delete_notification', 'get_notifications',
    'api_inventory_list', 'api_inventory_update', 'api_inventory_totals',
    'api_departments_list', 'api_asset_categories_list', 'api_audit_log',
    'data_backup'
]