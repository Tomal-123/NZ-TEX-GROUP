from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'name', 'department', 'designation', 'mobile', 'email')
    search_fields = ('name', 'company_name', 'department', 'email')
    list_filter = ('company_name', 'department')