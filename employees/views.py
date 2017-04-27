# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
#from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
import time
import json
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
from .forms import EmployeeForm, EmployeeChangeForm, MonthForm, MonthApproveForm
from .models import City, Employee, Month
from .mixins import MonthOwnershipMixin, OwnershipMixin, StaffRequiredMixin
from  django.db.models import Case, When, Sum, Value, F, Q, DecimalField
import re
from django.db import IntegrityError
from polishlody.settings import WARNING_DAYS_LEFT, FORM_SUBMIT_DELAY
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from functools import reduce

def ajax_autocomplete(request):
    if request.is_ajax():
        query = request.GET.get('query', '')
        polishquery = query
        polishqueryarr = []
        for word, initial in {'A':'Ą','C':'Ć','E':'Ę','L':'Ł','N':'Ń','O':'Ó','S':'Ś','Z':'Ź','Z':'Ż',
            'a':'ą','c':'ć','e':'ę','l':'ł','n':'ń','o':'ó','s':'ś','z':'ź','z':'ż'}.items():
            polishquery = query
            polishquery = polishquery.replace(word,initial)
            polishqueryarr.append(polishquery)
        for word, initial in {'A':'Ą','C':'Ć','E':'Ę','L':'Ł','N':'Ń','O':'Ó','S':'Ś','Z':'Ź','Z':'Ż',
            'a':'ą','c':'ć','e':'ę','l':'ł','n':'ń','o':'ó','s':'ś','z':'ź','z':'ż'}.items():
            polishquery = polishquery.replace(word,initial)
            polishqueryarr.append(polishquery)
        data = json.dumps({

            "suggestions" :
            
            [city.name for city in City.objects.filter(
                Q(name__icontains = query)|reduce(lambda x, y: x | y, [Q(name__contains=word) for word in polishqueryarr]))]
            
            })
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def ajax_verify_email(request):
    if request.POST and request.is_ajax():
        email = request.POST.get('email')
        if Employee.objects.filter(email=email).exists():
            return HttpResponse(json.dumps({
                "status":1
                }), content_type='application/json')
        return HttpResponse('')
    return HttpResponse('')

def ajax_verify_date(request, **kwargs):
    year = request.GET.get('year')
    month = request.GET.get('month')
    empid = request.GET.get('employee_id')
    emp = Employee.objects.get(id=int(empid))
    employee_month_query = emp.month_set.all()
    data = {
        'is_date': employee_month_query.filter(month=month, year=year).exists()
    }
    return JsonResponse(data)

def make_year_list_for_filtering_in_emp_detail(employee):
    months = employee.month_set.all()
    years = []
    for month in months:
        if not month.year in years:
            years.append(month.year)
    sorted_years = sorted(years)
    if len(years) != 0:
        return sorted_years[::-1]
    else:
        return False

def position_list_and_filtering(self, queryset):
    positions = {
        'position_sale': 'Sale',
        'position_production': 'Production',
        'position_other': 'Other',
        'position_none': 'None',
    }
    exclude_list = []
    for key in positions.keys():
        if self.request.GET.get(key) is None:
            exclude_list.append(positions[key])
            queryset = queryset.exclude(position=positions[key])
    queryset = queryset.exclude(position=None)
    return queryset

def make_paginate_by_list():
    paginate_by = [2, 5, 10, 25, 100]
    return paginate_by

def find_user_by_name(query_name):
    qs = Employee.objects.all()
    for term in query_name.split():
        qs = qs.filter( Q(first_name__icontains = term) | Q(last_name__icontains = term)
                        | Q(first_name__icontains = term.title()) | Q(last_name__icontains = term.title()))
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

class EmployeeList(LoginRequiredMixin, StaffRequiredMixin, ListView):
    
    template_name = 'employees/employee_list.html'
    context_object_name = 'all_employee_list'

    def get_template_names(self, **kwargs):
        if self.request.is_ajax():
            names = ['employees/employee_list_table.html']
        else:
            names = ['employees/employee_list.html']
        return names

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            qset = context['all_employee_list']
            order = context['orderby']
            try:
                page_obj = context['page_obj']
                paginator = context['paginator']
            except:
                pass
            context = {
                'all_employee_list':qset,
                'paginator': paginator,
                'page_obj': page_obj,
                'orderby': order,
            }
            context['warning_x_days_left'] = WARNING_DAYS_LEFT
            if qset.count() == 0:
                context['empty_qset'] = True
            context['ajax_request'] = True
            return self.response_class(
                request = self.request,
                template = self.get_template_names(),
                context = context,
                **response_kwargs
            )
        else:
            response = super().render_to_response(context, **response_kwargs)
            return super().render_to_response(context, **response_kwargs)

    def get_paginate_by(self, queryset):
        try:
            per_page = self.request.GET.get('per_page') or self.kwargs.get('per_page') or 10
        except:
            per_page = 10
        return per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        context['orderby'] = self.request.GET.get('order', 'last_name')
        context['position_filter'] = self.request.GET.get('position_filter')
        context['employee_filter'] = self.request.GET.get('employee_filter') or _('e.g. Darth Vader')
        context['hide_zero_salary_months'] = self.request.GET.get('hide_zero_salary_months') or False
        context['hide_paid_employees_filter'] = self.request.GET.get('hide_paid_employees_filter') or False
        context['per_page'] = self.request.GET.get('per_page') or 10
        context['page'] = page
        context['warning_x_days_left'] = WARNING_DAYS_LEFT
        context['position_sale'] = self.request.GET.get('position_sale') or False
        context['position_production'] = self.request.GET.get('position_production') or False
        context['position_other'] = self.request.GET.get('position_other') or False
        context['form_submit_delay'] = FORM_SUBMIT_DELAY
        return context

    def get_queryset(self):
        clear_filters = self.request.GET.get('clear_filters')
        order = self.request.GET.get('order', 'last_name')
        sale_position_filter = self.request.GET.get('position_sale') or False
        production_position_filter = self.request.GET.get('position_production') or False
        other_position_filter = self.request.GET.get('position_other') or False
        employee_filter = self.request.GET.get('employee_filter')
        position_filter = self.request.GET.get('position_filter')
        hide_zero_salary_months_filter = self.request.GET.get('hide_zero_salary_months')
        hide_paid_employees_filter = self.request.GET.get('hide_paid_employees_filter')
        if order == 'unpaid_salaries':
            queryset = order_by_unpaid_salaries(employee_filter, '')
        elif order == '-unpaid_salaries':
            queryset = order_by_unpaid_salaries(employee_filter, '-')
        elif not 'unpaid' in order and employee_filter is not None and employee_filter != '':
            filtered_queryset = find_user_by_name(employee_filter)
            queryset = filtered_queryset.order_by(order)
        else:
            queryset = order_by_default(order)
        if sale_position_filter or production_position_filter or other_position_filter:
            queryset = position_list_and_filtering(self, queryset)
        
        
        if hide_paid_employees_filter is not None and hide_zero_salary_months_filter is not None:
            
            queryset = queryset

        else:
            
            if hide_paid_employees_filter is not None:
                exclude_list = []
                for employee in queryset:
                    if employee.all_unpaid_salaries() == 0 or employee.all_unpaid_salaries() is None:
                        exclude_list.append(employee.id)
                queryset = queryset.exclude(id__in=exclude_list)
                
            if hide_zero_salary_months_filter is not None:
                exclude_list = []
                for employee in queryset:
                    if employee.all_unpaid_salaries() != 0 and employee.all_unpaid_salaries() is not None:
                        exclude_list.append(employee.id)
                queryset = queryset.exclude(id__in=exclude_list)

        if queryset.count() == 0 and (employee_filter is not None or position_filter is not None
                or hide_zero_salary_months_filter is not None or hide_paid_employees_filter is not None) \
                    and self.request.is_ajax() is False:
            messages.add_message(self.request, messages.WARNING,
                                "No employee meets the search criteria. "
                                "Widen your search or check filter for typos.")
        return queryset

class EmployeeDetail(LoginRequiredMixin, OwnershipMixin, ListView):
    model = Month
    template_name = 'employees/employee_detail.html'

    def get_template_names(self, **kwargs):
        if self.request.is_ajax():
            names = ['employees/employee_detail_table.html']
        else:
            names = ['employees/employee_detail.html']
        return names

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            qset = context['object_list']
            orderby = context['orderby']
            try:
                page_obj = context['page_obj']
                paginator = context['paginator']
            except:
                pass
            try:
                years = context['years']
            except:
                pass
            context = {
                'months': qset,
                'paginator': paginator,
                'page_obj': page_obj,
                'orderby': orderby,
                'years': years,
            }
            context['warning_x_days_left'] = WARNING_DAYS_LEFT
            if qset.count() == 0:
                context['empty_qset'] = True
            context['ajax_request'] = True
            return self.response_class(
                request = self.request,
                template = self.get_template_names(),
                context = context,
                **response_kwargs
            )
        else:
            response = super().render_to_response(context, **response_kwargs)
            return super().render_to_response(context, **response_kwargs)

    def get_paginate_by(self, queryset):
        try:
            per_page = self.request.GET.get('per_page') or self.kwargs.get('per_page') or 10
        except:
            per_page = 10
        return per_page

    def get_selected_years(self):
        url = self.request.GET.urlencode()
        selected_years = re.findall(r'\d+', url)
        selected_years = [int(num) for num in selected_years if len(num) > 3]
        return selected_years

    def get_queryset(self):
        employee = Employee.objects.get(pk=self.kwargs.get('pk'))
        order = self.request.GET.get('order', ('-year', '-month'))
        hide_paid_filter = self.request.GET.get('hide_paid_months_filter')
        hide_unpaid_filter = self.request.GET.get('hide_unpaid_months_filter')
        clear_filters = self.request.GET.get('clear_filters')
        selected_years = self.get_selected_years()
        if clear_filters is None:
            if order == 'newest':
                month_queryset = employee.month_set.all().order_by('-year', '-month')

            elif order == 'oldest':
                month_queryset = employee.month_set.all().order_by('year', 'month')

            elif order == 'tbp-up':
                month_queryset = employee.month_set.annotate(
                    to_be_paid=(F('hours_worked_in_this_month')*F('rate_per_hour_this_month'))
                ).order_by('to_be_paid')
            elif order == '-to_be_paid':
                month_queryset = employee.month_set.annotate(
                    to_be_paid=(F('hours_worked_in_this_month')*F('rate_per_hour_this_month'))
                ).order_by('tbp-down')
            elif order == 'hours-up':
                month_queryset = employee.month_set.all().order_by('hours_worked_in_this_month')
            elif order == 'oldest':
                month_queryset = employee.month_set.all().order_by('-hours_worked_in_this_month')

            elif order == 'rph-up':
                month_queryset = employee.month_set.all().order_by('rate_per_hour_this_month')
            elif order == 'rph-down':
                month_queryset = employee.month_set.all().order_by('-rate_per_hour_this_month')
            else:
                try:
                    month_queryset = employee.month_set.all().order_by(order)
                except:
                    month_queryset = employee.month_set.all().order_by('-year', '-month')
            if len(selected_years) != 0:
                month_queryset = month_queryset.filter(year__in=selected_years)
            if hide_paid_filter is not None:
                month_queryset = month_queryset.exclude(salary_is_paid=True)
            if hide_unpaid_filter is not None:
                month_queryset = month_queryset.exclude(salary_is_paid=False)
            if month_queryset.count() == 0 and not employee.month_set.all().count() == 0 \
                and self.request.is_ajax() is False:
                messages.add_message(self.request, messages.WARNING,
                                    "Employee has no months which satisfy specified criteria. Check filters again.")
        else:
            try:
                month_queryset = employee.month_set.all().order_by(order)
            except:
                month_queryset = employee.month_set.all().order_by('-year', '-month')
        return month_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        context['years'] = make_year_list_for_filtering_in_emp_detail(context['employee'])
        selected_years = self.get_selected_years()
        try:
            context['selected_years'] = selected_years
            show_all_years_at_load = [yr for yr in selected_years if yr in context['years'][5:]]
            if len(show_all_years_at_load) == 0:
                context['years_5'] = False
            else:
                context['years_5'] = True
            context['years_hidden'] = context['years'][5:] or None
            context['years_shown'] = context['years'][:5]
        except:
            pass
        context['hide_paid_months_filter'] = self.request.GET.get('hide_paid_months_filter') or False
        context['hide_unpaid_months_filter'] = self.request.GET.get('hide_unpaid_months_filter') or False
        context['orderby'] = self.request.GET.get('order', 'newest')
        context['form_submit_delay'] = FORM_SUBMIT_DELAY
        context['warning_x_days_left'] = WARNING_DAYS_LEFT
        context['per_page'] = self.request.GET.get('per_page') or 10
        return context

class EmployeeCreate(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employees')
    template_name = 'employees/employee_form.html'

    def form_valid(self, form, **kwargs):
        self.object = form.save(commit=False)
        obj = form.save(commit=False)
        if (not form.cleaned_data['password1'] or not obj.has_usable_password()):
            # Django's PasswordResetForm won't let us reset an unusable
            # password. We set it above super() so we don't have to save twice.
            obj.set_password(get_random_string())
            reset_password = True
        else:
            reset_password = False

        super().form_valid(form)

        try:
            form_validation = super().form_valid(form)
            if reset_password:
                reset_form = PasswordResetForm({'email': obj.email})
                assert reset_form.is_valid()
                request = HttpRequest()
                reset_form.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name='registration/password_set_email.html',
                )
            messages.add_message(self.request, messages.SUCCESS,
                                 _("Successfully created employee %s") % self.object.full_name())
            return form_validation
        except:
            messages.add_message(self.request, messages.ERROR,
                                    _("Specified e-mail address has already been assigned to another employee"))
            return HttpResponseRedirect('')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class EmployeeUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    
    model = Employee
    form_class = EmployeeChangeForm
    success_url = reverse_lazy('employees')
    template_name = 'employees/employee_form.html'

    def get_queryset(self, **kwargs):
        try:
            return Employee.objects.filter(pk=self.kwargs['pk'])        
        except:
            messages.add_message(self.request, messages.ERROR, _("This employee does not exist!"))
            return HttpResponseRedirect('../')

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        employee_object = self.get_queryset()
        city_object = employee_object[0].address_city
        initial['address_city'] = city_object
        
        return initial

    def form_valid(self, form, **kwargs):
        
        form_validation = super().form_valid(form)

        messages.add_message(self.request, messages.SUCCESS,
            _("Changes saved for employee %s.") % (self.get_queryset().first()))
        return form_validation

class MonthCreate(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    form_class = MonthForm
    success_url = reverse_lazy('employee_detail')
    template_name = 'employees/month_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('employee_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        self.employee_object = Employee.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['employee'] = self.employee_object
        return context

    def get_initial(self):
        initial = super().get_initial()
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
            form_validation = super().form_valid(form)
            messages.add_message(self.request, messages.SUCCESS,
                                 _("Successfully created month %(month)s %(year)s") % ({
                                    'month':self.object.get_month_display(),
                                    'year':self.object.year}))
            return form_validation
        except:
            if "errorlist nonfield" in str(form.errors):
                messages.add_message(self.request, messages.ERROR,
                                     _("Specified month has already been assigned to employee %s.") %
                                     (employee_object.full_name()))
            return HttpResponseRedirect('')

    def form_invalid(self, form, **kwargs):
        response = super(MonthCreate, self).form_invalid(form, **kwargs)
        employee_object = Employee.objects.get(pk=self.kwargs['pk'])
        if "errorlist nonfield" in str(form.errors):
            messages.add_message(self.request, messages.ERROR,
                                _("Specified month has already been assigned to employee %s.") %
                                (employee_object.full_name()))
        return response

class MonthUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):

    form_class = MonthForm
    template_name = 'employees/month_edit_form.html'

    def get_queryset(self, **kwargs):
        try:
            return Month.objects.filter(pk=self.kwargs['pk'])
        except:
            messages.add_message(self.request, messages.ERROR, _("This month does not exist!"))
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
            context = super().get_context_data(**kwargs)
            employee_object = self.get_object().employee
            context['employee'] = employee_object           
            return context
        except:
            messages.add_message(self.request, messages.ERROR, _("This month does not exist!"))
            return HttpResponseRedirect('../')

    def form_valid(self, form, **kwargs):
        form_validation = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS,
                            _("Successfully edited month %(month)s %(year)s.") %({
                                'month':self.object.get_month_display(),
                                'year':self.object.year}))
        if 'hours_worked_in_this_month' in form.changed_data and self.object.salary_is_paid != True:
            month = Month.objects.get(pk = self.object.id)
            month.month_is_approved = False
            month.save()
        return form_validation

    def form_invalid(self, form, **kwargs):
        employee_object = self.get_object().employee
        if "errorlist nonfield" in str(form.errors):
            messages.add_message(self.request, messages.ERROR,
                                _("Specified month has already been assigned to employee %s.") %
                                (employee_object.full_name()))
        return super(MonthUpdate, self).form_invalid(form, **kwargs)

class MonthApprove(LoginRequiredMixin, MonthOwnershipMixin, UpdateView):

    form_class = MonthApproveForm
    template_name = 'employees/month_approve.html'

    def get_queryset(self, **kwargs):
        try:
            return Month.objects.filter(pk = self.kwargs['pk'])
        except:
            messages.add_message(self.request, messages.ERROR, _("This month does not exist!"))
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
            context = super().get_context_data(**kwargs)
            employee_object = self.get_object().employee
            context['employee'] = employee_object
            return context
        except:
            messages.add_message(self.request, messages.ERROR, _("This month does not exist!"))
            return HttpResponseRedirect('../')

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['month_is_approved'] = True
        return initial

    def form_valid(self, form):
        form_validation = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS,
                            _("Successfully approved month %(month)s %(year)s.") % ({
                                'month':self.object.get_month_display(),
                                'year':self.object.year}))
        return form_validation

    def form_invalid(self, form, **kwargs):
        employee_object = self.get_object().employee
        if "errorlist nonfield" in str(form.errors):
            messages.add_message(self.request, messages.ERROR,
                                _("Specified month has already been assigned to employee %s.") %
                                (employee_object.full_name()))
        return super().form_invalid(form, **kwargs)

class EmployeeDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employees')

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.add_message(self.request, messages.WARNING,
                                 _("Successfully deleted employee %s.") % self.object.full_name())
        except:
            messages.add_message(self.request, messages.ERROR, _("This employee does not exist!"))

        return HttpResponseRedirect(self.success_url)

class MonthDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Month

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
            employee_object = self.get_object().employee
            redirector = employee_object.pk
            success_url = reverse_lazy('employee_detail', kwargs={'pk': redirector})
            messages.add_message(self.request, messages.WARNING,
                                             _("Successfully deleted month %(month)s %(year)s.") % ({
                                                'month':self.get_object().get_month_display(),
                                                'year':self.get_object().year}))
            self.object = self.get_object()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except AttributeError:
            messages.add_message(self.request, messages.ERROR, _("This month does not exist!"))
            HttpResponseRedirect('employees')

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
