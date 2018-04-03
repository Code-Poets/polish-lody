# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, BaseDeleteView, BaseUpdateView
from django.urls import reverse_lazy
# from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
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
from django.db.models import Case, When, Sum, Value, F, Q, DecimalField
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
        for word, initial in {'A': 'Ą', 'C': 'Ć', 'E': 'Ę', 'L': 'Ł', 'N': 'Ń', 'O': 'Ó', 'S': 'Ś', 'Z': 'Ź', 'Z': 'Ż',
                              'a': 'ą', 'c': 'ć', 'e': 'ę', 'l': 'ł', 'n': 'ń', 'o': 'ó', 's': 'ś', 'z': 'ź',
                              'z': 'ż'}.items():
            polishquery = query
            polishquery = polishquery.replace(word, initial)
            polishqueryarr.append(polishquery)
        for word, initial in {'A': 'Ą', 'C': 'Ć', 'E': 'Ę', 'L': 'Ł', 'N': 'Ń', 'O': 'Ó', 'S': 'Ś', 'Z': 'Ź', 'Z': 'Ż',
                              'a': 'ą', 'c': 'ć', 'e': 'ę', 'l': 'ł', 'n': 'ń', 'o': 'ó', 's': 'ś', 'z': 'ź',
                              'z': 'ż'}.items():
            polishquery = polishquery.replace(word, initial)
            polishqueryarr.append(polishquery)
        data = json.dumps({

            "suggestions":

                [city.name for city in City.objects.filter(
                    Q(name__icontains=query) | reduce(lambda x, y: x | y,
                                                      [Q(name__contains=word) for word in polishqueryarr]))]

        })
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def ajax_verify_email(request):
    if request.GET and request.is_ajax():
        email = request.GET.get('email')
        if Employee.objects.filter(email=email).exists():
            return HttpResponse(json.dumps({
                "status": 1
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


def position_list_and_filtering_session(self, queryset):
    positions = {
        'position_sale': 'Sale',
        'position_production': 'Production',
        'position_other': 'Other',
        # 'position_none': 'None',
    }
    exclude_list = []
    for key in positions.keys():

        if self.request.session[key] is None:
            exclude_list.append(positions[key])
            queryset = queryset.exclude(position=positions[key])

    queryset = queryset.exclude(position=None)
    return queryset


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


def former_and_current_filtering(self, queryset):
    # queryset = queryset.exclude(currently_employed=None) don't need to take caro of None, column Not Null in Data Base
    if self.request.is_ajax():
        if self.request.GET.get('current_employees'):
            queryset = queryset.exclude(currently_employed=False)
        if not self.request.GET.get('current_employees'):
            queryset = queryset.exclude(currently_employed=True)

        return queryset
    else:
        if self.request.session['current_employees']:
            queryset = queryset.exclude(currently_employed=False)
        if not self.request.session['current_employees']:
            queryset = queryset.exclude(currently_employed=True)
        return queryset


def make_paginate_by_list():
    paginate_by = [2, 5, 10, 25, 100]
    return paginate_by


def find_user_by_name(query_name):
    qs = Employee.objects.all()
    for term in query_name.split():
        qs = qs.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term)
                       | Q(first_name__icontains=term.title()) | Q(last_name__icontains=term.title()))
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


class UpdateSession(View):
    # class to update current session

    def post(self, request):
        print('UpdateSession')

        if not request.is_ajax() or not request.method == 'POST':
            from django.http import HttpResponseNotAllowed
            return HttpResponseNotAllowed(['POST'])

        try:
            print('before')
            print('order ' + str(request.session['order']))
            print('position_sale ' + request.session['position_sale'])
            print('position_production ' + request.session['position_production'])
            print('position_other ' + request.session['position_other'])
        except:
            pass

        try:
            order = self.request.POST['order']
            request.session['order'] = order
        except:
            request.session['order'] = 'last_name'

        position_sale = self.__make_true_or_false_from_POST_request(request, 'position_sale')
        request.session['position_sale'] = position_sale
        position_other = self.__make_true_or_false_from_POST_request(request, 'position_other')
        request.session['position_other'] = position_other
        position_production = self.__make_true_or_false_from_POST_request(request, 'position_production')
        request.session['position_production'] = position_production
        hide_paid_employees_filter = self.__make_true_or_false_from_POST_request(request, 'hide_paid_employees_filter')
        request.session['hide_paid_employees_filter'] = hide_paid_employees_filter
        hide_zero_salary_months = self.__make_true_or_false_from_POST_request(request, 'hide_zero_salary_months')
        request.session['hide_zero_salary_months'] = hide_zero_salary_months
        former_employees = self.__make_true_or_false_from_POST_request(request, 'former_employees')
        request.session['former_employees'] = former_employees
        current_employees = self.__make_true_or_false_from_POST_request(request, 'current_employees')
        request.session['current_employees'] = current_employees

        try:
            per_page = self.request.POST['per_page']
            request.session['per_page'] = per_page
        except:
            request.session['per_page'] = 10

        try:
            page = self.request.POST['page']
            request.session['page'] = page
        except:
            request.session['page'] = 1

        print('after')

        print('order ' + str(request.session['order']))
        print('position_sale ' + str(request.session['position_sale']))
        print('position_production ' + str(request.session['position_production']))
        print('position_other ' + str(request.session['position_other']))

        return HttpResponse('ok')

    @staticmethod
    def __make_true_or_false_from_POST_request(request, filer_name):
        try:
            value = request.POST[filer_name]
            if value == 'on':
                return True
            else:
                return False
        except:
            return False

    # @staticmethod
    # def __make_number_from_POST_request(request, filer_name):
    #     try:
    #         value = request.POST[filer_name]
    #         if value == 'on':
    #             return True
    #         else:
    #             return False
    #     except:
    #         return False


class EmployeeList(LoginRequiredMixin, StaffRequiredMixin, ListView):
    template_name = 'employees/employee_list.html'
    context_object_name = 'all_employee_list'

    def get(self, request, *args, **kwargs):

        if self.request.is_ajax():
            self.object_list = self.get_queryset()
            # self.object_list = self.get_queryset_ajax()
            allow_empty = self.get_allow_empty()
            if not allow_empty:
                if self.get_paginate_by_ajax() is not None and hasattr(self.object_list, 'exists'):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = len(self.object_list) == 0
                if is_empty:
                    raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                        'class_name': self.__class__.__name__,
                    })
            context = self.get_context_data()
            return self.render_to_response(context)


        else:
            # self.object_list = self.get_queryset_session_or_default()
            self.object_list = self.get_queryset()
            allow_empty = self.get_allow_empty()
            if not allow_empty:
                if self.get_paginate_by_session_or_default() is not None and hasattr(self.object_list,
                                                                                     'exists'):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = len(self.object_list) == 0
                if is_empty:
                    raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                        'class_name': self.__class__.__name__,
                    })
            # context = self.get_context_data_session_or_default()
            context = self.get_context_data()
            # context = self.get_context_data_session_or_default(self.object_list)
            return self.render_to_response(context)

    def __get_filter_value_from_ajax_or_session_with_default_secure(self, filer_name):
        if self.request.is_ajax():
            try:
                value = self.request.GET.get(filer_name)
                if value == 'on':
                    return True
                if value == True:
                    return True
                else:
                    return False
            except:
                return False
        else:
            if filer_name=='current_employees':
                return self.__make_true_from_SESSION_request(filer_name)
            else:
              try:
                 return self.request.session[filer_name]
              except:
                self.request.session[filer_name] = None
                return None

    # def __make_true_or_false_from_AJAX_request(self, filer_name):
    #     try:
    #         value = self.request.GET.get(filer_name)
    #         if value=='on':
    #             return True
    #         if value==True:
    #             return True
    #         else:
    #             return False
    #     except:
    #         return False
    #
    #
    #
    #
    #
    # def __make_true_or_None_from_SESSION_request(self, filer_name):
    #     try:
    #         return self.request.session[filer_name]
    #     except:
    #         self.request.session[filer_name] = None
    #         return None

    def __make_true_from_SESSION_request(self, filer_name):
        try:
            return self.request.session[filer_name]
        except:
            self.request.session[filer_name] = True
            return True

    def __get_order(self):
        if self.request.is_ajax():
            return self.request.GET.get('order', 'last_name')
        else:
            try:
                return self.request.session['order']
            except:
                return 'last_name'

    def get_queryset(self):
        order = self.__get_order()


        clear_filters = self.__get_filter_value_from_ajax_or_session_with_default_secure('clear_filters')
        sale_position_filter = self.__get_filter_value_from_ajax_or_session_with_default_secure('position_sale')
        former_employees_filter = self.__get_filter_value_from_ajax_or_session_with_default_secure(
                'former_employees')
        current_employees_filter = self.__get_filter_value_from_ajax_or_session_with_default_secure('current_employees')
        production_position_filter = self.__get_filter_value_from_ajax_or_session_with_default_secure('position_production')
        other_position_filter = self.__get_filter_value_from_ajax_or_session_with_default_secure('position_other')
        employee_filter = self.request.GET.get('employee_filter')
        hide_zero_salary_months_filter = self.__get_filter_value_from_ajax_or_session_with_default_secure('hide_zero_salary_months')
        hide_paid_employees_filter = self.__get_filter_value_from_ajax_or_session_with_default_secure('hide_paid_employees_filter')



        if order == 'unpaid_salaries':
            queryset = order_by_unpaid_salaries(employee_filter, '')
        elif order == '-unpaid_salaries':
            queryset = order_by_unpaid_salaries(employee_filter, '-')
        elif not 'unpaid' in order and employee_filter is not None and employee_filter != '':
            filtered_queryset = find_user_by_name(employee_filter)
            queryset = filtered_queryset.order_by(order)
        else:

            queryset = order_by_default(order)

        if not sale_position_filter and not production_position_filter and not other_position_filter:
            pass
        else:
            if not sale_position_filter:
                queryset = queryset.exclude(position='Sale')

            if not production_position_filter:
                queryset = queryset.exclude(position='Production')

            if not other_position_filter:
                queryset = queryset.exclude(position='Other')

        if former_employees_filter or current_employees_filter:

            if former_employees_filter and current_employees_filter:
                pass
            else:
                queryset = former_and_current_filtering(self, queryset)

        if hide_paid_employees_filter is True and hide_zero_salary_months_filter is True:
            queryset = queryset

        else:

            if hide_paid_employees_filter is True:
                exclude_list = []
                for employee in queryset:
                    if employee.all_unpaid_salaries() == 0 or employee.all_unpaid_salaries() is None:
                        exclude_list.append(employee.id)
                queryset = queryset.exclude(id__in=exclude_list)

            if hide_zero_salary_months_filter is True:
                exclude_list = []
                for employee in queryset:
                    if employee.all_unpaid_salaries() != 0 and employee.all_unpaid_salaries() is not None:
                        exclude_list.append(employee.id)
                queryset = queryset.exclude(id__in=exclude_list)

        return queryset


    def __get_active_page_number(self):
        if self.request.is_ajax():
            try:
                page = self.request.GET.get('page')
                if page == None:
                    page = 1
                return page
            except:
                return 1
        else:
            try:
                return self.request.session['page']
            except:
                return 1



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # # employee_list = context['all_employee_list']
        # employee_list = self.object_list
        # # paginator = Paginator(employee_list, self.get_paginate_by_ajax())
        # # context['paginator']=paginator


        paginator=context['paginator']



        active_page_number=self.__get_active_page_number()



        try:
            page_obj = paginator.page(active_page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        qset = page_obj.object_list




        context = {
            'all_employee_list': qset,
            'paginator': paginator,
            'page_obj': page_obj,
            'orderby': self.request.GET.get('order', 'last_name'),
        }

        current_active_per_page = self.get_paginate_by(self.queryset)

        if current_active_per_page is not None:
            context['current_paginate_by_number'] = int(current_active_per_page)




        # context['warning_x_days_left'] = WARNING_DAYS_LEFT
        if qset.count() == 0:
            context['empty_qset'] = True


                          # AJAX
        if self.request.is_ajax():
            context['ajax_request'] = True


                          # SESSION
        else:
            #
            # 'all_employee_list': qset,
            # 'paginator': paginator,
            # 'page_obj': page_obj,
            # 'orderby': order,

            # context['all_employee_list'] = qset

            # context['qset'] = qset

            # context['paginator'] = paginator
            # context['page_obj'] = page_obj
            # context['is_paginated'] = True

            context['paginate_by_numbers'] = make_paginate_by_list()  # określa, ile osób na stronie, 2,5,10, itp.
            context['per_page'] = self.request.GET.get('per_page') or 10  # button przesazujący info jw
            context['active_page_number'] = active_page_number

            context['employee_list'] = page_obj
            # context['orderby'] = self.request.GET.get('order', 'last_name')
            try:
                context['orderby'] = self.request.session['order']
            except:
                context['orderby'] = 'last_name'

            # filtry pozycji

            context['position_sale'] = self.__set_boolean_from_session_with_exception_secure(
                self.request.session['position_sale'])
            context['position_production'] = self.__set_boolean_from_session_with_exception_secure(
                self.request.session['position_production'])
            context['position_other'] = self.__set_boolean_from_session_with_exception_secure(
                self.request.session['position_other'])

            context['hide_zero_salary_months'] = self.__set_boolean_from_session_with_exception_secure(
                self.request.session['hide_zero_salary_months'])

            context['hide_paid_employees_filter'] = self.__set_boolean_from_session_with_exception_secure(
                self.request.session['hide_paid_employees_filter'])

            context['former_employees'] = self.__set_boolean_from_session_with_exception_secure(
                self.request.session['former_employees'])









            # context['position_sale'] = self.request.GET.get('position_sale') or False
            # context['position_production'] = self.request.GET.get('position_production') or False
            # context['position_other'] = self.request.GET.get('position_other') or False
            # context['hide_zero_salary_months'] = self.request.GET.get('hide_zero_salary_months') or False
            # context['hide_paid_employees_filter'] = self.request.GET.get('hide_paid_employees_filter') or False
            # context['former_employees'] = self.request.GET.get('former_employees') or False


            # ustawia domyślnie zaznaczonych obecnych pracowników. Dlatego tak wyjątkowo
            try:
                if self.request.session['current_employees'] == None:
                    context['current_employees'] = True
                else:
                    context['current_employees'] = self.request.session['current_employees']

            except:
                context['current_employees'] = None

            # context['employees_action'] = self.request.GET.get('employees_action') or False





        context['warning_x_days_left'] = WARNING_DAYS_LEFT
        context['form_submit_delay'] = FORM_SUBMIT_DELAY

        return context


    def get_context_data_session_or_default(self, objects_list, **kwargs):

        context = super().get_context_data(**kwargs)
        employee_list = context['all_employee_list']

        paginator = Paginator(employee_list, self.get_paginate_by(employee_list))

        try:
            page = self.request.session['page']
        except:
            page = 1

        pg = self.get_paginate_by(employee_list)
        self.paginate_queryset(employee_list, self.get_paginate_by(employee_list))

        if pg is not None:
            context['current_paginate_by_number'] = int(pg)
        try:
            employee_pages = paginator.page(page)
        except PageNotAnInteger:
            employee_pages = paginator.page(1)
        except EmptyPage:
            employee_pages = paginator.page(paginator.num_pages)

        qset = employee_pages.object_list

        #   TO HARD REFACTOR !!!!
        context['paginate_by_numbers'] = make_paginate_by_list()
        context['employee_list'] = employee_pages

        qset = employee_pages.object_list

        context['qset'] = qset
        context['paginator'] = paginator
        context['page_obj'] = employee_pages
        context['employee_list'] = qset
        context['object_list'] = qset
        context['all_employee_list'] = qset
        context['is_paginated'] = True
        try:
            context['orderby'] = self.request.session['order']
        except:
            context['orderby'] = 'last_name'
        # context['order'] = self.request.session['order']
        # generuje błąd klucza

        context['hide_zero_salary_months'] = self.__set_boolean_from_session_with_exception_secure(
            self.request.session['hide_zero_salary_months'])

        context['former_employees'] = self.__set_boolean_from_session_with_exception_secure(
            self.request.session['former_employees'])
        context['current_employees'] = self.__set_boolean_from_session_with_exception_secure(
            self.request.session['current_employees'])

        # ustawia domyślnie zaznaczonych obecnych pracowników. Dlatego tak wyjątkowo
        try:
            if self.request.session['current_employees'] == None:
                context['current_employees'] = True
            else:
                context['current_employees'] = self.request.session['current_employees']

        except:
            context['current_employees'] = None

        context['hide_paid_employees_filter'] = self.__set_boolean_from_session_with_exception_secure(
            self.request.session['hide_paid_employees_filter'])
        context['per_page'] = self.request.GET.get('per_page') or 10
        context['page'] = page
        context['warning_x_days_left'] = WARNING_DAYS_LEFT
        context['position_sale'] = self.__set_boolean_from_session_with_exception_secure(
            self.request.session['position_sale'])
        context['position_production'] = self.__set_boolean_from_session_with_exception_secure(
            self.request.session['position_production'])
        context['position_other'] = self.__set_boolean_from_session_with_exception_secure(
            self.request.session['position_other'])
        context['form_submit_delay'] = FORM_SUBMIT_DELAY
        return context

    # def get_context_data_session_or_default_archiwum_względnie_działające(self, objects_list, **kwargs):
    #
    #     context = super().get_context_data(**kwargs)
    #     employee_list = context['all_employee_list']
    #
    #     paginator = Paginator(employee_list, self.get_paginate_by_session_or_default())
    #
    #     try:
    #         page = self.request.session['page']
    #     except:
    #         page = 1
    #
    #     pg = self.get_paginate_by_session_or_default()
    #
    #     if pg is not None:
    #         context['current_paginate_by_number'] = int(pg)
    #     try:
    #         employee_pages = paginator.page(page)
    #     except PageNotAnInteger:
    #         employee_pages = paginator.page(1)
    #     except EmptyPage:
    #         employee_pages = paginator.page(paginator.num_pages)
    #
    #     qset = employee_pages.object_list
    #     #
    #     # context['qset'] = qset
    #     # context['paginator'] = paginator
    #     # context['page_obj'] = employee_pages
    #
    #     #
    #     # context = super().get_context_data(**kwargs)
    #     # employee_list = objects_list
    #     # # employee_list = self.object_list
    #     # paginate_by = self.get_paginate_by_session_or_default()
    #     #
    #     # print('paginate by ' + str(paginate_by))
    #     # print('employee_list ' + str(employee_list))
    #     # paginator = Paginator(employee_list, paginate_by)
    #     # context['paginator'] = paginator
    #     #
    #     # try:
    #     #     page = self.request.session['page']
    #     # except:
    #     #     page = 1
    #     #
    #     # pg = self.get_paginate_by_session_or_default()
    #     #
    #     # if pg is not None:
    #     #     context['current_paginate_by_number'] = int(pg)
    #     # try:
    #     #     employee_pages = paginator.page(page)
    #     # except PageNotAnInteger:
    #     #     employee_pages = paginator.page(1)
    #     # except EmptyPage:
    #     #     employee_pages = paginator.page(paginator.num_pages)
    #
    #     context['paginate_by_numbers'] = make_paginate_by_list()
    #     context['employee_list'] = employee_pages
    #     context['orderby'] = self.request.GET.get('order', 'last_name')
    #     #
    #     qset = employee_pages.object_list
    #
    #     context['qset'] = qset
    #     context['paginator'] = paginator
    #     context['page_obj'] = employee_pages
    #     context['employee_list'] = qset
    #     #
    #
    #     # context['position_filter'] = self.__set_boolean_from_session_with_exception_secure(self.request.COOKIES['position_filter'])
    #     # context['position_filter'] = self.__set_boolean_from_session_with_exception_secure(self.request.COOKIES['position_filter'])
    #     # context['position_filter'] = self.__set_boolean_from_session_with_exception_secure(self.request.COOKIES['position_filter'])
    #
    #     #
    #     # print(self.request.COOKIES['employee_filter'])
    #     #
    #     #
    #     # print(self.__set_boolean_from_session_with_exception_secure(self.request.COOKIES['employee_filter']))
    #
    #     # context['employee_filter'] = self.__set_boolean_from_session_with_exception_secure(self.request.COOKIES['employee_filter'])
    #
    #     context['hide_zero_salary_months'] = self.__set_boolean_from_session_with_exception_secure(
    #         self.request.session['hide_zero_salary_months'])
    #
    #     context['former_employees'] = self.__set_boolean_from_session_with_exception_secure(
    #         self.request.session['former_employees'])
    #     context['current_employees'] = self.__set_boolean_from_session_with_exception_secure(
    #         self.request.session['current_employees'])
    #
    #     context['hide_paid_employees_filter'] = self.__set_boolean_from_session_with_exception_secure(
    #         self.request.session['hide_paid_employees_filter'])
    #     context['per_page'] = self.request.GET.get('per_page') or 10
    #     context['page'] = page
    #     context['warning_x_days_left'] = WARNING_DAYS_LEFT
    #     context['position_sale'] = self.__set_boolean_from_session_with_exception_secure(
    #         self.request.session['position_sale'])
    #     context['position_production'] = self.__set_boolean_from_session_with_exception_secure(
    #         self.request.session['position_production'])
    #     context['position_other'] = self.__set_boolean_from_session_with_exception_secure(
    #         self.request.session['position_other'])
    #     context['form_submit_delay'] = FORM_SUBMIT_DELAY
    #     return context
    #
    def render_to_response_session_or_default(self, context, **response_kwargs):

        # qset = context['qset']
        # order = context['orderby']
        # try:
        #     page_obj = context['page_obj']
        #     paginator = context['paginator']
        #
        # except:
        #     pass
        # context = {
        #     'all_employee_list': qset,
        #     'paginator': paginator,
        #     'page_obj': page_obj,
        #     'orderby': order,
        # }
        # context['warning_x_days_left'] = WARNING_DAYS_LEFT
        # if qset.count() == 0:
        #     context['empty_qset'] = True
        #
        # return self.response_class(
        #     request=self.request,
        #     template=self.get_template_names(),
        #     context=context,
        #     **response_kwargs)

        response = super().render_to_response(context, **response_kwargs)
        return response

    # AJAX                     AJAX                     AJAX                     AJAX                     AJAX                     AJAX                     AJAX

    def get_context_data_ajax(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_list = context['all_employee_list']

        paginator = Paginator(employee_list, self.get_paginate_by_ajax())

        try:
            page = self.request.GET.get('page')
            if page == None:
                page = 1
        except:
            page = 1

        pg = self.get_paginate_by_ajax()
        if pg is not None:
            context['current_paginate_by_number'] = int(pg)
        try:
            employee_pages = paginator.page(page)
        except PageNotAnInteger:
            employee_pages = paginator.page(1)
        except EmptyPage:
            employee_pages = paginator.page(paginator.num_pages)

        qset = employee_pages.object_list

        context['qset'] = qset
        context['paginator'] = paginator
        context['page_obj'] = employee_pages
        # context['is_paginated'] = True

        context['paginate_by_numbers'] = make_paginate_by_list()
        context['employee_list'] = employee_pages
        context['orderby'] = self.request.GET.get('order', 'last_name')
        context['position_filter'] = self.request.GET.get('position_filter')
        context['employee_filter'] = self.request.GET.get('employee_filter') or _('e.g. Darth Vader')
        context['hide_zero_salary_months'] = self.request.GET.get('hide_zero_salary_months') or False

        context['former_employees'] = self.request.GET.get('former_employees') or False
        context['current_employees'] = self.request.GET.get('current_employees') or False
        context['employees_action'] = self.request.GET.get('employees_action') or False

        context['hide_paid_employees_filter'] = self.request.GET.get('hide_paid_employees_filter') or False
        context['per_page'] = self.request.GET.get('per_page') or 10
        context['page'] = page
        context['warning_x_days_left'] = WARNING_DAYS_LEFT
        context['position_sale'] = self.request.GET.get('position_sale') or False
        context['position_production'] = self.request.GET.get('position_production') or False
        context['position_other'] = self.request.GET.get('position_other') or False
        context['form_submit_delay'] = FORM_SUBMIT_DELAY
        return context

    def get_template_names(self, **kwargs):
        if self.request.is_ajax():
            names = ['employees/employee_list_table.html']
        else:
            names = ['employees/employee_list.html']
        return names

    # def render_to_response_ajax(self, context, **response_kwargs):
    #
    #     # if self.request.is_ajax():
    #     print("render to respose ajax")
    #     qset = context['qset']
    #     order = context['orderby']
    #     try:
    #         page_obj = context['page_obj']
    #         paginator = context['paginator']
    #
    #     except:
    #         pass
    #     # context = {
    #     #     # 'all_employee_list': qset,
    #     #     # 'paginator': paginator,
    #     #     # 'page_obj': page_obj,
    #     #     # 'orderby': order,
    #     # }
    #     # context['warning_x_days_left'] = WARNING_DAYS_LEFT
    #     # if qset.count() == 0:
    #     #     context['empty_qset'] = True
    #     # context['ajax_request'] = True
    #     response = self.response_class(
    #         request=self.request,
    #         template=self.get_template_names(),
    #         context=context,
    #         **response_kwargs)
    #     return response

    # else:
    #     print("render to respose NO ajax")
    #     response = super().render_to_response(context, **response_kwargs)
    #     return super().render_to_response(context, **response_kwargs)

    def get_paginate_by_ajax(self):
        try:
            per_page = self.request.GET.get('per_page') or self.kwargs.get('per_page') or 10
        except:
            per_page = 10
        return per_page

    def get_paginate_by_session_or_default(self):
        try:
            per_page = self.request.session['per_page'] or 10
        except:
            per_page = 10
        return per_page


    def get_paginate_by(self, queryset):
        if self.request.is_ajax():
            return self.get_paginate_by_ajax()
        else:
            return self.get_paginate_by_session_or_default()


    # def get_context_data(self, **kwargs):
    #
    #     print("COOKIES")
    #     # print(self.request.COOKIES)
    #     print("current_employees")
    #     # print(self.request.COOKIES['current_employees'])
    #
    #     if not self.request.is_ajax():
    #         try:
    #             # context = self.get_context_data_ajax_or_default()
    #             context = self.get_context_data_no_ajax_from_cookie()
    #         #     blok ładujący z cookie
    #         except:
    #             context = self.get_context_data_ajax_or_default()
    #
    #     else:
    #         context = self.get_context_data_ajax_or_default()
    #
    #     return context

    @staticmethod
    def __set_boolean_from_session_with_exception_secure(boolean_value):
        try:
            return boolean_value
        except:
            return False


class EmployeeAction(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Employee

    def post(self, request, *args, **kwargs):
        dismiss_array = request.POST.getlist('dismiss[]')
        add_one_array = request.POST.getlist('add_one[]')
        add_three_array = request.POST.getlist('add_three[]')

        message_dismiss = "OK"
        message_add_one = "OK"
        message_add_three = "OK"

        for employee_id in dismiss_array:
            try:
                status = self.dismiss_employee(employee_id)
                if not status:
                    message_dismiss = "Fail"
            except:
                message_dismiss = "Fail"

        for employee_id in add_one_array:
            try:
                status = self.add_one_month(employee_id)
                if not status:
                    message_add_one = "Fail"
            except:
                message_add_one = "Fail"

        for employee_id in add_three_array:
            try:
                status = self.add_three_months(employee_id)
                if not status:
                    message_add_three = "Fail"
            except:
                message_add_three = "Fail"

        your_list = [message_dismiss, message_add_one, message_add_three]
        your_list_as_json = json.dumps(your_list)
        return HttpResponse(your_list_as_json)

    @staticmethod
    def dismiss_employee(employee_id):
        employee_to_dismiss = Employee.objects.get(pk=employee_id)
        employee_to_dismiss.currently_employed = False
        employee_to_dismiss.save()

        dismissed_employee = Employee.objects.get(pk=employee_id)
        if not dismissed_employee.currently_employed:
            return True
        else:
            return False

    @staticmethod
    def add_one_month(employee_id):
        employee_to_update = Employee.objects.get(pk=employee_id)

        old_date = employee_to_update.contract_exp_date

        day = old_date.day
        old_month = old_date.month
        old_year = old_date.year

        new_year = old_year
        new_month = old_month + 1

        if new_month == 13:
            new_month = 1
            new_year = old_year + 1

        import datetime
        new_date = datetime.date(new_year, new_month, day)
        employee_to_update.contract_exp_date = new_date
        employee_to_update.save()

        updated_employee = Employee.objects.get(pk=employee_id)
        updated_date = updated_employee.contract_exp_date

        if ((old_date.day == updated_date.day) and (old_date.month + 1 == updated_date.month) and (
                old_date.year == updated_date.year)):
            return True

        elif ((old_date.day == updated_date.day) and (updated_date.month == 1) and (
                old_date.year + 1 == updated_date.year)):
            return True

        else:
            return False

    @staticmethod
    def add_three_months(employee_id):
        employee_to_update = Employee.objects.get(pk=employee_id)

        old_date = employee_to_update.contract_exp_date

        day = old_date.day
        old_month = old_date.month
        old_year = old_date.year

        new_year = old_year

        new_month = old_month + 3

        if new_month == 13:
            new_month = 1
            new_year = old_year + 1

        if new_month == 14:
            new_month = 2
            new_year = old_year + 1

        if new_month == 15:
            new_month = 3
            new_year = old_year + 1

        import datetime
        new_date = datetime.date(new_year, new_month, day)
        employee_to_update.contract_exp_date = new_date
        employee_to_update.save()

        updated_employee = Employee.objects.get(pk=employee_id)
        updated_date = updated_employee.contract_exp_date

        if ((old_date.day == updated_date.day) and (old_date.month + 3 == updated_date.month) and (
                old_date.year == updated_date.year)):
            return True

        elif ((old_date.day == updated_date.day) and (updated_date.month == 1) and (
                old_date.year + 1 == updated_date.year)):
            return True

        elif ((old_date.day == updated_date.day) and (updated_date.month == 2) and (
                old_date.year + 1 == updated_date.year)):
            return True

        elif ((old_date.day == updated_date.day) and (updated_date.month == 3) and (
                old_date.year + 1 == updated_date.year)):
            return True

        else:
            return False


#
# def post(self, request, *args, **kwargs):
#     return self.delete(request, *args, **kwargs)
#
#
# def get_queryset(self):
#     queryset=None
# #     clear_filters = self.request.GET.get('clear_filters')
# #     # order = self.request.GET.get('order', 'last_name')
# #     #
# #     # sale_position_filter = self.request.GET.get('position_sale') or False
# #     # former_employees_filter = self.request.GET.get('former_employees') or False
# #     # current_employees_filter = self.request.GET.get('current_employees') or False
# #     #
# #     # production_position_filter = self.request.GET.get('position_production') or False
# #     # other_position_filter = self.request.GET.get('position_other') or False
# #     # employee_filter = self.request.GET.get('employee_filter')
# #     # position_filter = self.request.GET.get('position_filter')
# #     # hide_zero_salary_months_filter = self.request.GET.get('hide_zero_salary_months')
# #     #
# #     # hide_paid_employees_filter = self.request.GET.get('hide_paid_employees_filter')
# #     # if order == 'unpaid_salaries':
# #     #     queryset = order_by_unpaid_salaries(employee_filter, '')
# #     # elif order == '-unpaid_salaries':
# #     #     queryset = order_by_unpaid_salaries(employee_filter, '-')
# #     # elif not 'unpaid' in order and employee_filter is not None and employee_filter != '':
# #     #     filtered_queryset = find_user_by_name(employee_filter)
# #     #     queryset = filtered_queryset.order_by(order)
# #     # else:
# #     #     queryset = order_by_default(order)
# #     # if sale_position_filter or production_position_filter or other_position_filter:
# #     #     queryset = position_list_and_filtering(self, queryset)
# #     #
# #     # if former_employees_filter or current_employees_filter:
# #     #
# #     #     if former_employees_filter and current_employees_filter:
# #     #         queryset = queryset
# #     #     else:
# #     #         queryset = former_and_current_filtering(self, queryset)
# #     #
# #     # if hide_paid_employees_filter is not None and hide_zero_salary_months_filter is not None:
# #     #
# #     #     queryset = queryset
# #     #
# #     # else:
# #     #
# #     #     if hide_paid_employees_filter is not None:
# #     #         exclude_list = []
# #     #         for employee in queryset:
# #     #             if employee.all_unpaid_salaries() == 0 or employee.all_unpaid_salaries() is None:
# #     #                 exclude_list.append(employee.id)
# #     #         queryset = queryset.exclude(id__in=exclude_list)
# #     #
# #     #     if hide_zero_salary_months_filter is not None:
# #     #         exclude_list = []
# #     #         for employee in queryset:
# #     #             if employee.all_unpaid_salaries() != 0 and employee.all_unpaid_salaries() is not None:
# #     #                 exclude_list.append(employee.id)
# #     #         queryset = queryset.exclude(id__in=exclude_list)
# #     #
# #     # if queryset.count() == 0 and (employee_filter is not None or position_filter is not None
# #     #                               or hide_zero_salary_months_filter is not None or hide_paid_employees_filter is not None) \
# #     #         and self.request.is_ajax() is False:
# #     #     messages.add_message(self.request, messages.WARNING,
# #     #                          "No employee meets the search criteria. "
# #     #                          "Widen your search or check filter for typos.")
#     return queryset


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

            print("render to response ajax")
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
                request=self.request,
                template=self.get_template_names(),
                context=context,
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
                    to_be_paid=(F('hours_worked_in_this_month') * F('rate_per_hour_this_month'))
                ).order_by('to_be_paid')
            elif order == '-to_be_paid':
                month_queryset = employee.month_set.annotate(
                    to_be_paid=(F('hours_worked_in_this_month') * F('rate_per_hour_this_month'))
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

    def get(self, request, *args, **kwargs):
        # self.add_filters_to_cookie()
        self.object_list = self.get_queryset()

        allow_empty = self.get_allow_empty()
        if not allow_empty:

            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

    #
    #
    # def add_filters_to_cookie(self):
    #     self.request.session['testFilter']='exampleValue4'
    #     self.request.session.modified = True


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
                                     'month': self.object.get_month_display(),
                                     'year': self.object.year}))
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
                             _("Successfully edited month %(month)s %(year)s.") % ({
                                 'month': self.object.get_month_display(),
                                 'year': self.object.year}))
        if 'hours_worked_in_this_month' in form.changed_data and self.object.salary_is_paid != True:
            month = Month.objects.get(pk=self.object.id)
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


class MonthApproveBase(LoginRequiredMixin, MonthOwnershipMixin, UpdateView):

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

    def form_valid(self, form):
        form_validation = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS,
                             _("Successfully updated month %(month)s %(year)s.") % ({
                                 'month': self.object.get_month_display(),
                                 'year': self.object.year}))
        return form_validation

    def form_invalid(self, form, **kwargs):
        employee_object = self.get_object().employee
        if "errorlist nonfield" in str(form.errors):
            messages.add_message(self.request, messages.ERROR,
                                 _("Specified month has already been assigned to employee %s.") %
                                 (employee_object.full_name()))
        return super().form_invalid(form, **kwargs)


class MonthApprove(MonthApproveBase):
    form_class = MonthApproveForm
    template_name = 'employees/month_approve.html'

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['month_is_approved'] = True
        return initial


class Month_NOT_Approve(MonthApproveBase):
    form_class = MonthApproveForm
    model = Month
    template_name = 'employees/month_NOT_approve.html'

    # Employee.objects.get(pk=employee_id)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # print('post ')
        # print(request.POST.get('employee_message'))
        # print(self.kwargs['pk'])

        pk = self.kwargs['pk']
        employee_message = request.POST.get('employee_message')
        month_to_update = Month.objects.get(id=int(pk))

        month_to_update.message_reason_hours_not_approved = employee_message
        month_to_update.save()

        self.object = self.get_object()
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['month_not_approved_with_comment'] = True
        return initial


class EmployeeMessage(DetailView):
    model = Month
    template_name = 'employees/employee_message.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            employee_message = self.object.message_reason_hours_not_approved
        except:
            employee_message = str(_("Unexpected problem with getting message from employee"))

        if employee_message == None or employee_message == "":
            employee_message = str(_("No message from employee"))

        employee_message_as_json = json.dumps(employee_message)
        return HttpResponse(employee_message_as_json)


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
                                     'month': self.get_object().get_month_display(),
                                     'year': self.get_object().year}))
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
