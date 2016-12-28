# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import time
from django.contrib import messages
from .forms import EmployeeForm, MonthForm
from .models import Employee, Month


class EmployeeList(LoginRequiredMixin, ListView):
    tmplate_name = 'employees/employee_list.html'
    context_object_name = 'all_employee_list'
    paginate_by = 10

    def get_queryset(self):
        return Employee.objects.order_by("last_name")

class EmployeeDetail(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetail, self).get_context_data(**kwargs)
        employee_object = self.get_object()
        context['months'] = employee_object.month_set.all().order_by('-year', '-month')
        return context

class EmployeeCreate(LoginRequiredMixin, CreateView):

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
            print(str(self.object.employee))
            if "already exists" in str(form.errors):
                messages.add_message(self.request, messages.ERROR,
                                     "Specified e-mail address has already been assigned to another employee")
            return HttpResponseRedirect('')

class EmployeeUpdate(LoginRequiredMixin, UpdateView):

    form_class = EmployeeForm
    success_url = reverse_lazy('employees')
    template_name = 'employees/employee_form.html'

    def get_queryset(self, **kwargs):
        try:
            return Employee.objects.filter(pk=self.kwargs['pk'])
        except:
            messages.add_message(self.request, messages.ERROR, "This employee does not exist!")
            return HttpResponseRedirect('../')

class MonthCreate(LoginRequiredMixin, CreateView):

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

class MonthUpdate(LoginRequiredMixin, UpdateView):

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
        print("dfgdgdd")
        form_validation = super(MonthUpdate, self).form_valid(form)
        print("fsdfgsfs")
        messages.add_message(self.request, messages.SUCCESS,
                             "Successfully edited month %s in year %s." %
                             (self.object.month_name(), self.object.year))
        return form_validation

    def form_invalid(self, form, **kwargs):
        print("ASDFF")
        employee_object = self.get_object().employee
        if "already exists" in str(form.errors):
            messages.add_message(self.request, messages.ERROR,
                                 "Specified month has already been assigned to employee %s." %
                                 (employee_object.full_name()))
        return HttpResponseRedirect('')

class EmployeeDelete(LoginRequiredMixin, DeleteView):
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

class MonthDelete(LoginRequiredMixin, DeleteView):
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