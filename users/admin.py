from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
 
from users.models import MyUser
from users.forms import UserCreationForm, UserChangeForm
 
class UserAdmin(AuthUserAdmin):
    fieldsets = (
        ('User', {'fields': ('email','password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                        'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email','password1', 'password2',)}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('last_name','first_name',)

admin.site.register(MyUser, UserAdmin)