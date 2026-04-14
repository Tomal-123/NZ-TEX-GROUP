from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from taskmanager.views import home, register, create_task, task_list, update_task_status, add_comment, contact, approve_task, delete_task, edit_task, notifications, create_notification, mark_notification_read, delete_notification, get_notifications, dashboard, profile, organogram, erp_service, team, get_contacts

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('organogram/', organogram, name='organogram'),
    path('team/', team, name='team'),
    path('erp/', erp_service, name='erp_service'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/<int:task_id>/status/', update_task_status, name='update_task_status'),
    path('tasks/<int:task_id>/comment/', add_comment, name='add_comment'),
    path('tasks/<int:task_id>/approve/', approve_task, name='approve_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('tasks/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('contact/', contact, name='contact'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/create/', create_notification, name='create_notification'),
    path('notifications/<int:notif_id>/read/', mark_notification_read, name='mark_notification_read'),
    path('notifications/<int:notif_id>/delete/', delete_notification, name='delete_notification'),
    path('api/notifications/', get_notifications, name='get_notifications'),
    path('api/contacts/', get_contacts, name='get_contacts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)