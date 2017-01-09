# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
import time
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .forms import EmployeeForm, EmployeeChangeForm, MonthForm
from .models import Employee, Month
from .mixins import OwnershipMixin
import random
from  django.db.models import Case, When, Sum, Value, F, Q, DecimalField

def make_year_list_for_filtering_in_emp_detail(employee):
    months = employee.month_set.all()
    years = []
    for month in months:
        if not month.year in years:
            years.append(month.year)
    sorted_years = sorted(years)
    return sorted_years

def make_employee_list_view_order_form_options():
    options = [
        ('id', 'Oldest first'),
        ('-id', 'Newest first'),
        ("contract_start_date", "Contract start date ascending"),
        ("-contract_start_date", "Contract start date descending"),
        ("rate_per_hour", "Rate per hour ascending"),
        ("-rate_per_hour", "Rate per hour descending"),
        ("health_book_exp_date", "Health book expiration date ascending"),
        ("-health_book_exp_date", "Health book expiration date descending"),
        ("contract_exp_date", "Contract expiration date ascending"),
        ("-contract_exp_date", "Contract expiration date descending"),
        ("unpaid_salaries", "Total unpaid salaries ascending"),
        ("-unpaid_salaries", "Total unpaid salaries descending"),
    ]
    return options

def make_employee_detail_view_order_form_options():
    options = [
       ('oldest','Oldest first'),
       ('newest', 'Newest first'),
       ("hours_worked_in_this_month","Hours worked ascending"),
       ("-hours_worked_in_this_month","Hours worked descending"),
       ("rate_per_hour_this_month","Rate per hour ascending"),
       ("-rate_per_hour_this_month","Rate per hour descending"),
       ("to_be_paid", "To be paid ascending"),
       ("-to_be_paid", "To be paid descending"),
    ]
    return options
>>>>>>> added new features in views.py

def make_paginate_by_list():
    paginate_by = [2, 5, 10, 25, 100]
    return paginate_by

<<<<<<< a0ef3ef15bf4ea7f06412f59d95bcf417cb1d5c2
def order_by_unpaid_salaries(descending):
    employees = Employee.objects.all()
    employees_dict = {}
    for emp in employees:
        emp_salary_value = emp.all_unpaid_salaries_for_sorting()
        if emp_salary_value is not None:
            employees_dict[emp] = emp_salary_value
        else:
            employees_dict[emp] = -1
    sorted_by_unpaid_salaries_list = sorted(employees_dict.items(), reverse=descending,
                                            key=lambda x: x[1])
    new_emp_list = []
    for employee, value in sorted_by_unpaid_salaries_list:
        new_emp_list.append(employee)
    return new_emp_list
class EmployeeList(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
=======
def find_user_by_name(query_name):
   qs = Employee.objects.all()
   for term in query_name.split():
        qs = qs.filter( Q(first_name__contains = term) | Q(last_name__contains = term))
   return qs

def order_by_default(order):
    try:
        queryset = Employee.objects.all().order_by(order)
    except:
        queryset = Employee.objects.all()
    return queryset

def order_by_unpaid_salaries(name_filter, descending):
    if name_filter is not None:
        employees = find_user_by_name(name_filter)
    else:
        employees = Employee.objects.all()

    query = employees.annotate(
        unpaid_salaries=Sum(
            Case(
                When(
                    month=None,
                    then=-1
                ),
                When(
                    month__salary_is_paid=False,
                    then=(F('month__rate_per_hour_this_month') * F('month__hours_worked_in_this_month')),
                ),
                default=0,
                output_field=DecimalField(),
            )
        )
    ).order_by('%sunpaid_salaries' % (descending))
    return query


class EmployeeList(LoginRequiredMixin, ListView):
    template_name = 'employees/employee_list.html'
    context_object_name = 'all_employee_list'
    def get_paginate_by(self, queryset):
        try:
            per_page = self.request.GET.get('per_page') or self.kwargs.get('per_page') or 10
        except:
            per_page = 10
        return per_page

    def get_context_data(self, **kwargs):
        context = super(EmployeeList, self).get_context_data(**kwargs)
        employee_list = context['all_employee_list']
        paginator = Paginator(employee_list, self.get_paginate_by(employee_list))
        page = self.request.GET.get('page')
        pg = self.get_paginate_by(employee_list)
        if pg is not None:
            context['current_paginate_by_number'] = int(pg)
        try:
            employee_pages = paginator.page(page)
        except PageNotAnInteger:
            employee_pages = paginator.page(1)
        except EmptyPage:
            employee_pages = paginator.page(paginator.num_pages)
        context['paginate_by_numbers'] = make_paginate_by_list()
        context['employee_list'] = employee_pages
        context['orderby'] = self.request.GET.get('orderby', 'last_name')
        context['position_filter'] = self.request.GET.get('position_filter')
        context['employee_filter'] = self.request.GET.get('employee_filter') or 'Search for employee...'
        context['sorting_options'] = make_employee_list_view_order_form_options()
        context['hide_zero_salary_months'] = self.request.GET.get('hide_zero_salary_months') or False
        return context

    def get_queryset(self):
        clear_filters = self.request.GET.get('clear_filters')
        order = self.request.GET.get('orderby', 'last_name')
        employee_filter = self.request.GET.get('employee_filter') or None
        position_filter = self.request.GET.get('position_filter') or None
        hide_zero_salary_months_filter = self.request.GET.get('hide_zero_salary_months') or None
        if clear_filters is None:
            if order == 'unpaid_salaries':
                queryset = order_by_unpaid_salaries(employee_filter, '')
            elif order == '-unpaid_salaries':
                queryset = order_by_unpaid_salaries(employee_filter, '-')
            elif not 'unpaid' in order and employee_filter is not None:
                filtered_queryset = find_user_by_name(employee_filter)
                queryset = filtered_queryset.order_by(order)
            else:
                queryset = order_by_default(order)
            if position_filter is not None:
                queryset = queryset.filter(position=position_filter)
            if hide_zero_salary_months_filter is not None:
                exclude_list = []
                for employee in queryset:
                    if employee.all_unpaid_salaries() == 0 or employee.all_unpaid_salaries() is None:
                        exclude_list.append(employee.id)
                queryset = queryset.exclude(id__in=exclude_list)
            if queryset.count() == 0:
                messages.add_message(self.request, messages.WARNING,
                                     "No employee meets the search criteria. Widen your search or check filter for typos.")
        else:
            order = self.request.GET.get('orderby', 'last_name')
            queryset = order_by_default(order)
        return queryset

class EmployeeDetail(LoginRequiredMixin, OwnershipMixin, DetailView):
    model = Month
    template_name = 'employees/employee_detail.html'
    def get_paginate_by(self, queryset):
        try:
            per_page = self.request.GET.get('per_page') or self.kwargs.get('per_page') or 10
        except:
            per_page = 10
        return per_page
    def get_queryset(self):
        employee = Employee.objects.get(pk=self.kwargs.get('pk'))
        order = self.request.GET.get('orderby', )#('-year', '-month'))
        hide_paid_filter = self.request.GET.get('hide_paid_months_filter')
        hide_unpaid_filter = self.request.GET.get('hide_unpaid_months_filter')
        clear_filters = self.request.GET.get('clear_filters')
        year_filter = self.request.GET.get('select_year')
        if clear_filters is None:

            if order == 'newest':
                month_queryset = employee.month_set.all().order_by('-year', '-month')

            elif order == 'oldest':
                month_queryset = employee.month_set.all().order_by('year', 'month')

            elif order == 'to_be_paid':
                month_queryset = employee.month_set.annotate(
                    to_be_paid=(F('hours_worked_in_this_month')*F('rate_per_hour_this_month'))
                ).order_by('to_be_paid')
            elif order == '-to_be_paid':
                month_queryset = employee.month_set.annotate(
                    to_be_paid=(F('hours_worked_in_this_month')*F('rate_per_hour_this_month'))
                ).order_by('-to_be_paid')

            else:
                try:
                    month_queryset = employee.month_set.all().order_by(order)
                except:
                    month_queryset = employee.month_set.all().order_by('-year', '-month')
            if year_filter is not None:
                years = make_year_list_for_filtering_in_emp_detail(employee)
                years.remove(int(year_filter))
                month_queryset = month_queryset.exclude(year__in=years)
            if hide_paid_filter is not None:
                month_queryset = month_queryset.exclude(salary_is_paid=True)
            if hide_unpaid_filter is not None:
                month_queryset = month_queryset.exclude(salary_is_paid=False)

            if month_queryset.count() == 0:
                messages.add_message(self.request, messages.WARNING,
                                     "Employee has no months which satisfy specified criteria. Check filters again.")
        else:
            try:
                month_queryset = employee.month_set.all().order_by(order)
            except:
                month_queryset = employee.month_set.all().order_by('-year', '-month')
        return month_queryset

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetail, self).get_context_data(**kwargs)
        month_list = context['object_list']
        context['employee'] = Employee.objects.get(pk=self.kwargs.get('pk'))
        paginator = Paginator(month_list, self.get_paginate_by(month_list))
        page = self.request.GET.get('page')
        pg = self.get_paginate_by(month_list)
        if pg is not None:
            context['current_paginate_by_number'] = int(pg)
        try:
            month_pages = paginator.page(page)
        except PageNotAnInteger:
            month_pages = paginator.page(1)
        except EmptyPage:
            month_pages = paginator.page(paginator.num_pages)
        context['paginate_by_numbers'] = make_paginate_by_list()
        context['months'] = month_pages
        context['month_sorting_options'] = make_employee_detail_view_order_form_options()
        context['years'] = make_year_list_for_filtering_in_emp_detail(context['employee'])
        try:
            context['select_year'] = int(self.request.GET.get('select_year'))
        except:
            pass
        context['hide_paid_months_filter'] = self.request.GET.get('hide_paid_months_filter') or False
        context['hide_unpaid_months_filter'] = self.request.GET.get('hide_unpaid_months_filter') or False
        context['orderby'] = self.request.GET.get('orderby')
        return context

class EmployeeCreate(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employees')
    template_name = 'employees/employee_form.html'

    def form_valid(self, form, **kwargs):
        self.object = form.save(commit=False)
        try:
            form_validation = super(EmployeeCreate, self).form_valid(form)
            messages.add_message(self.request, messages.SUCCESS,
                                 "Successfully created employee %s" % self.object.full_name())
            return form_validation
        except:
            if "already exists" in str(form.errors):
                messages.add_message(self.request, messages.ERROR,
                                     "Specified e-mail address has already been assigned to another employee")
            return HttpResponseRedirect('')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class EmployeeUpdate(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):

    model = Employee
    form_class = EmployeeChangeForm
    success_url = reverse_lazy('employees')
    template_name = 'employees/employee_form.html'

    def get_queryset(self, **kwargs):
        try:
            return Employee.objects.filter(pk=self.kwargs['pk'])
        except:
            messages.add_message(self.request, messages.ERROR, "This employee does not exist!")
            return HttpResponseRedirect('../')

class MonthCreate(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):

    form_class = MonthForm
    success_url = reverse_lazy('employee_detail')
    template_name = 'employees/month_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('employee_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        self.employee_object = Employee.objects.get(pk=self.kwargs['pk'])
        context = super(MonthCreate, self).get_context_data(**kwargs)
        context['employee'] = self.employee_object
        return context

    def get_initial(self):
        initial = super(MonthCreate, self).get_initial()
        initial = initial.copy()
        employee_object = Employee.objects.get(pk=self.kwargs['pk'])
        initial['rate_per_hour_this_month'] = employee_object.rate_per_hour
        initial['employee'] = employee_object
        return initial

    def form_valid(self, form, **kwargs):
        employee_object = Employee.objects.get(pk=self.kwargs['pk'])
        form.employee = employee_object.full_name()
        self.object = form.save(commit=False)
        try:
            form_validation = super(MonthCreate, self).form_valid(form)
            messages.add_message(self.request, messages.SUCCESS,
                                 "Successfully created month %s in year %s" %
                                 (self.object.month_name(), self.object.year))
            return form_validation
        except:
            if "already exists" in str(form.errors):
                messages.add_message(self.request, messages.ERROR,
                                     "Specified month has already been assigned to employee %s." %
                                     (employee_object.full_name()))
            return HttpResponseRedirect('')

    def form_invalid(self, form, **kwargs):
        employee_object = Employee.objects.get(pk=self.kwargs['pk'])
        if "already exists" in str(form.errors):
            messages.add_message(self.request, messages.ERROR,
                                 "Specified month has already been assigned to employee %s." %
                                 (employee_object.full_name()))
        return HttpResponseRedirect('')

class MonthUpdate(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):

    form_class = MonthForm
    success_url = reverse_lazy('employee_detail')
    template_name = 'employees/month_edit_form.html'

    def get_queryset(self, **kwargs):
        try:
            return Month.objects.filter(pk=self.kwargs['pk'])
        except:
            messages.add_message(self.request, messages.ERROR, "This month does not exist!")
            return HttpResponseRedirect('../')

    def get_success_url(self, **kwargs):
        try:
            employee_object = self.get_object().employee
            redirector = employee_object.pk
            return reverse_lazy('employee_detail', kwargs={'pk': redirector})
        except:
            return '../'

    def get_context_data(self, **kwargs):
        try:
            context = super(MonthUpdate, self).get_context_data(**kwargs)
            employee_object = self.get_object().employee
            context['employee'] = employee_object
            return context
        except:
            messages.add_message(self.request, messages.ERROR, "This month does not exist!")
            return HttpResponseRedirect('../')

    def form_valid(self, form):
        form_validation = super(MonthUpdate, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS,
                             "Successfully edited month %s in year %s." %
                             (self.object.month_name(), self.object.year))
        return form_validation

    def form_invalid(self, form, **kwargs):
        employee_object = self.get_object().employee
        if "already exists" in str(form.errors):
            messages.add_message(self.request, messages.ERROR,
                                 "Specified month has already been assigned to employee %s." %
                                 (employee_object.full_name()))
        return HttpResponseRedirect('')

class EmployeeDelete(LoginRequiredMixin, StaffuserRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employees')

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.add_message(self.request, messages.WARNING,
                                 "Successfully deleted employee %s." % self.object.full_name())
        except:
            messages.add_message(self.request, messages.ERROR, "This employee does not exist!")

        return HttpResponseRedirect(self.success_url)

class MonthDelete(LoginRequiredMixin, StaffuserRequiredMixin, DeleteView):
    model = Month

    def get_success_url(self, **kwargs):
        try:
            employee_object = self.get_object().employee
            redirector = employee_object.pk
            return reverse_lazy('employee_detail', kwargs={'pk': redirector})
        except AttributeError:
            return '../'

    def get_object(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            obj = queryset.get()
            return obj
        except queryset.model.DoesNotExist:
            return AttributeError("")

    def get_context_data(self, **kwargs):
        context = super(MonthDelete, self).get_context_data(**kwargs)
        try:
            employee_object = self.get_object().employee
            context['employee'] = employee_object
            return context
        except AttributeError:
            return context

    def delete(self, request, *args, **kwargs):
        try:
            if not self.get_object() is None:
                self.object = self.get_object()
                success_url = self.get_success_url()
                self.object.delete()
                messages.add_message(self.request, messages.WARNING, "Successfully deleted month %s." % self.object.month_name())
                return HttpResponseRedirect(success_url)
            else:
                messages.add_message(self.request, messages.ERROR, "This month does not exist!")
                return HttpResponseRedirect(self.get_success_url(**kwargs))
        except AttributeError:
            messages.add_message(self.request, messages.ERROR, "This month does not exist!")
            return HttpResponseRedirect(self.get_success_url())

def pl_404_view(request):
    template = 'employees/404.html'
    response = render(request, template)
    response.status_code = 404
    return response

def pl_500_view(request):
    template = 'employees/500.html'
    response = render(request, template)
    response.status_code = 500
    return response
