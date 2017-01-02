from django.forms import ModelForm, RadioSelect
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UserChangeForm as AuthUserChangeForm
from employees.models import Employee, Month
from django.utils.safestring import mark_safe
from django import forms
from functools import partial

dateinput = partial(forms.DateInput, {'class': 'datepicker'})

# class DateRangeForm(forms.Form):
#     start_date = forms.DateField(widget=DateInput())
#     end_date = forms.DateField(widget=DateInput())

class HorizontalRadioRenderer(RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class EmployeeForm(AuthUserCreationForm):
    
    class Meta:
        model = Employee
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'rate_per_hour', 'contract_start_date', 'contract_exp_date',
         'health_book_exp_date', 'gender', 'position', 'contract_type']
        exclude = []

class EmployeeChangeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['email', 'first_name', 'last_name', 'rate_per_hour', 'contract_start_date', 'contract_exp_date',
         'health_book_exp_date', 'gender', 'position', 'contract_type']
        exclude = []

class MonthForm(ModelForm):
    class Meta:
        model = Month
        exclude = []

        widgets = {
            'salary_is_paid': RadioSelect(renderer=HorizontalRadioRenderer)
        }