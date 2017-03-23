# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import time
from django.core.validators import validate_email, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from users.models import MyUser

import re

def is_expiring(exp_date):
    if exp_date is not None:
        expiration_date = exp_date
        current_time = time.time()
        expiration_date = int(time.mktime(time.strptime(str(expiration_date), '%Y-%m-%d')))
        days_left = int((expiration_date - current_time) / 86400)
        if 0 <= days_left <= 30:
            return days_left
        elif 0 > days_left:
            return [days_left, days_left*(-1)]

def sanity_check(account_number):

    assert isinstance(account_number, str) 
    
    if account_number.replace(' ', '').isdigit():
    
        account_number_sans_checksum = account_number.replace(' ', '')[2:]
        original_checksum = int(account_number[0:2])
        new_checksum = 98 - (int(account_number_sans_checksum + '252100') % 97)

        assert new_checksum >= 0

        if new_checksum < 10:
            new_checksum = int('0' + str(new_checksum))

        if original_checksum != new_checksum:
            
            raise ValidationError(_("The bank account number you entered is invalid"))

    else:

        raise ValidationError(_('Bank account number cannot contain letters'))

def phone_check(phone_number):
    
    assert isinstance(phone_number, str)
    
    phone_number_clean = phone_number.replace(' ','')

    if phone_number_clean.replace('+','').isdigit():

        if len(phone_number) <= 3:
            phone_number = ''

        else:

            pattern = re.compile('^\+[0-9]{2}[\s][0-9]{3}[\s][0-9]{3}[\s][0-9]{3}$')
            
            if not pattern.match(phone_number):
                
                raise ValidationError(_("The phone number you entered is invalid"))       

        return phone_number
    
    else:

        raise ValidationError(_('Phone number cannot contain letters'))

def zip_check(zip_code):
    
    assert isinstance(zip_code, str)

    if zip_code.replace('-','').isdigit():

        pattern = re.compile('^[0-9]{2}-[0-9]{3}$')

        if not pattern.match(zip_code):
            
            raise ValidationError(_("The zip code you entered is invalid"))  

    else:
        raise ValidationError(_('Zip code cannot contain letters'))
    

class City(models.Model):

    name = models.CharField(max_length = 50, null = True, blank = True, default = None, unique = True)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    def __str__(self):
        return self.name

class Employee(MyUser):

    gender_choices = (
        ("Male", _("Male")),
        ("Female", _("Female")),
    )
    position_choices = (
        ("Production", _("Production")),
        ("Sale", _("Sale")),
        ("Other", _("Other")),
    )
    contract_choices = (
        ("Fixed-term employment contract", _("Fixed-term employment contract")),
        ("Non-fixed-term employment contract", _("Non-fixed-term employment contract")),
        ("Other", _("Other")),
    )

    rate_per_hour = models.DecimalField(_('rate per hour'),max_digits=7, decimal_places=2, blank=True, default=0, validators=[
        MinValueValidator(0)
    ])
    contract_start_date = models.DateField(_('contract start date'),blank=True, default=timezone.now, null=True)# alter if needed
    contract_exp_date = models.DateField(_('contract exp date'),blank=True, default=None, null=True)
    health_book_exp_date = models.DateField(_('health book exp date'),blank=True, default=None, null=True)
    gender = models.CharField(_('gender'),max_length=16, null=True, blank=True, default=None,
                              choices=gender_choices)
    position = models.CharField(_('position'),max_length=16, null=True, blank=True, default=None,
                              choices=position_choices)
    contract_type = models.CharField(_('contract type'),blank=True, null=True, default=None, max_length=64,
                                     choices=contract_choices)
    
    address_city = models.ForeignKey(City, to_field='name', on_delete=models.SET_NULL, max_length = 30, null=True, blank=True, verbose_name = _('City'), default = None)

    address_street = models.CharField(_('Street'),max_length = 80, null=True, blank=True, default=None)

    address_zip_code = models.CharField(_('Zip code'),max_length = 6, blank = True, null = True, default = None, validators = [zip_check])
    
    bank_account_number = models.CharField(_('Bank account number'),max_length = 32, blank = True, null = True, default = None, validators = [sanity_check])
 
    phone_contact_number = models.CharField(_('Phone contact number'),max_length = 15, blank = True, null = True, default = None, validators = [phone_check])

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    def months_dict(self):
        months_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                       7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        months_enum = list(months_dict.keys())
        return months_dict, months_enum

    def all_unpaid_salaries(self):
        employee_months = self.month_set.all()
        if len(employee_months) != 0:
            unpaid_salaries = 0
            for month in employee_months:
                if month.salary_is_paid is False:
                    ms = month.calculating_salary_for_this_month()
                    unpaid_salaries += ms
            return unpaid_salaries

    def all_unpaid_salaries_for_sorting(self):
        employee_months = self.month_set.all()
        if len(employee_months) != 0:
            unpaid_salaries = 0
            for month in employee_months:
                if month.salary_is_paid is False or month.salary_is_paid == 0:
                    ms = month.calculating_salary_for_this_month()
                    unpaid_salaries += ms
            return unpaid_salaries

    def __str__(self):
        return self.first_name + " " + self.last_name

    def full_name(self):
        return self.last_name + " " + self.first_name

    def is_health_book_expiring(self):
        return is_expiring(self.health_book_exp_date)
    def is_contract_expiring(self):
        return is_expiring(self.contract_exp_date)


class Month(models.Model):

    month_choices = (
        (1, _("January")),
        (2, _("February")),
        (3, _("March")),
        (4, _("April")),
        (5, _("May")),
        (6, _("June")),
        (7, _("July")),
        (8, _("August")),
        (9, _("September")),
        (10, _("October")),
        (11, _("November")),
        (12, _("December")),
    )
    bool_choices = (
        (True, _('Yes')),
        (False, _('No')),
        )
    default_year = date.today().year
    default_month = date.today().month
    months_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                   7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    year = models.PositiveIntegerField(_('year'),default=default_year, validators=[MaxValueValidator(9999)])
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    month = models.IntegerField(_(u'Month'),choices=month_choices, default=default_month)
    salary_is_paid = models.BooleanField(_(u'Paid?'),default=False, choices=bool_choices)
    hours_worked_in_this_month = models.DecimalField(_('hours worked in this month'),decimal_places=1, max_digits=4, default=0,
                                                    validators=[MaxValueValidator(720), MinValueValidator(0)])
    month_is_approved = models.BooleanField(_(u'Approved?'),default=False, choices=bool_choices)
    rate_per_hour_this_month = models.DecimalField(_('rate per hour this month'),decimal_places=2, max_digits=7, default=0,
                                                   validators=[MinValueValidator(0)])
    bonuses = models.DecimalField(_('Bonuses'), decimal_places = 2, max_digits = 7, default = 0, validators = [MinValueValidator(0)])

    def __str__(self):
        return self.months_dict[self.month] + " " + str(self.year)

    def month_status(self):
        if self.salary_is_paid == False:
            return str(self.month) + " " + str(self.year) + " - " + str(self.employee) + " - Not paid yet."
        if self.salary_is_paid == True:
            return str(self.month) + " " + str(self.year) + " - " + str(self.employee) + " - Paid!"

    def month_detail(self):
        return str(self.year) + " " + self.months_dict[int(self.month)]

    def simple_month_name(self):
        return str(self.month)

    def month_name(self):
        return self.months_dict[self.month]

    def calculating_salary_for_this_month(self):
        return round((self.rate_per_hour_this_month * self.hours_worked_in_this_month + self.bonuses), 2)

    class Meta:
        verbose_name = _('month')
        verbose_name_plural = _('months')
        unique_together = (("employee", "month", "year"),)