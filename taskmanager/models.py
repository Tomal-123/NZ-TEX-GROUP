from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


class Contact(models.Model):
    company_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    ip_phone = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.company_name}"


class InventoryItem(models.Model):
    DEPARTMENT_CHOICES = [
        ('computer_accessories', 'Computer Accessories'),
        ('printer_and_scanner', 'Printer and Scanner'),
        ('others_it_product', "Other's IT Product"),
    ]
    
    CATEGORY_CHOICES = [
        ('desktop', 'Desktop'),
        ('monitor', 'Monitor'),
        ('laptop', 'Laptop'),
        ('mouse', 'Mouse'),
        ('wireless_mouse', 'Wireless Mouse'),
        ('keyboard', 'Keyboard'),
        ('ups', 'UPS'),
        ('general_printer', 'General Printer'),
        ('color_printer', 'Color Printer'),
        ('dot_printer', 'Dot Printer'),
        ('sticker_printer', 'Sticker Printer'),
        ('scanner', 'Scanner'),
        ('photocopy_machine', 'Photocopy Machine'),
        ('enroll_scanner', 'Enroll Scanner'),
        ('ip_phone', 'IP Phone'),
        ('switch_8port', '8 Port Switch'),
        ('switch_24port', '24 Port Switch'),
        ('mc', 'MC'),
        ('tj_box', 'TJ Box'),
        ('nvr', 'NVR'),
        ('ip_camera', 'IP Camera'),
        ('pendrive', 'Pendrive'),
        ('usb_hub', 'USB Hub'),
        ('eth_adapter', 'Eth. Adapter'),
        ('tv', 'TV'),
        ('wifi', 'Wifi'),
        ('virdi_device', 'Virdi Device'),
        ('network_booster', 'Network Booster'),
        ('projector', 'Projector'),
        ('wallstand_screen', 'Wall Stand and Screen'),
    ]
    
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='computer_accessories')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_department_display()} - {self.get_category_display()} - {self.quantity}"

    class Meta:
        verbose_name_plural = "Inventory Items"