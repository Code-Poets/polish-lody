# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Employee, Month

from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UserChangeForm as AuthUserChangeForm
from django import forms
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

class EmployeeCreationForm(AuthUserCreationForm):

    class Meta:
        model = Employee
        fields = ["email"]

class EmployeeChangeForm(AuthUserChangeForm):

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
    form = EmployeeChangeForm
    add_form = EmployeeCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ()
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('last_name','first_name',)



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

