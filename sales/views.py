from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from employees.mixins import StaffRequiredMixin
# Create your views here.
from django.views.generic import TemplateView

class SalesIndex(LoginRequiredMixin, StaffRequiredMixin, TemplateView):

    template_name = 'sales/sales_index.html'
    context_object_name = 'sales_index'