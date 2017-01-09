# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db import models, transaction
from django.utils import timezone
from django.core.validators import validate_email, MinValueValidator, MaxValueValidator

class Employee(models.Model):

    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    position_choices = (
        ("Production", "Production"),
        ("Sale", "Sale"),
        ("Other", "Other"),
    )
    contract_choices = (
        ("Fixed-term employment contract", "Fixed-term employment contract"),
        ("Non-fixed-term employment contract", "Non-fixed-term employment contract"),
        ("Other", "Other"),
    )

    first_name = models.CharField(max_length=255, default=None)
    last_name = models.CharField(max_length=255, default=None)
    email = models.EmailField(validators=[validate_email], max_length=255, unique=True, default=None)
    rate_per_hour = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0, validators=[
        MinValueValidator(0)
    ])
    contract_start_date = models.DateField(blank=True, default=timezone.now, null=True)# alter if needed
    contract_exp_date = models.DateField(blank=True, default=None, null=True)
    health_book_exp_date = models.DateField(blank=True, default=None, null=True)
    gender = models.CharField(max_length=16, null=True, blank=True, default=None,
                              choices=gender_choices)
    position = models.CharField(max_length=16, null=True, blank=True, default=None,
                              choices=position_choices)
    contract_type = models.CharField(blank=True, null=True, default=None, max_length=64,
                                     choices=contract_choices)

    def months_dict(self):
        months_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                       7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        months_enum = list(months_dict.keys())
        return months_dict, months_enum

    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)

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


class Month(models.Model):

    month_choices = (
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
    )
    bool_choices = (
        (True, 'Yes'),
        (False, 'No'),
        )
    default_year = date.today().year
    default_month = date.today().month
    months_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                   7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    year = models.PositiveIntegerField(default=default_year, validators=[MaxValueValidator(9999)])
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    month = models.IntegerField(choices=month_choices, default=default_month, verbose_name=u'Month')
    salary_is_paid = models.BooleanField(default=False, verbose_name=u'Paid?', choices=bool_choices)
    hours_worked_in_this_month = models.DecimalField(decimal_places=1, max_digits=4, default=0,
                                                    validators=[MaxValueValidator(720), MinValueValidator(0)])
    rate_per_hour_this_month = models.DecimalField(decimal_places=2, max_digits=7, default=0,
                                                   validators=[MinValueValidator(0)])

    def __str__(self):
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
        return round((self.rate_per_hour_this_month * self.hours_worked_in_this_month), 2)

    class Meta:
        unique_together = (("employee", "month", "year"),)