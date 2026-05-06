from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Case, When
from taskmanager.models import Task, Category
from taskmanager.forms import CustomUserCreationForm
from taskmanager.utils.permissions import is_admin, is_manager
from taskmanager.utils.pagination import paginate_queryset, get_pagination_context
import logging

logger = logging.getLogger(__name__)


def register(request):
    try:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, f'Account created for {user.username}!')
                logger.info(f"New user registered: {user.username}")
                return redirect('home')
        else:
            form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in register view: {str(e)}")
        messages.error(request, 'An error occurred during registration.')
        return redirect('login')


@login_required
def home(request):
    # Redirect to the task dashboard as the homepage
    from django.shortcuts import redirect
    return redirect('dashboard')


@login_required
def dashboard(request):
    from datetime import datetime
    from calendar import monthrange
    from django.contrib.auth.models import User
    
    try:
        selected_month = request.GET.get('month')
        selected_year = request.GET.get('year')

        today = datetime.now()
        
        if selected_month and selected_year:
            month = int(selected_month)
            year = int(selected_year)
            _, last_day = monthrange(year, month)
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month, last_day, 23, 59, 59)
            tasks = Task.objects.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            )
        else:
            month = None
            year = None
            tasks = Task.objects.all()

        tasks = tasks.order_by('-created_at')

        pending_count = tasks.filter(status='pending').count()
        in_progress_count = tasks.filter(status='in_progress').count()
        completed_count = tasks.filter(status='completed').count()

        stats_year = int(selected_year) if selected_year else today.year
        monthly_stats = []
        for m in range(1, 13):
            m_start = datetime(stats_year, m, 1)
            _, m_last = monthrange(stats_year, m)
            m_end = datetime(stats_year, m, m_last, 23, 59, 59)
            m_total = Task.objects.filter(created_at__gte=m_start, created_at__lte=m_end).count()
            m_completed = Task.objects.filter(created_at__gte=m_start, created_at__lte=m_end, status='completed').count()
            monthly_stats.append({
                'month': m,
                'month_date': datetime(stats_year, m, 1),
                'total': m_total,
                'completed': m_completed
            })

        context = {
            'tasks': tasks,
            'pending_count': pending_count,
            'in_progress_count': in_progress_count,
            'completed_count': completed_count,
            'all_pending_count': Task.objects.filter(status='pending').count(),
            'all_in_progress_count': Task.objects.filter(status='in_progress').count(),
            'all_completed_count': Task.objects.filter(status='completed').count(),
            'all_tasks_count': Task.objects.count(),
            'users': User.objects.filter(assigned_tasks__isnull=False).distinct(),
            'selected_month': selected_month,
            'selected_year': selected_year,
            'monthly_stats': monthly_stats,
            'years': list(range(2023, 2031))
        }
        if selected_month and selected_year:
            context['selected_month_date'] = datetime(int(selected_year), int(selected_month), 1)
        
        return render(request, 'dashboard.html', context)
    except Exception as e:
        logger.error(f"Error in dashboard view: {str(e)}")
        messages.error(request, 'An error occurred while loading the dashboard.')
        return redirect('home')


@login_required
def profile(request):
    from django.contrib.auth.models import User
    
    try:
        if request.method == 'POST':
            user = request.user
            user.email = request.POST.get('email', user.email)
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()
            messages.success(request, 'Profile updated successfully!')
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        messages.error(request, 'Failed to update profile.')
    
    return render(request, 'profile.html')


@login_required
def organogram(request):
    return render(request, 'organogram.html')


@login_required
def team(request):
    return render(request, 'team.html')


@login_required
def erp_service(request):
    return render(request, 'erp.html')


@login_required
def network_diagram(request):
    return render(request, 'network_diagram.html')


@login_required
def hrm_service(request):
    return render(request, 'hrm.html', {'no_sidebar': True})