from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from functools import wraps
from .models import Module, Permission, UserRole


def has_permission(module_code, action):
    """
    Decorator to check if user has permission for a specific module and action.
    
    Usage:
        @has_permission('tasks', 'view')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Superuser has all permissions
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check if user has the required permission
            user_roles = UserRole.objects.filter(
                user=request.user,
                is_active=True,
                role__is_active=True
            ).select_related('role')
            
            has_access = False
            for user_role in user_roles:
                permission = Permission.objects.filter(
                    role=user_role.role,
                    module__code=module_code,
                    module__is_active=True
                ).first()
                
                if permission and action in permission.get_actions_list():
                    has_access = True
                    break
            
            if not has_access:
                raise PermissionDenied("You don't have permission to access this module.")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def has_module_access(module_code):
    """
    Decorator to check if user has any access to a module.
    
    Usage:
        @has_module_access('tasks')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Superuser has all permissions
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check if user has any permission for the module
            user_roles = UserRole.objects.filter(
                user=request.user,
                is_active=True,
                role__is_active=True
            ).select_related('role')
            
            has_access = False
            for user_role in user_roles:
                permission = Permission.objects.filter(
                    role=user_role.role,
                    module__code=module_code,
                    module__is_active=True
                ).exists()
                
                if permission:
                    has_access = True
                    break
            
            if not has_access:
                raise PermissionDenied("You don't have permission to access this module.")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def get_user_permissions(user):
    """
    Get all permissions for a user.
    Returns a dict with module_code as key and list of actions as value.
    """
    if user.is_superuser:
        # Superuser has all permissions for all active modules
        modules = Module.objects.filter(is_active=True)
        permissions = {}
        for module in modules:
            permissions[module.code] = ['view', 'create', 'edit', 'delete']
        return permissions
    
    permissions = {}
    user_roles = UserRole.objects.filter(
        user=user,
        is_active=True,
        role__is_active=True
    ).select_related('role')
    
    for user_role in user_roles:
        perms = Permission.objects.filter(
            role=user_role.role,
            module__is_active=True
        ).select_related('module')
        
        for perm in perms:
            module_code = perm.module.code
            actions = perm.get_actions_list()
            if module_code not in permissions:
                permissions[module_code] = []
            for action in actions:
                if action not in permissions[module_code]:
                    permissions[module_code].append(action)
    
    return permissions


def user_can(user, module_code, action):
    """
    Check if user has permission for a specific module and action.
    
    Usage:
        if user_can(request.user, 'tasks', 'view'):
            ...
    """
    if user.is_superuser:
        return True
    
    user_roles = UserRole.objects.filter(
        user=user,
        is_active=True,
        role__is_active=True
    ).select_related('role')
    
    for user_role in user_roles:
        permission = Permission.objects.filter(
            role=user_role.role,
            module__code=module_code,
            module__is_active=True
        ).first()
        
        if permission and action in permission.get_actions_list():
            return True
    
    return False
