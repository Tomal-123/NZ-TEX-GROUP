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


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20, default='pcs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class InventoryNew(models.Model):
    SHED_CHOICES = [
        ('shed1', 'NZ Apparels Shed-1'),
        ('shed2', 'NZ Apparels Shed-2'),
        ('shed3', 'NZ Apparels Shed-3'),
        ('it_stock', 'IT Stock Product'),
        ('all_it', 'All IT Product Inventory'),
        ('it_department', 'IT Department'),
    ]
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='inventories')
    asset_category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.IntegerField(default=0)
    shed_name = models.CharField(max_length=50, choices=SHED_CHOICES, default='shed1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.department.name} - {self.asset_category.name} - {self.quantity}"

    class Meta:
        unique_together = ['department', 'asset_category', 'shed_name']
        verbose_name_plural = "Inventory Records"


class ShedInventory(models.Model):
    SHED_CHOICES = [
        ('shed1', 'NZ Apparels Shed-1'),
        ('shed2', 'NZ Apparels Shed-2'),
        ('shed3', 'NZ Apparels Shed-3'),
        ('it_stock', 'IT Stock Product'),
        ('all_it', 'All IT Product Inventory'),
        ('it_department', 'IT Department'),
    ]
    
    shed_name = models.CharField(max_length=50, unique=True)
    row_labels = models.JSONField(default=list)
    column_labels = models.JSONField(default=list)
    data = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        display_name = dict(SHED_CHOICES).get(self.shed_name, self.shed_name.replace('_', ' ').title())
        return f"{display_name} Inventory"


class InventoryAuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
    ]
    
    department = models.CharField(max_length=100)
    asset_category = models.CharField(max_length=100)
    old_quantity = models.IntegerField(default=0)
    new_quantity = models.IntegerField(default=0)
    shed_name = models.CharField(max_length=50)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.department} - {self.asset_category}: {self.old_quantity} -> {self.new_quantity}"


class Module(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Permission(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='permissions')
    actions = models.CharField(max_length=100, blank=True, help_text="Comma separated actions: view,create,edit,delete")
    
    def __str__(self):
        return f"{self.module.name} - {self.actions or 'None'}"
    
    def get_actions_list(self):
        """Return actions as a list."""
        if not self.actions:
            return []
        return [action.strip() for action in self.actions.split(',')]
    
    def has_action(self, action):
        """Check if permission has a specific action."""
        return action in self.get_actions_list()


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, related_name='roles', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

    class Meta:
        unique_together = ['user', 'role']