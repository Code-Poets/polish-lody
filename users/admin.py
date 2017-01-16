from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
 
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

    def save_model(self, request, obj, form, change):
        if not change and (not form.cleaned_data['password1'] or not obj.has_usable_password()):
            # Django's PasswordResetForm won't let us reset an unusable
            # password. We set it above super() so we don't have to save twice.
            obj.set_password(get_random_string())
            reset_password = True
        else:
            reset_password = False

        super(UserAdmin, self).save_model(request, obj, form, change)

        if reset_password:
            reset_form = PasswordResetForm({'email': obj.email})
            assert reset_form.is_valid()
            reset_form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_set_email.html',
            )

admin.site.register(MyUser, UserAdmin)