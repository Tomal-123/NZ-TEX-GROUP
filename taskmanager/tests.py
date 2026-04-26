from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from taskmanager.models import (
    Task, Category, Comment, Notification, Contact,
    Department, AssetCategory, InventoryNew, ShedInventory
)
import json


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.category = Category.objects.create(name='Test Category', color='#FF0000')


class TaskModelTest(BaseTestCase):
    def test_task_creation(self):
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='pending',
            priority='high',
            created_by=self.user
        )
        self.assertEqual(str(task), 'Test Task')
        self.assertEqual(task.status, 'pending')
        self.assertEqual(task.priority, 'high')

    def test_task_assignment(self):
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user
        )
        task.assigned_to.add(self.user)
        self.assertIn(self.user, task.assigned_to.all())


class CategoryModelTest(BaseTestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='Work', color='#00FF00')
        self.assertEqual(str(category), 'Work')
        self.assertEqual(category.color, '#00FF00')


class TaskViewsTest(BaseTestCase):
    def test_home_view_requires_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_home_view_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_task_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        Task.objects.create(title='Task 1', created_by=self.user)
        Task.objects.create(title='Task 2', created_by=self.user)
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('All Tasks', response.content.decode())

    def test_create_task_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)

    def test_create_task_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('create_task'), {
            'title': 'New Task',
            'description': 'Task Description',
            'status': 'pending',
            'priority': 'medium',
        })
        self.assertEqual(Task.objects.filter(title='New Task').count(), 1)

    def test_update_task_status(self):
        self.client.login(username='testuser', password='testpass123')
        task = Task.objects.create(title='Task', created_by=self.user)
        response = self.client.post(
            reverse('update_task_status', args=[task.id]),
            {'status': 'completed'}
        )
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, 'completed')

    def test_delete_task(self):
        self.client.login(username='testuser', password='testpass123')
        task = Task.objects.create(title='Task to Delete', created_by=self.user)
        response = self.client.post(reverse('delete_task', args=[task.id]))
        self.assertFalse(Task.objects.filter(id=task.id).exists())


class CommentTest(BaseTestCase):
    def test_add_comment(self):
        self.client.login(username='testuser', password='testpass123')
        task = Task.objects.create(title='Task', created_by=self.user)
        response = self.client.post(
            reverse('add_comment', args=[task.id]),
            {'text': 'Test comment'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)


class NotificationTest(BaseTestCase):
    def test_notifications_view(self):
        self.client.login(username='testuser', password='testpass123')
        Notification.objects.create(user=self.user, message='Test notification')
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test notification')

    def test_create_notification(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('create_notification'), {
            'message': 'New notification'
        })
        self.assertEqual(Notification.objects.count(), 1)


class ContactTest(BaseTestCase):
    def test_contact_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        Contact.objects.create(
            company_name='Test Co',
            name='John Doe',
            department='IT',
            designation='Developer'
        )
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Co')

    def test_contact_api(self):
        self.client.login(username='testuser', password='testpass123')
        Contact.objects.create(
            company_name='Test Co',
            name='John Doe',
            department='IT',
            designation='Developer'
        )
        response = self.client.get(reverse('get_contacts'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['contacts']), 1)


class InventoryTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.department = Department.objects.create(name='IT', code='IT')
        self.asset_category = AssetCategory.objects.create(
            name='Computer', code='COMP', unit='pcs'
        )

    def test_inventory_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 200)

    def test_inventory_smart_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('inventory_shed1'))
        self.assertEqual(response.status_code, 200)

    def test_api_inventory_list(self):
        self.client.login(username='testuser', password='testpass123')
        InventoryNew.objects.create(
            department=self.department,
            asset_category=self.asset_category,
            quantity=10,
            shed_name='shed1'
        )
        response = self.client.get(reverse('api_inventory_list') + '?shed=shed1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['inventory']), 1)


class AuthTest(BaseTestCase):
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class ProfileTest(BaseTestCase):
    def test_profile_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')


class ExportTest(BaseTestCase):
    def test_export_tasks_csv(self):
        self.client.login(username='testuser', password='testpass123')
        Task.objects.create(title='Task 1', created_by=self.user)
        response = self.client.get(reverse('export_tasks_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')


class RBACPermissionTest(BaseTestCase):
    def test_is_admin_function(self):
        from taskmanager.utils.permissions import is_admin
        self.assertFalse(is_admin(self.user))
        self.assertTrue(is_admin(self.admin_user))

    def test_staff_member(self):
        from taskmanager.utils.permissions import is_staff_member
        self.user.is_staff = True
        self.user.save()
        self.assertTrue(is_staff_member(self.user))


class PaginationTest(BaseTestCase):
    def test_task_list_pagination(self):
        self.client.login(username='testuser', password='testpass123')
        for i in range(20):
            Task.objects.create(title=f'Task {i}', created_by=self.user)
        
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)


class ModelChoicesTest(BaseTestCase):
    def test_task_status_choices(self):
        task = Task.objects.create(
            title='Test',
            status='pending',
            created_by=self.user
        )
        self.assertEqual(task.get_status_display(), 'Pending')

    def test_task_priority_choices(self):
        task = Task.objects.create(
            title='Test',
            priority='high',
            created_by=self.user
        )
        self.assertEqual(task.get_priority_display(), 'High')