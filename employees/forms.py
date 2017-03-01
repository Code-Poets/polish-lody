from django.forms import ModelForm, RadioSelect, SelectDateWidget
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm
from employees.models import City, Employee, Month
from django.utils.safestring import mark_safe
from django import forms
from functools import partial
from datetime import datetime 

dateinput = partial(forms.DateInput, {'class': 'datepicker'})

# class DateRangeForm(forms.Form):
#     start_date = forms.DateField(widget=DateInput())
#     end_date = forms.DateField(widget=DateInput())

class HorizontalRadioRenderer(RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class EmployeeForm(AuthUserCreationForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(EmployeeForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

    class Meta:
        model = Employee
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'rate_per_hour', 'contract_start_date', 'contract_exp_date',
         'health_book_exp_date', 'gender', 'position', 'contract_type', 'bank_account_number', 'phone_contact_number',
         'address_street', 'address_zip_code', 'address_city']
        widgets = {
                    'contract_start_date'   : forms.DateInput(attrs={'class': 'datepicker'}),
                    'contract_exp_date'     : forms.DateInput(attrs={'class': 'datepicker'}),
                    'health_book_exp_date'  : forms.DateInput(attrs={'class': 'datepicker'}),
                    'bank_account_number'   : forms.TextInput(attrs = {
                                                                        'autofocus required title' : ' bank account number must have 26 digits'
                                                                        }
                                                                ),
                    'phone_contact_number'   : forms.TextInput(attrs = {'value' : '+48'}),
                    'address_zip_code'      : forms.TextInput(attrs = {
                                                                        'autofocus required title' : ' __-___'
                                                                        }
                                                                ),
                    }

class EmployeeChangeForm(ModelForm):
    #def __init__(self, *args, **kwargs):
    #super().__init__(*args, **kwargs)

    class Meta:
        model = Employee
        fields = ['email', 'first_name', 'last_name', 'rate_per_hour', 'contract_start_date', 'contract_exp_date',
         'health_book_exp_date', 'gender', 'position', 'contract_type', 'bank_account_number', 'phone_contact_number',
         'address_street', 'address_zip_code', 'address_city']
        widgets = {
                    'contract_start_date'   : forms.DateInput(attrs={'class': 'datepicker'}),
                    'contract_exp_date'     : forms.DateInput(attrs={'class': 'datepicker'}),
                    'health_book_exp_date'  : forms.DateInput(attrs={'class': 'datepicker'}),
                    'bank_account_number'   : forms.TextInput(attrs = {
                                                                       'autofocus required title' : ' bank account number must have 26 digits' 
                                                                       }
                                                                ),
                    'phone_contact_number'  : forms.TextInput(attrs = {'value' : '+48'}),
                    'address_zip_code'      : forms.TextInput(attrs = {
                                                                        'autofocus required title' : ' __-___'
                                                                        } 
                                                                ),
                    'address_city'          : forms.TextInput()
                    }

class MonthForm(ModelForm):
    class Meta:
        model = Month
        exclude = ['month_is_approved']

        widgets = {
            'salary_is_paid': RadioSelect(renderer=HorizontalRadioRenderer)
        }

class MonthApproveForm(ModelForm):
    class Meta:
        model = Month
        fields = ['month_is_approved',]
        widgets = {
                    'month_is_approved' : forms.HiddenInput()
                    }                       
