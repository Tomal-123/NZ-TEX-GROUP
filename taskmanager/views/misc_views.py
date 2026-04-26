from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from taskmanager.models import Contact, Notification, Task
from taskmanager.utils.pagination import paginate_queryset, get_pagination_context
import csv
import io
import logging

logger = logging.getLogger(__name__)


@login_required
def contact(request):
    try:
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
                logger.info(f"Contact added: {request.POST.get('name')} by {request.user.username}")
            
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
                logger.info(f"Contact updated: {contact.name} by {request.user.username}")
            
            elif action == 'delete':
                contact_id = request.POST.get('contact_id')
                Contact.objects.get(id=contact_id).delete()
                messages.success(request, 'Contact deleted successfully!')
                logger.info(f"Contact deleted by {request.user.username}")
            
            elif action == 'import':
                contacts_data = request.POST.get('contacts_data')
                if contacts_data:
                    reader = csv.reader(io.StringIO(contacts_data))
                    next(reader)
                    imported_count = 0
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
                            imported_count += 1
                    messages.success(request, f'Contacts imported successfully! ({imported_count} records)')
                    logger.info(f"{imported_count} contacts imported by {request.user.username}")
            
            return redirect('contact')
        
        contacts = Contact.objects.all().order_by('company_name', 'name')
        page_obj = paginate_queryset(request, contacts, per_page=20)
        return render(request, 'contact.html', get_pagination_context(page_obj))
    except Exception as e:
        logger.error(f"Error in contact view: {str(e)}")
        messages.error(request, 'An error occurred.')
        return redirect('dashboard')


@login_required
def get_contacts(request):
    try:
        contacts = Contact.objects.all().order_by('company_name', 'name')
        data = [{
            'id': contact.id,
            'company_name': contact.company_name,
            'name': contact.name,
            'department': contact.department,
            'designation': contact.designation,
            'ip_phone': contact.ip_phone,
            'mobile': contact.mobile,
            'email': contact.email,
        } for contact in contacts]
        return JsonResponse({'contacts': data})
    except Exception as e:
        logger.error(f"Error getting contacts: {str(e)}")
        return JsonResponse({'contacts': [], 'error': str(e)}, status=500)


@login_required
def notifications(request):
    try:
        notifications_list = Notification.objects.filter(user=request.user).order_by('-created_at')
        page_obj = paginate_queryset(request, notifications_list, per_page=20)
        return render(request, 'notifications.html', get_pagination_context(page_obj))
    except Exception as e:
        logger.error(f"Error in notifications view: {str(e)}")
        messages.error(request, 'An error occurred.')
        return redirect('dashboard')


@login_required
def create_notification(request):
    try:
        if request.method == 'POST':
            message = request.POST.get('message')
            if message:
                for user in User.objects.all():
                    Notification.objects.create(user=user, message=message)
                messages.success(request, 'Notification sent to all users!')
                logger.info(f"Notification sent by {request.user.username}: {message[:50]}...")
            return redirect('notifications')
        return redirect('notifications')
    except Exception as e:
        logger.error(f"Error creating notification: {str(e)}")
        messages.error(request, 'Failed to send notification.')
        return redirect('notifications')


@login_required
def mark_notification_read(request, notif_id):
    try:
        notif = Notification.objects.get(id=notif_id, user=request.user)
        notif.is_read = True
        notif.save()
        return redirect('notifications')
    except Notification.DoesNotExist:
        messages.error(request, 'Notification not found.')
        return redirect('notifications')
    except Exception as e:
        logger.error(f"Error marking notification read: {str(e)}")
        messages.error(request, 'An error occurred.')
        return redirect('notifications')


@login_required
def delete_notification(request, notif_id):
    try:
        notif = Notification.objects.get(id=notif_id, user=request.user)
        notif.delete()
        return redirect('notifications')
    except Notification.DoesNotExist:
        messages.error(request, 'Notification not found.')
        return redirect('notifications')
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}")
        messages.error(request, 'An error occurred.')
        return redirect('notifications')


@login_required
def get_notifications(request):
    try:
        notifications_list = Notification.objects.filter(user=request.user)[:5]
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        data = [{
            'id': n.id,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%b %d, %H:%M'),
            'unread_count': unread_count
        } for n in notifications_list]
        return JsonResponse({'notifications': data})
    except Exception as e:
        logger.error(f"Error getting notifications: {str(e)}")
        return JsonResponse({'notifications': [], 'error': str(e)}, status=500)