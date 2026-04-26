from django.db import migrations, models


def create_initial_data(apps, schema_editor):
    Module = apps.get_model('taskmanager', 'Module')
    Permission = apps.get_model('taskmanager', 'Permission')
    Role = apps.get_model('taskmanager', 'Role')
    
    # Create Modules
    modules_data = [
        ('Task Management', 'tasks', 'Task management module'),
        ('Inventory', 'inventory', 'Inventory management module'),
        ('ERP Service', 'erp', 'ERP service module'),
        ('Dashboard', 'dashboard', 'Dashboard module'),
        ('User Management', 'users', 'User management module'),
        ('Reports', 'reports', 'Reports module'),
    ]
    
    modules = {}
    for name, code, desc in modules_data:
        module, created = Module.objects.get_or_create(
            code=code,
            defaults={'name': name, 'description': desc, 'is_active': True}
        )
        modules[code] = module
    
    # Create Roles
    roles_data = [
        ('User', 'user', 'Regular user with basic access'),
        ('Moderator', 'moderator', 'Moderator with extended access'),
        ('Manager', 'manager', 'Manager with team management access'),
        ('Admin', 'admin', 'Administrator with full access'),
    ]
    
    roles = {}
    for name, code, desc in roles_data:
        role, created = Role.objects.get_or_create(
            code=code,
            defaults={'name': name, 'description': desc, 'is_active': True}
        )
        roles[code] = role
    
    # Create Permissions and assign to roles
    
    # User permissions - can view tasks, inventory, dashboard
    user_perms = {
        'tasks': 'view',
        'inventory': 'view',
        'dashboard': 'view',
    }
    
    for module_code, actions in user_perms.items():
        permission, created = Permission.objects.get_or_create(
            module=modules[module_code],
            defaults={'actions': actions}
        )
        roles['user'].permissions.add(permission)
    
    # Moderator permissions - view, create, edit
    moderator_perms = {
        'tasks': 'view,create,edit',
        'inventory': 'view,create,edit',
        'dashboard': 'view',
        'erp': 'view',
    }
    
    for module_code, actions in moderator_perms.items():
        permission, created = Permission.objects.get_or_create(
            module=modules[module_code],
            defaults={'actions': actions}
        )
        roles['moderator'].permissions.add(permission)
    
    # Manager permissions - view, create, edit, delete
    manager_perms = {
        'tasks': 'view,create,edit,delete',
        'inventory': 'view,create,edit,delete',
        'dashboard': 'view',
        'erp': 'view,create,edit',
        'users': 'view',
        'reports': 'view',
    }
    
    for module_code, actions in manager_perms.items():
        permission, created = Permission.objects.get_or_create(
            module=modules[module_code],
            defaults={'actions': actions}
        )
        roles['manager'].permissions.add(permission)
    
    # Admin permissions - all actions on all modules
    admin_perms = {
        'tasks': 'view,create,edit,delete',
        'inventory': 'view,create,edit,delete',
        'dashboard': 'view,create,edit,delete',
        'erp': 'view,create,edit,delete',
        'users': 'view,create,edit,delete',
        'reports': 'view,create,edit,delete',
    }
    
    for module_code, actions in admin_perms.items():
        permission, created = Permission.objects.get_or_create(
            module=modules[module_code],
            defaults={'actions': actions}
        )
        roles['admin'].permissions.add(permission)


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0011_remove_permission_action_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
