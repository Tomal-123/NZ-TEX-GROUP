from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from taskmanager.models import Task, Category, Comment
from taskmanager.utils.pagination import paginate_queryset, get_pagination_context
from taskmanager.utils.permissions import is_admin, is_manager
import csv
import logging

logger = logging.getLogger(__name__)


@login_required
def create_task(request):
    try:
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
            
            if not title:
                messages.error(request, 'Title is required.')
                return render(request, 'task/create_task.html', {'categories': categories, 'users': users})
            
            category = Category.objects.get(id=category_id) if category_id else None
            
            task = Task.objects.create(
                title=title,
                description=description,
                status=status,
                priority=priority,
                due_date=due_date if due_date else None,
                category=category,
                created_by=request.user
            )
            
            if assigned_to_ids:
                assigned_users = User.objects.filter(id__in=assigned_to_ids)
                task.assigned_to.set(assigned_users)
            
            messages.success(request, 'Task created successfully!')
            logger.info(f"Task created: {task.id} by {request.user.username}")
            return redirect('task_list')
        
        return render(request, 'task/create_task.html', {'categories': categories, 'users': users})
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        messages.error(request, 'Failed to create task.')
        return redirect('task_list')


@login_required
def task_list(request):
    try:
        tasks = Task.objects.all().order_by('-created_at')
        page_obj = paginate_queryset(request, tasks, per_page=15)
        return render(request, 'task/task_list.html', get_pagination_context(page_obj))
    except Exception as e:
        logger.error(f"Error in task list: {str(e)}")
        messages.error(request, 'An error occurred while loading tasks.')
        return render(request, 'task/task_list.html', {'tasks': [], 'page_obj': None, 'is_paginated': False})


@login_required
def edit_task(request, task_id):
    try:
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
            logger.info(f"Task updated: {task.id} by {request.user.username}")
            return redirect('task_list')
        
        return render(request, 'task/edit_task.html', {'task': task, 'categories': categories, 'users': users})
    except Task.DoesNotExist:
        messages.error(request, 'Task not found.')
        return redirect('task_list')
    except Exception as e:
        logger.error(f"Error editing task: {str(e)}")
        messages.error(request, 'Failed to update task.')
        return redirect('task_list')


@login_required
def delete_task(request, task_id):
    try:
        if request.method == 'POST':
            task = Task.objects.get(id=task_id)
            task.delete()
            messages.success(request, 'Task deleted!')
            logger.info(f"Task deleted: {task_id} by {request.user.username}")
        return redirect('task_list')
    except Task.DoesNotExist:
        messages.error(request, 'Task not found.')
        return redirect('task_list')
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        messages.error(request, 'Failed to delete task.')
        return redirect('task_list')


@login_required
def update_task_status(request, task_id):
    try:
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
            
            logger.info(f"Task status updated: {task.id} to {new_status} by {request.user.username}")
            return JsonResponse({
                'success': True,
                'status': new_status,
                'color': status_colors.get(new_status, '#3B82F6'),
                'message': status_texts.get(new_status, 'Status updated')
            })
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Task not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating task status: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
def approve_task(request, task_id):
    try:
        if request.method == 'POST':
            task = Task.objects.get(id=task_id)
            new_status = request.POST.get('status', 'in_progress')
            task.status = new_status
            task.save()
            status_display = task.get_status_display()
            messages.success(request, f'Task status changed to {status_display}!')
            logger.info(f"Task approved: {task.id} to {new_status} by {request.user.username}")
        return redirect('dashboard')
    except Task.DoesNotExist:
        messages.error(request, 'Task not found.')
        return redirect('dashboard')
    except Exception as e:
        logger.error(f"Error approving task: {str(e)}")
        messages.error(request, 'Failed to approve task.')
        return redirect('dashboard')


@login_required
def add_comment(request, task_id):
    try:
        if request.method == 'POST':
            task = Task.objects.get(id=task_id)
            text = request.POST.get('text')
            if text:
                Comment.objects.create(task=task, user=request.user, text=text)
                logger.info(f"Comment added to task {task_id} by {request.user.username}")
                return JsonResponse({'success': True})
        return JsonResponse({'success': False})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Task not found'}, status=404)
    except Exception as e:
        logger.error(f"Error adding comment: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
def export_tasks_csv(request):
    try:
        tasks = Task.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tasks_export.csv"'
        writer = csv.writer(response)
        writer.writerow(['Title', 'Description', 'Status', 'Priority', 'Due Date', 'Category', 'Assigned To', 'Created By', 'Created At'])
        
        for task in tasks:
            assigned = ', '.join([u.username for u in task.assigned_to.all()])
            writer.writerow([
                task.title,
                task.description,
                task.status,
                task.priority,
                task.due_date,
                task.category.name if task.category else '',
                assigned,
                task.created_by.username if task.created_by else '',
                task.created_at
            ])
        
        logger.info(f"Tasks exported as CSV by {request.user.username}")
        return response
    except Exception as e:
        logger.error(f"Error exporting tasks: {str(e)}")
        messages.error(request, 'Failed to export tasks.')
        return redirect('dashboard')


@login_required
def import_tasks_csv(request):
    try:
        if request.method == 'POST':
            csv_file = request.FILES.get('file')
            if csv_file:
                decoded = csv_file.read().decode('utf-8')
                reader = csv.reader(decoded.splitlines())
                next(reader, None)
                
                imported_count = 0
                for row in reader:
                    if len(row) >= 2:
                        title = row[0].strip()
                        description = row[1].strip() if len(row) > 1 else ''
                        Task.objects.create(
                            title=title,
                            description=description,
                            status='pending',
                            priority='medium',
                            created_by=request.user
                        )
                        imported_count += 1
                
                messages.success(request, f'Successfully imported {imported_count} tasks!')
                logger.info(f"{imported_count} tasks imported by {request.user.username}")
        return redirect('dashboard')
    except Exception as e:
        logger.error(f"Error importing tasks: {str(e)}")
        messages.error(request, 'Failed to import tasks.')
        return redirect('dashboard')