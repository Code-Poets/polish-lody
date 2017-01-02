from django.forms import ModelForm, RadioSelect
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

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['email', 'first_name', 'last_name', 'rate_per_hour', 'contract_start_date', 'contract_exp_date',
         'health_book_exp_date', 'gender', 'position', 'contract_type']
        exclude = []

        widgets = {
            'contract_start_date': forms.DateInput(attrs={'class':'datepicker'}),
            'contract_exp_date': forms.DateInput(attrs={'class':'datepicker'}),
            'health_book_exp_date': forms.DateInput(attrs={'class':'datepicker'}),
        }

class MonthForm(ModelForm):
    class Meta:
        model = Month
        exclude = []

        widgets = {
            'salary_is_paid': RadioSelect(renderer=HorizontalRadioRenderer)
        }