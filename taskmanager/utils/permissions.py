from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from taskmanager.models import UserRole, Permission, Role


def has_permission(user, module_code, action):
    if user.is_superuser:
        return True
    
    user_roles = UserRole.objects.filter(
        user=user,
        is_active=True
    ).select_related('role')
    
    for user_role in user_roles:
        role = user_role.role
        if role and role.is_active:
            for perm in role.permissions.all():
                if perm.module.code == module_code and perm.has_action(action):
                    return True
    return False


def require_permission(module_code, action):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if has_permission(request.user, module_code, action):
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('dashboard')
        return wrapped_view
    return decorator


def is_admin(user):
    if user.is_superuser:
        return True
    return UserRole.objects.filter(
        user=user,
        role__code='admin',
        is_active=True
    ).exists()


def is_manager(user):
    if user.is_superuser:
        return True
    if UserRole.objects.filter(user=user, role__code='admin', is_active=True).exists():
        return True
    return UserRole.objects.filter(
        user=user,
        role__code='manager',
        is_active=True
    ).exists()


def is_staff_member(user):
    if user.is_superuser:
        return True
    if user.is_staff:
        return True
    return UserRole.objects.filter(
        user=user,
        role__is_active=True
    ).exists()