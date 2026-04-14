from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Case, When
from .models import Task, Category, Comment, Notification, Contact

def home(request):
    tasks = Task.objects.all().order_by(
        Case(
            When(status='in_progress', then=1),
            When(status='pending', then=2),
            When(status='completed', then=3),
        ),
        '-created_at'
    )[:10]
    pending_count = Task.objects.filter(status='pending').count()
    in_progress_count = Task.objects.filter(status='in_progress').count()
    completed_count = Task.objects.filter(status='completed').count()
    users = User.objects.filter(assigned_tasks__isnull=False).distinct()
    return render(request, 'index.html', {
        'tasks': tasks,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'users': users
    })

@login_required
def dashboard(request):
    tasks = Task.objects.all().order_by(
        Case(
            When(status='in_progress', then=1),
            When(status='pending', then=2),
            When(status='completed', then=3),
        ),
        '-created_at'
    )
    pending_count = Task.objects.filter(status='pending').count()
    in_progress_count = Task.objects.filter(status='in_progress').count()
    completed_count = Task.objects.filter(status='completed').count()
    users = User.objects.filter(assigned_tasks__isnull=False).distinct()
    return render(request, 'dashboard.html', {
        'tasks': tasks,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'users': users
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def create_task(request):
    categories = Category.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        category_id = request.POST.get('category')
        assigned_to_ids = request.POST.getlist('assigned_to')
        
        if category_id:
            category = Category.objects.get(id=category_id)
        else:
            category = None
        
        task = Task.objects.create(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            category=category,
            created_by=request.user
        )
        
        if assigned_to_ids:
            assigned_users = User.objects.filter(id__in=assigned_to_ids)
            task.assigned_to.set(assigned_users)
        
        messages.success(request, 'Task created successfully!')
        return redirect('task_list')
    
    return render(request, 'task/create_task.html', {'categories': categories, 'users': users})

@login_required
def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'task/task_list.html', {'tasks': tasks})

@login_required
def update_task_status(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        new_status = request.POST.get('status')
        task.status = new_status
        task.save()
        
        status_colors = {
            'pending': '#EF4444',
            'in_progress': '#F59E0B', 
            'completed': '#10B981'
        }
        status_texts = {
            'pending': 'Task marked as Pending',
            'in_progress': 'Task marked as In Progress',
            'completed': 'Task completed!'
        }
        
        return JsonResponse({
            'success': True,
            'status': new_status,
            'color': status_colors.get(new_status, '#3B82F6'),
            'message': status_texts.get(new_status, 'Status updated')
        })
    return JsonResponse({'success': False})

@login_required
def add_comment(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        text = request.POST.get('text')
        if text:
            Comment.objects.create(task=task, user=request.user, text=text)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def approve_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.status = 'in_progress'
        task.save()
        messages.success(request, 'Task approved!')
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
        messages.success(request, 'Task deleted!')
    return redirect('task_list')

@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    categories = Category.objects.all()
    users = User.objects.all()
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        
        due_date = request.POST.get('due_date')
        task.due_date = due_date if due_date else None
        
        category_id = request.POST.get('category')
        task.category = Category.objects.get(id=category_id) if category_id else None
        
        assigned_to_ids = request.POST.getlist('assigned_to')
        if assigned_to_ids:
            assigned_users = User.objects.filter(id__in=assigned_to_ids)
            task.assigned_to.set(assigned_users)
        else:
            task.assigned_to.clear()
        
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('task_list')
    
    return render(request, 'task/edit_task.html', {'task': task, 'categories': categories, 'users': users})

def contact(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            Contact.objects.create(
                company_name=request.POST.get('company_name'),
                name=request.POST.get('name'),
                department=request.POST.get('department'),
                designation=request.POST.get('designation'),
                ip_phone=request.POST.get('ip_phone'),
                mobile=request.POST.get('mobile'),
                email=request.POST.get('email')
            )
            messages.success(request, 'Contact added successfully!')
        
        elif action == 'edit':
            contact_id = request.POST.get('contact_id')
            contact = Contact.objects.get(id=contact_id)
            contact.company_name = request.POST.get('company_name')
            contact.name = request.POST.get('name')
            contact.department = request.POST.get('department')
            contact.designation = request.POST.get('designation')
            contact.ip_phone = request.POST.get('ip_phone')
            contact.mobile = request.POST.get('mobile')
            contact.email = request.POST.get('email')
            contact.save()
            messages.success(request, 'Contact updated successfully!')
        
        elif action == 'delete':
            contact_id = request.POST.get('contact_id')
            Contact.objects.get(id=contact_id).delete()
            messages.success(request, 'Contact deleted successfully!')
        
        elif action == 'import':
            contacts = request.POST.get('contacts_data')
            if contacts:
                import csv
                import io
                reader = csv.reader(io.StringIO(contacts))
                next(reader)
                for row in reader:
                    if len(row) >= 7:
                        Contact.objects.create(
                            company_name=row[1],
                            name=row[2],
                            department=row[3],
                            designation=row[4],
                            ip_phone=row[5],
                            mobile=row[6],
                            email=row[7] if len(row) > 7 else ''
                        )
                messages.success(request, 'Contacts imported successfully!')
        
        return redirect('contact')
    
    contacts = Contact.objects.all().order_by('company_name', 'name')
    return render(request, 'contact.html', {'contacts': contacts})

@login_required
def notifications(request):
    notifications_list = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications_list})


def get_contacts(request):
    contacts = Contact.objects.all().order_by('company_name', 'name')
    data = []
    for contact in contacts:
        data.append({
            'id': contact.id,
            'company_name': contact.company_name,
            'name': contact.name,
            'department': contact.department,
            'designation': contact.designation,
            'ip_phone': contact.ip_phone,
            'mobile': contact.mobile,
            'email': contact.email,
        })
    return JsonResponse({'contacts': data})

@login_required
def create_notification(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            for user in User.objects.all():
                Notification.objects.create(user=user, message=message)
            messages.success(request, 'Notification sent to all users!')
        return redirect('notifications')
    return redirect('notifications')

@login_required
def mark_notification_read(request, notif_id):
    notif = Notification.objects.get(id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notifications')

@login_required
def delete_notification(request, notif_id):
    notif = Notification.objects.get(id=notif_id, user=request.user)
    notif.delete()
    return redirect('notifications')

@login_required
def get_notifications(request):
    notifications_list = Notification.objects.filter(user=request.user)[:5]
    data = [{
        'id': n.id,
        'message': n.message,
        'is_read': n.is_read,
        'created_at': n.created_at.strftime('%b %d, %H:%M'),
        'unread_count': Notification.objects.filter(user=request.user, is_read=False).count()
    } for n in notifications_list]
    return JsonResponse({'notifications': data})

@login_required
def profile(request):
    return render(request, 'profile.html')

def organogram(request):
    return render(request, 'organogram.html')

def team(request):
    return render(request, 'team.html')

def erp_service(request):
    return render(request, 'erp.html')