# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Employee, Month

from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UserChangeForm as AuthUserChangeForm
from django import forms
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string

class EmployeeCreateAdminForm(AuthUserCreationForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeCreateAdminForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(EmployeeCreateAdminForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

    class Meta:
        model = Employee
        fields = ["email"]

class EmployeeChangeAdminForm(AuthUserChangeForm):

    class Meta:
        model = Employee
        fields = ["email"]

class EmployeeAdmin(AuthUserAdmin):
    fieldsets = (
        ('User', {'fields': ('email','password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Employee info', {'fields': ('rate_per_hour', 'contract_start_date', 'contract_exp_date',
         'health_book_exp_date', 'gender', 'position', 'contract_type')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email','password1', 'password2',)}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Employee info', {'fields': ('rate_per_hour', 'contract_start_date', 'contract_exp_date',
         'health_book_exp_date', 'gender', 'position', 'contract_type')}),
    )
    form = EmployeeChangeAdminForm
    add_form = EmployeeCreateAdminForm
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ()
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

        super(EmployeeAdmin, self).save_model(request, obj, form, change)

        if reset_password:
            reset_form = PasswordResetForm({'email': obj.email})
            assert reset_form.is_valid()
            reset_form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_set_email.html',
            )

admin.site.register(Employee, EmployeeAdmin)



def make_month_paid(modeladmin, request, queryset):
    queryset.update(salary_is_paid=True)

def make_month_unpaid(modeladmin, request, queryset):
    queryset.update(salary_is_paid=False)


make_month_unpaid.short_description = "Mark selected months as unpaid"
make_month_paid.short_description = "Mark selected months as paid"

class MonthAdmin(admin.ModelAdmin):
    actions = [make_month_paid, make_month_unpaid]

admin.site.register(Month, MonthAdmin)

