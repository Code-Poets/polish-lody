# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from employees.utils import phone_check, sanity_check, zip_check, is_expiring, is_expiring_contract
from users.models import MyUser


class City(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, default=None, unique=True)

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
        ("Contract work", _("Contract work")),  # umowa o dzieło
        ("Fee-for-task contract", _("Fee-for-task contract ")),  # umowa zlecenie
        ("B2B", _("B2B")),
        ("Other", _("Other")),
    )

    rate_per_hour = models.DecimalField(
        _('rate per hour'),
        max_digits=7,
        decimal_places=2,
        blank=True,
        default=0,
        validators=[
            MinValueValidator(0)
        ])

    contract_start_date = models.DateField(
        _('contract start date'),
        blank=True,
        default=timezone.now,
        null=True)  # alter if needed

    contract_exp_date = models.DateField(
        _('contract exp date'),
        blank=True,
        default=None,
        null=True)

    health_book_exp_date = models.DateField(
        _('health book exp date'),
        blank=True,
        default=None,
        null=True)

    gender = models.CharField(
        _('gender'),
        max_length=16,
        blank=False,
        null=True,
        default="Male",
        choices=gender_choices)

    position = models.CharField(
        _('position'),
        max_length=16,
        null=True,
        blank=False,
        default="Other",
        choices=position_choices)

    contract_type = models.CharField(
        _('contract type'),
        blank=True,
        null=True,
        default=None,
        max_length=64,
        choices=contract_choices)

    address_city = models.ForeignKey(
        City,
        to_field='name',
        on_delete=models.SET_NULL,
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('City'),
        default=None)

    address_street = models.CharField(
        _('Street'),
        max_length=80,
        null=True,
        blank=True,
        default=None)

    address_zip_code = models.CharField(
        _('Zip code'),
        max_length=6,
        blank=True,
        null=True,
        default=None,
        validators=[zip_check])

    bank_account_number = models.CharField(
        _('Bank account number'),
        max_length=250,
        blank=True,
        null=True,
        default=None,
        validators=[sanity_check])

    phone_contact_number = models.CharField(
        _('Phone contact number'),
        max_length=15,
        blank=True,
        null=True,
        default=None,
        validators=[phone_check])

    currently_employed = models.BooleanField(
        _('Currently employed'),
        default=True)

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
        return is_expiring_contract(self.contract_exp_date)

    def get_contract_exp_date_string(self):

        if self.contract_exp_date is not None:
            date_to_send = '' + self.contract_exp_date.strftime("%d.%m.%Y")
            return date_to_send
        else:
            return None


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

    year = models.PositiveIntegerField(
        _('year'),
        default=default_year,
        validators=[MaxValueValidator(9999)]
    )

    employee = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    month = models.IntegerField(
        _(u'Month'),
        choices=month_choices,
        default=default_month
    )

    salary_is_paid = models.BooleanField(
        _(u'Paid?'),
        default=False,
        choices=bool_choices
    )

    hours_worked_in_this_month = models.DecimalField(
        _('hours worked in this month'),
        decimal_places=1,
        max_digits=4,
        default=0,
        validators=[MaxValueValidator(720), MinValueValidator(0)]
    )

    month_is_approved = models.BooleanField(
        _(u'Approved?'),
        default=False,
        choices=bool_choices
    )

    month_not_approved_with_comment = models.BooleanField(
        _(u'Approved?'),
        default=False,
        choices=bool_choices
    )

    message_reason_hours_not_approved = models.TextField(
        _('Comment, why you disagree with the hours (optional)'),
        blank=True,
        null=True,
        default=None
    )

    rate_per_hour_this_month = models.DecimalField(
        _('rate per hour this month'),
        decimal_places=2,
        max_digits=7,
        default=0,
        validators=[MinValueValidator(0)]
    )

    bonuses = models.DecimalField(
        _('Bonuses'),
        decimal_places=2,
        max_digits=7,
        default=0,
        validators=[MinValueValidator(0)]
    )

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
