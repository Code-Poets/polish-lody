from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Employee

class EmployeeList(LoginRequiredMixin, ListView):
    tmplate_name = 'employees/employee_list.html'
    context_object_name = 'all_employee_list'

    def get_queryset(self):
        return Employee.objects.order_by('first_name')

class EmployeeDetail(LoginRequiredMixin, DetailView):
    model = Employee
    tmplate_name = 'employees/employee_detail.html'

    def get_context_data(self, **kwargs):
        #Overriding this method to use another model within the template
        context = super(EmployeeDetail, self).get_context_data(**kwargs)
        employee_object = self.get_object()
        context['months'] = employee_object.month_set.all()
        return context


class EmployeeCreate(LoginRequiredMixin, CreateView):

    model = Employee
    success_url = reverse_lazy('employees')
    fields = ['first_name',
              'last_name',
              'email',
              'gender',
              'rate_per_hour',
              'contract_start_date',
              'contract_exp_date',
              'health_book_exp_date',
              'position',
              'contract_type',
              'hours_in_current_month']


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    success_url = reverse_lazy('employees')
    fields = ['first_name',
              'last_name',
              'email',
              'gender',
              'rate_per_hour',
              'contract_start_date',
              'contract_exp_date',
              'health_book_exp_date',
              'position',
              'contract_type',
              'hours_in_current_month']

class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employees')