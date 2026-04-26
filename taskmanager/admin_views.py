from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Module, Permission, Role, UserRole, Task, Contact
from django.core.paginator import Paginator
from django.db.models import Count, Q

def is_admin(user):
    """Check if user is admin or has admin role."""
    if user.is_superuser:
        return True
    return UserRole.objects.filter(
        user=user,
        role__code='admin',
        is_active=True
    ).exists()

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Custom admin dashboard."""
    # Stats
    stats = {
        'total_users': User.objects.filter(is_active=True).count(),
        'total_tasks': Task.objects.count(),
        'total_roles': Role.objects.filter(is_active=True).count(),
        'total_modules': Module.objects.filter(is_active=True).count(),
    }
    
    # Recent users
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    
    # Recent tasks
    recent_tasks = Task.objects.all().order_by('-created_at')[:5]
    
    context = {
        'stats': stats,
        'recent_users': recent_users,
        'recent_tasks': recent_tasks,
    }
    return render(request, 'admin_custom/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    """Manage users."""
    users = User.objects.all().annotate(
        role_count=Count('user_roles', filter=Q(user_roles__is_active=True))
    )
    
    # Pagination
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'admin_custom/users.html', context)

@login_required
@user_passes_test(is_admin)
def admin_roles(request):
    """Manage roles."""
    roles = Role.objects.filter(is_active=True).annotate(
        user_count=Count('user_roles', filter=Q(user_roles__is_active=True)),
        perm_count=Count('permissions')
    )
    
    context = {
        'roles': roles,
    }
    return render(request, 'admin_custom/roles.html', context)

@login_required
@user_passes_test(is_admin)
def admin_modules(request):
    """Manage modules and permissions."""
    modules = Module.objects.filter(is_active=True).prefetch_related('permissions__module')
    
    context = {
        'modules': modules,
    }
    return render(request, 'admin_custom/modules.html', context)

@login_required
@user_passes_test(is_admin)
def admin_assign_role(request, user_id):
    """Assign role to user."""
    user = User.objects.get(id=user_id)
    roles = Role.objects.filter(is_active=True)
    
    if request.method == 'POST':
        role_id = request.POST.get('role')
        role = Role.objects.get(id=role_id)
        
        # Check if already assigned
        user_role, created = UserRole.objects.get_or_create(
            user=user,
            role=role,
            defaults={'is_active': True}
        )
        
        if not created:
            user_role.is_active = True
            user_role.save()
        
        messages.success(request, f'Role "{role.name}" assigned to {user.username}')
        return redirect('admin_users')
    
    context = {
        'user_obj': user,
        'roles': roles,
    }
    return render(request, 'admin_custom/assign_role.html', context)
@login_required
@user_passes_test(is_admin)
def admin_contacts(request):
    """Manage contacts."""
    from django.db.models import Q
    contacts = Contact.objects.all().order_by('-created_at')
    
    # Search/filter
    query = request.GET.get('q')
    if query:
        contacts = contacts.filter(
            Q(company_name__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(department__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'admin_custom/contacts.html', context)

