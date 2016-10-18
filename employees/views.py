from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Employee

class EmployeeList(ListView):
    tmplate_name = 'employees/employee_list.html'
    context_object_name = 'all_employee_list'

    def get_queryset(self):
        return Employee.objects.order_by('first_name')

class EmployeeDetail(DetailView):
    model = Employee
    tmplate_name = 'employees/employee_detail.html'

class EmployeeCreate(CreateView):
    model = Employee
    success_url = reverse_lazy('employees')
    fields = ['first_name', 'last_name', 'email', 'rate_per_hour', 'contract_exp_date', 'health_book_exp_date']

class EmployeeUpdate(UpdateView):
    model = Employee
    success_url = reverse_lazy('employees')
    fields = ['first_name', 'last_name', 'email', 'rate_per_hour', 'contract_exp_date', 'health_book_exp_date']

class EmployeeDelete(DeleteView):
    model = Employee
    success_url = reverse_lazy('employees')