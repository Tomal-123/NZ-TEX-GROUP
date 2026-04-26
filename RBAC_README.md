# Role-Based Access Control (RBAC) System

## Overview
Module-wise permission system with custom roles implemented.

## Models Created
1. **Module** - Represents different modules (Tasks, Inventory, ERP, etc.)
2. **Permission** - Links modules with actions (view, create, edit, delete)
3. **Role** - Custom roles (User, Moderator, Manager, Admin)
4. **UserRole** - Assigns roles to users

## Default Roles & Permissions

### User
- Tasks: view
- Inventory: view
- Dashboard: view

### Moderator
- Tasks: view, create, edit
- Inventory: view, create, edit
- Dashboard: view
- ERP: view

### Manager
- Tasks: view, create, edit, delete
- Inventory: view, create, edit, delete
- Dashboard: view
- ERP: view, create, edit
- Users: view
- Reports: view

### Admin
- Full access (view, create, edit, delete) to all modules

## How to Use

### 1. Assign Role to User (Admin Panel)
1. Login to admin panel: `/admin/`
2. Go to "Taskmanager" section
3. Click "User roles"
4. Add new user role:
   - Select user
   - Select role (User/Moderator/Manager/Admin)
   - Check "Is active"

### 2. Protect Views with Permissions (Using Decorators)

```python
from taskmanager.decorators import has_permission, has_module_access

@has_module_access('tasks')  # Check if user has any access to tasks module
def task_list(request):
    ...

@has_permission('tasks', 'create')  # Check if user can create tasks
def create_task(request):
    ...
```

### 3. Check Permissions in Templates

Load the template tags first:
```django
{% load permissions %}
```

Check permissions:
```django
{% if request.user|has_perm:"tasks,view" %}
    <a href="{% url 'task_list' %}">View Tasks</a>
{% endif %}

{% if request.user|has_perm:"tasks,create" %}
    <a href="{% url 'create_task' %}">Create Task</a>
{% endif %}
```

Check module access:
```django
{% if request.user|has_module_perm:"inventory" %}
    <a href="{% url 'inventory' %}">Inventory</a>
{% endif %}
```

### 4. Check Permissions in Views

```python
from taskmanager.decorators import user_can

def my_view(request):
    if user_can(request.user, 'tasks', 'edit'):
        # User can edit tasks
        pass
```

## Files Created/Modified
- `taskmanager/decorators.py` - Permission check decorators
- `taskmanager/context_processors.py` - Makes permissions available in templates
- `taskmanager/templatetags/permissions.py` - Template tags for permission checks
- `taskmanager/migrations/0012_initial_modules_roles_permissions.py` - Initial data

## Management Command (Optional)
To assign role from command line:
```bash
python manage.py assign_role <username> <role_code>
```

Create this command if needed.
