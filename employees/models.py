from __future__ import unicode_literals

import time
from datetime import date
from django.db import models, transaction
from django.utils import timezone
from django.core.validators import validate_email, MinValueValidator, MaxValueValidator

def save_month(mon, yr, Employee, rph):
    month = Month.objects.create(month=mon, year=yr, employee=Employee, rate_per_hour_this_month=rph)
    month.save()

class Employee(models.Model):

    gender_choices = (
        ("1", "Male"),
        ("2", "Female"),
    )
    position_choices = (
        ("1", "Production"),
        ("2", "Sale"),
        ("3", "Other"),
    )
    contract_choices = (
        ("1", "Type 1"),
        ("2", "Type 2"),
        ("3", "Type 3"),
    )

    first_name = models.CharField(max_length=255, default=None)
    last_name = models.CharField(max_length=255, default=None)
    email = models.EmailField(validators=[validate_email], max_length=255, unique=True, default=None)
    rate_per_hour = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0, validators=[
        MinValueValidator(0)
    ])
    employee_password = models.CharField(max_length=64, default=None, blank=True, null=True)
    contract_start_date = models.DateField(blank=True, default=timezone.now, null=True)
    contract_exp_date = models.DateField(blank=True, default=None, null=True)
    health_book_exp_date = models.DateField(blank=True, default=None, null=True)
    gender = models.CharField(max_length=16, null=True, blank=True, default=None,
                              choices=gender_choices)
    position = models.CharField(max_length=16, null=True, blank=True, default=None,
                              choices=position_choices)
    contract_type = models.CharField(blank=True, null=True, default=None, max_length=64,
                                     choices=contract_choices)

    def create_or_update_months_and_years_for_employee(self):

        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December'
                  ]
        years = self.years_employed()
        months_in_start_year, months_in_last_year = self.months_in_first_and_last_year()
        if self.year_set.all().count() == 0:
            for yr in years:
                with transaction.atomic():
                    yr = Year.objects.create(year=yr, employee=self)
                    yr.save()
            db_years_list = list(self.year_set.all())
            if len(db_years_list) != 1:
                with transaction.atomic():
                    for yr in db_years_list:
                        if db_years_list.index(yr) == 0:
                            for mon in months_in_start_year:
                                save_month(mon, yr, self, self.rate_per_hour)
                        elif db_years_list.index(yr) == (len(db_years_list)-1):
                            for mon in months_in_last_year:
                                save_month(mon, yr, self, self.rate_per_hour)
                        else:
                            for mon in months:
                                save_month(mon, yr, self, self.rate_per_hour)
            else:
                with transaction.atomic():
                    for mon in months_in_start_year:
                        save_month(mon, db_years_list[0], self, self.rate_per_hour)
        else:
            db_years_list = list(self.year_set.all())
            print(db_years_list)
            if len(years) == len(db_years_list) and len(db_years_list) != 1:
                for mon in months_in_last_year:
                    if not self.month_set.filter(month=mon).exists():
                        save_month(mon, db_years_list[0], self, self.rate_per_hour)
                for mon in months_in_start_year:
                    if not self.month_set.filter(month=mon).exists():
                        save_month(mon, db_years_list[-1], self, self.rate_per_hour)

            for yr in years:
                print(yr, db_years_list[-1])

                if not self.year_set.filter(year=yr).exists() and years.index(yr) != (len(years)-1)\
                        and years.index(yr) != 0:
                    yr = Year.objects.create(year=yr, employee=self)
                    yr.save()
                    with transaction.atomic():
                        for mon in months:
                            save_month(mon, yr, self, self.rate_per_hour)

                elif self.year_set.filter(year=yr).exists() and len(db_years_list) == 1:
                    with transaction.atomic():
                        for mon in months_in_start_year:
                            if self.month_set.filter(month=mon).exists() == False:
                                save_month(mon, db_years_list[0], self, self.rate_per_hour)

                elif not self.year_set.filter(year=yr).exists() and years.index(yr) == (len(years)-1):
                    yr = Year.objects.create(year=yr, employee=self)
                    yr.save()
                    with transaction.atomic():
                        for mon in months_in_last_year:
                            save_month(mon, yr, self, self.rate_per_hour)

                elif not self.year_set.filter(year=yr).exists() and years.index(yr) == 0:
                    yr = Year.objects.create(year=yr, employee=self)
                    yr.save()
                    with transaction.atomic():
                        for mon in months_in_start_year:
                            save_month(mon, yr, self, self.rate_per_hour)


    def __str__(self):
        return self.first_name + " " + self.last_name

    def full_name(self):
        return self.first_name + " " + self.last_name

    def all_unpaid_months_salary(self):
        all_months = self.month_set.all()
        sum_of_all_months = 0
        for mon in all_months:
            rph = mon.rate_per_hour_this_month
            hpm = mon.hours_worked_in_this_month
            sal = (rph * hpm)
            sum_of_all_months += sal
            sum_of_all_months -= mon.how_much_was_paid_to_employee
        return sum_of_all_months

    def years_employed(self):
        years_employed_list = []
        if self.contract_exp_date.year != self.contract_start_date.year:
            years_employed_list = (range(self.contract_start_date.year, (self.contract_exp_date.year+1)))
            return years_employed_list
        else:
            years_employed_list.append(int(self.contract_start_date.year))
            return years_employed_list

    def months_in_first_and_last_year(self):
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December'
                  ]
        if len(self.years_employed()) != 1:
            months_in_first_year = months[(int(self.contract_start_date.month) - 1):]
            months_in_last_year = months[:(int(self.contract_exp_date.month))]
        else:
            months_in_first_year = months[(int(self.contract_start_date.month) - 1):(int(self.contract_exp_date.month))]
            months_in_last_year = []
        return months_in_first_year, months_in_last_year

    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)

        self.create_or_update_months_and_years_for_employee()

class Year(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    year = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return str(self.year)

class Month(models.Model):


    year = models.ForeignKey(Year, default=2016, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    month = models.CharField(max_length=255, verbose_name=u'Month')
    salary_is_paid = models.BooleanField(default=False, verbose_name=u'Paid?')
    hours_worked_in_this_month = models.IntegerField(blank=True, null=True, default=0, validators=[
        MinValueValidator(0), MaxValueValidator(720)
    ])
    how_much_was_paid_to_employee = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True,
                                                        default=0, validators=[MinValueValidator(0)])
    rate_per_hour_this_month = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True,
                                                        default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        if self.salary_is_paid == False:
            return self.month + " " + str(self.year) + " - " + str(self.employee) + " -- Not paid yet."
        if self.salary_is_paid == True:
            return self.month + " " + str(self.year) + " - " + str(self.employee) + " -- Paid!"

    def month_detail(self):
        return str(self.year) + " " + self.month

    def simple_month_name(self):
        return self.month

    def calculating_salary_for_this_month(self):
        return round((self.rate_per_hour_this_month * self.hours_worked_in_this_month), 2)

    def current_month(self):
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December'
                  ]
        current_date = date.today()
        current_month = months[(current_date.month)-1]
        return current_month

