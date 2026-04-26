from django import template
from django.contrib.auth.models import User
from taskmanager.decorators import get_user_permissions, user_can

register = template.Library()


@register.simple_tag
def user_permissions(user):
    """Get all permissions for a user."""
    return get_user_permissions(user)


@register.filter
def has_perm(user, args):
    """
    Check if user has permission for module and action.
    Usage in template:
        {% if request.user|has_perm:"tasks,view" %}
            ...
        {% endif %}
    """
    if not user.is_authenticated:
        return False
    
    try:
        module_code, action = args.split(',')
        return user_can(user, module_code.strip(), action.strip())
    except:
        return False


@register.filter
def has_module_perm(user, module_code):
    """
    Check if user has any permission for a module.
    Usage in template:
        {% if request.user|has_module_perm:"tasks" %}
            ...
        {% endif %}
    """
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    from taskmanager.models import Module, Permission, UserRole
    
    user_roles = UserRole.objects.filter(
        user=user,
        is_active=True,
        role__is_active=True
    ).select_related('role')
    
    for user_role in user_roles:
        if Permission.objects.filter(
            role=user_role.role,
            module__code=module_code,
            module__is_active=True
        ).exists():
            return True
    
    return False
