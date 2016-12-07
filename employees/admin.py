from django.contrib import admin
from .models import Employee, Month, Year

def make_month_paid(modeladmin, request, queryset):
    queryset.update(salary_is_paid=True)

def make_month_unpaid(modeladmin, request, queryset):
    queryset.update(salary_is_paid=False)


make_month_unpaid.short_description = "Mark selected months as unpaid"
make_month_paid.short_description = "Mark selected months as paid"

class MonthAdmin(admin.ModelAdmin):
    actions = [make_month_paid, make_month_unpaid]

admin.site.register(Employee)
admin.site.register(Month, MonthAdmin)
admin.site.register(Year)

