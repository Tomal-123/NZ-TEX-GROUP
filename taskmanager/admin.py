from django.contrib import admin
from django import forms
from .models import Contact, Module, Permission, Role, UserRole

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'name', 'department', 'designation', 'mobile', 'email')
    search_fields = ('name', 'company_name', 'department', 'email')
    list_filter = ('company_name', 'department')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('module', 'actions')
    list_filter = ('module',)
    search_fields = ('module__name',)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'actions':
            kwargs['widget'] = forms.CheckboxSelectMultiple(choices=[('view', 'View'), ('create', 'Create'), ('edit', 'Edit'), ('delete', 'Delete')])
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)
    filter_horizontal = ('permissions',)





@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('user__username', 'role__name')