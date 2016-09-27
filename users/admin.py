from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import (
    password_validation,
)
from django.contrib.auth import forms as user_forms

from users.models import MyUser


class UserCreationForm(user_forms.UserCreationForm):
    """
    A form that creates a user
    """
    class Meta:
        model = MyUser
        fields = ("email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.email = self.cleaned_data.get('email')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2



class UserChangeForm(user_forms.UserChangeForm):
    class Meta:
        model = MyUser
        fields = ("email",)



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('id',)
    fieldsets = (
        ('Email', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    filter_horizontal = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

admin.site.register(MyUser, UserAdmin)